"""
Quantum Auth Handler - Supabase authentication with Google and Azure AD
Handles user authentication and authorization
"""

import os
import hashlib
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
import httpx
from supabase import create_client, Client

class AuthHandler:
    """
    Authentication handler with multiple providers
    - Supabase (email/password)
    - Google OAuth
    - Azure AD
    """
    
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL", "")
        self.supabase_key = os.getenv("SUPABASE_KEY", "")
        
        # Initialize Supabase client
        self.supabase: Optional[Client] = None
        if self.supabase_url and self.supabase_key:
            try:
                self.supabase = create_client(self.supabase_url, self.supabase_key)
                print(f"✅ Supabase connected: {self.supabase_url}")
            except Exception as e:
                print(f"⚠️ Supabase connection failed: {e}")
        
        # OAuth credentials
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        self.google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")
        
        self.azure_client_id = os.getenv("AZURE_CLIENT_ID", "")
        self.azure_client_secret = os.getenv("AZURE_CLIENT_SECRET", "")
        self.azure_tenant_id = os.getenv("AZURE_TENANT_ID", "")
        
        # In-memory user store (use database in production)
        self.users: Dict[str, Dict] = {}
        self.sessions: Dict[str, Dict] = {}
        
        # Rate limiting
        self.login_attempts: Dict[str, list] = {}
        
    async def signup(self, email: str, password: str) -> Dict:
        """
        Register a new user via Supabase Auth
        """
        # Validate email
        if not self._validate_email(email):
            return {
                "success": False,
                "error": "Invalid email format"
            }
        
        # Validate password
        password_check = self._validate_password(password)
        if not password_check["valid"]:
            return {
                "success": False,
                "error": password_check["message"]
            }
        
        # Try Supabase signup first
        if self.supabase:
            try:
                auth_response = self.supabase.auth.sign_up({
                    "email": email,
                    "password": password
                })
                
                if auth_response.user:
                    # Create profile
                    user_data = {
                        "id": auth_response.user.id,
                        "email": email,
                        "name": email.split("@")[0],
                        "auth_provider": "email",
                        "profile": {
                            "name": email.split("@")[0],
                            "avatar_url": None,
                            "settings": self._default_settings()
                        },
                        "stats": {
                            "conversations": 0,
                            "images_generated": 0,
                            "searches": 0
                        }
                    }
                    
                    return {
                        "success": True,
                        "user": user_data,
                        "session": {
                            "access_token": auth_response.session.access_token if auth_response.session else None,
                            "user_id": auth_response.user.id
                        },
                        "message": "Account created successfully! Check your email to confirm."
                    }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Signup failed: {str(e)}"
                }
        
        # Fallback to local storage if Supabase not configured
        user_id = self._hash_email(email)
        if user_id in self.users:
            return {
                "success": False,
                "error": "User already exists"
            }
        
        # Create user locally
        user = {
            "id": user_id,
            "email": email,
            "password_hash": self._hash_password(password),
            "created_at": datetime.now().isoformat(),
            "auth_provider": "email",
            "profile": {
                "name": email.split("@")[0],
                "avatar_url": None,
                "settings": self._default_settings()
            },
            "stats": {
                "conversations": 0,
                "images_generated": 0,
                "searches": 0
            }
        }
        
        self.users[user_id] = user
        session = self._create_session(user_id)
        
        return {
            "success": True,
            "user": self._sanitize_user(user),
            "session": session,
            "message": "Account created successfully!"
        }
    
    async def login(self, email: str, password: str) -> Dict:
        """
        Authenticate user via Supabase Auth
        """
        # Check rate limiting
        if not self._check_rate_limit(email):
            return {
                "success": False,
                "error": "Too many login attempts. Please try again later."
            }
        
        # Try Supabase login first
        if self.supabase:
            try:
                auth_response = self.supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                
                if auth_response.user:
                    user_data = {
                        "id": auth_response.user.id,
                        "email": auth_response.user.email,
                        "name": auth_response.user.user_metadata.get("name", email.split("@")[0]),
                        "auth_provider": "email",
                        "profile": {
                            "name": auth_response.user.user_metadata.get("name", email.split("@")[0]),
                            "avatar_url": auth_response.user.user_metadata.get("avatar_url"),
                            "settings": self._default_settings()
                        },
                        "stats": {
                            "conversations": 0,
                            "images_generated": 0,
                            "searches": 0
                        }
                    }
                    
                    return {
                        "success": True,
                        "user": user_data,
                        "session": {
                            "access_token": auth_response.session.access_token if auth_response.session else None,
                            "user_id": auth_response.user.id
                        },
                        "message": f"Welcome back, {user_data['name']}!"
                    }
            except Exception as e:
                self._record_login_attempt(email)
                return {
                    "success": False,
                    "error": "Invalid email or password"
                }
        
        # Fallback to local storage
        user_id = self._hash_email(email)
        
        if user_id not in self.users:
            self._record_login_attempt(email)
            return {
                "success": False,
                "error": "Invalid email or password"
            }
        
        user = self.users[user_id]
        
        if not self._verify_password(password, user["password_hash"]):
            self._record_login_attempt(email)
            return {
                "success": False,
                "error": "Invalid email or password"
            }
        
        session = self._create_session(user_id)
        
        return {
            "success": True,
            "user": self._sanitize_user(user),
            "session": session,
            "message": f"Welcome back, {user['profile']['name']}!"
        }
    
    async def google_auth(self, token: str) -> Dict:
        """
        Authenticate user with Google OAuth token
        """
        try:
            # Verify Google token
            google_user = await self._verify_google_token(token)
            
            if not google_user:
                return {
                    "success": False,
                    "error": "Invalid Google token"
                }
            
            # Check if user exists, create if not
            user_id = self._hash_email(google_user["email"])
            
            if user_id not in self.users:
                user = {
                    "id": user_id,
                    "email": google_user["email"],
                    "password_hash": None,
                    "created_at": datetime.now().isoformat(),
                    "auth_provider": "google",
                    "profile": {
                        "name": google_user.get("name", google_user["email"].split("@")[0]),
                        "avatar_url": google_user.get("picture"),
                        "settings": self._default_settings()
                    },
                    "stats": {
                        "conversations": 0,
                        "images_generated": 0,
                        "searches": 0
                    }
                }
                self.users[user_id] = user
            else:
                # Update profile if changed
                user = self.users[user_id]
                user["profile"]["name"] = google_user.get("name", user["profile"]["name"])
                user["profile"]["avatar_url"] = google_user.get("picture", user["profile"]["avatar_url"])
            
            session = self._create_session(user_id)
            
            return {
                "success": True,
                "user": self._sanitize_user(self.users[user_id]),
                "session": session,
                "message": f"Welcome, {self.users[user_id]['profile']['name']}!"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Google authentication failed: {str(e)}"
            }
    
    async def azure_auth(self, token: str) -> Dict:
        """
        Authenticate user with Azure AD token
        """
        try:
            # Verify Azure AD token
            azure_user = await self._verify_azure_token(token)
            
            if not azure_user:
                return {
                    "success": False,
                    "error": "Invalid Azure AD token"
                }
            
            # Check if user exists, create if not
            user_id = self._hash_email(azure_user["email"])
            
            if user_id not in self.users:
                user = {
                    "id": user_id,
                    "email": azure_user["email"],
                    "password_hash": None,
                    "created_at": datetime.now().isoformat(),
                    "auth_provider": "azure",
                    "profile": {
                        "name": azure_user.get("name", azure_user["email"].split("@")[0]),
                        "avatar_url": None,
                        "settings": self._default_settings()
                    },
                    "stats": {
                        "conversations": 0,
                        "images_generated": 0,
                        "searches": 0
                    }
                }
                self.users[user_id] = user
            else:
                user = self.users[user_id]
                user["profile"]["name"] = azure_user.get("name", user["profile"]["name"])
            
            session = self._create_session(user_id)
            
            return {
                "success": True,
                "user": self._sanitize_user(self.users[user_id]),
                "session": session,
                "message": f"Welcome, {self.users[user_id]['profile']['name']}!"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Azure AD authentication failed: {str(e)}"
            }
    
    async def get_user(self, user_id: str) -> Dict:
        """Get user information"""
        if user_id not in self.users:
            return {"error": "User not found"}
        
        return self._sanitize_user(self.users[user_id])
    
    async def update_profile(self, user_id: str, updates: Dict) -> Dict:
        """Update user profile"""
        if user_id not in self.users:
            return {"success": False, "error": "User not found"}
        
        user = self.users[user_id]
        
        # Update allowed fields
        if "name" in updates:
            user["profile"]["name"] = updates["name"]
        if "avatar_url" in updates:
            user["profile"]["avatar_url"] = updates["avatar_url"]
        if "settings" in updates:
            user["profile"]["settings"].update(updates["settings"])
        
        return {
            "success": True,
            "user": self._sanitize_user(user)
        }
    
    async def logout(self, session_id: str) -> Dict:
        """Logout user"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return {"success": True, "message": "Logged out successfully"}
        return {"success": False, "error": "Session not found"}
    
    def verify_session(self, session_id: str) -> Optional[Dict]:
        """Verify session is valid"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Check expiry
        if datetime.fromisoformat(session["expires_at"]) < datetime.now():
            del self.sessions[session_id]
            return None
        
        return session
    
    # ==================== HELPER METHODS ====================
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _validate_password(self, password: str) -> Dict:
        """Validate password strength"""
        if len(password) < 8:
            return {"valid": False, "message": "Password must be at least 8 characters"}
        if not any(c.isupper() for c in password):
            return {"valid": False, "message": "Password must contain at least one uppercase letter"}
        if not any(c.islower() for c in password):
            return {"valid": False, "message": "Password must contain at least one lowercase letter"}
        if not any(c.isdigit() for c in password):
            return {"valid": False, "message": "Password must contain at least one number"}
        return {"valid": True, "message": "Password is strong"}
    
    def _hash_email(self, email: str) -> str:
        """Create consistent user ID from email"""
        return hashlib.sha256(email.lower().encode()).hexdigest()[:16]
    
    def _hash_password(self, password: str) -> str:
        """Hash password for storage"""
        # In production, use bcrypt or argon2
        salt = "quantum_salt_2024"
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    
    def _verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify password against stored hash"""
        return self._hash_password(password) == stored_hash
    
    def _create_session(self, user_id: str) -> Dict:
        """Create new session"""
        import secrets
        session_id = secrets.token_urlsafe(32)
        
        session = {
            "id": session_id,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=7)).isoformat()
        }
        
        self.sessions[session_id] = session
        return session
    
    def _default_settings(self) -> Dict:
        """Default user settings"""
        return {
            "theme": "dark",
            "language": "en",
            "notifications": True,
            "autonomous_mode": True,
            "search_depth": "basic",
            "image_quality": "high"
        }
    
    def _sanitize_user(self, user: Dict) -> Dict:
        """Remove sensitive data from user object"""
        return {
            "id": user["id"],
            "email": user["email"],
            "created_at": user["created_at"],
            "auth_provider": user["auth_provider"],
            "profile": user["profile"],
            "stats": user["stats"]
        }
    
    def _check_rate_limit(self, email: str) -> bool:
        """Check if login attempts are rate limited"""
        now = datetime.now()
        if email not in self.login_attempts:
            self.login_attempts[email] = []
        
        # Remove attempts older than 15 minutes
        self.login_attempts[email] = [
            t for t in self.login_attempts[email]
            if now - t < timedelta(minutes=15)
        ]
        
        # Allow max 5 attempts per 15 minutes
        return len(self.login_attempts[email]) < 5
    
    def _record_login_attempt(self, email: str):
        """Record failed login attempt"""
        self.login_attempts[email].append(datetime.now())
    
    async def _verify_google_token(self, token: str) -> Optional[Dict]:
        """Verify Google OAuth token"""
        # In production, verify with Google's token endpoint
        # For demo, simulate verification
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://www.googleapis.com/oauth2/v3/userinfo",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return response.json()
        except:
            pass
        
        # Fallback for demo
        return None
    
    async def _verify_azure_token(self, token: str) -> Optional[Dict]:
        """Verify Azure AD token"""
        # In production, verify with Azure AD token endpoint
        # For demo, simulate verification
        if self.azure_tenant_id:
            try:
                async with httpx.AsyncClient() as client:
                    # Verify token with Microsoft
                    response = await client.get(
                        f"https://graph.microsoft.com/oidc/userinfo",
                        headers={"Authorization": f"Bearer {token}"},
                        timeout=10.0
                    )
                    
                    if response.status_code == 200:
                        return response.json()
            except:
                pass
        
        # Fallback for demo
        return None
    
    def get_auth_providers(self) -> Dict:
        """Get available authentication providers"""
        return {
            "providers": [
                {
                    "id": "email",
                    "name": "Email",
                    "icon": "email",
                    "enabled": True
                },
                {
                    "id": "google",
                    "name": "Google",
                    "icon": "google",
                    "enabled": bool(self.google_client_id)
                },
                {
                    "id": "azure",
                    "name": "Azure AD",
                    "icon": "azure",
                    "enabled": bool(self.azure_client_id)
                }
            ],
            "oauth_urls": {
                "google": f"https://accounts.google.com/o/oauth2/v2/auth?client_id={self.google_client_id}&redirect_uri=...&response_type=code&scope=openid%20profile%20email" if self.google_client_id else None,
                "azure": f"https://login.microsoftonline.com/{self.azure_tenant_id}/oauth2/v2.0/authorize?client_id={self.azure_client_id}&..." if self.azure_client_id else None
            }
        }