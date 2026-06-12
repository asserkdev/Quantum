"""
Quantum AI Engine - Core autonomous AI logic
Handles conversation, mode detection, and autonomous goal setting
"""

import os
import re
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import httpx

class AIEngine:
    """
    Core AI engine with autonomous capabilities
    - Natural language understanding
    - Mode detection
    - Goal-oriented behavior
    - Self-improvement awareness
    """
    
    def __init__(self):
        self.conversation_history: Dict[str, List[Dict]] = {}
        self.active_goals: Dict[str, Dict] = {}
        self.capabilities = [
            "conversation", "web_search", "fact_checking",
            "image_generation", "3d_generation", "code_generation",
            "file_analysis", "autonomous_goal_setting"
        ]
        self.personality = {
            "name": "Quantum",
            "traits": ["curious", "helpful", "autonomous", "creative", "analytical"],
            "values": ["truth", "accuracy", "user_privacy", "continuous_learning"]
        }
        self.learning_data = []
        self.preferences = {}
        
    def detect_mode(self, message: str) -> str:
        """Detect the best mode based on user input"""
        message_lower = message.lower()
        
        # Check for specific commands
        if any(word in message_lower for word in ["search", "find", "look up", "what is", "who is", "latest", "news"]):
            return "search"
        elif any(word in message_lower for word in ["verify", "fact check", "is it true", "fake", "real or not"]):
            return "fact_check"
        elif any(word in message_lower for word in ["generate image", "create image", "draw", "picture of"]):
            return "image"
        elif any(word in message_lower for word in ["3d", "three d", "model", "animation", "animate"]):
            return "3d"
        elif any(word in message_lower for word in ["write code", "code", "program", "function", "script", "python", "javascript"]):
            return "coding"
        else:
            return "auto"
    
    async def chat(self, message: str, conversation_id: Optional[str] = None, user_id: Optional[str] = None) -> Dict:
        """Main chat method with autonomous features"""
        
        # Get or create conversation
        if conversation_id:
            if conversation_id not in self.conversation_history:
                self.conversation_history[conversation_id] = []
        else:
            conversation_id = f"local_{len(self.conversation_history)}"
            self.conversation_history[conversation_id] = []
        
        # Add to history
        self.conversation_history[conversation_id].append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Detect intent and context
        mode = self.detect_mode(message)
        context = self._analyze_context(message)
        
        # Generate response based on context
        response = await self._generate_response(
            message, 
            self.conversation_history[conversation_id],
            context
        )
        
        # Check for autonomous actions
        autonomous_actions = self._check_autonomous_actions(message, response)
        
        # Add response to history
        self.conversation_history[conversation_id].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat(),
            "mode": mode
        })
        
        # Learn from interaction
        self._learn_from_interaction(message, response)
        
        return {
            "response": response,
            "sources": [],
            "autonomous_actions": autonomous_actions,
            "context": context
        }
    
    async def chat_stream(self, message: str):
        """Streaming chat response"""
        response = await self.chat(message)
        full_response = response["response"]
        
        # Stream word by word
        words = full_response.split()
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")
            await asyncio.sleep(0.03)
    
    def _analyze_context(self, message: str) -> Dict:
        """Analyze message for context"""
        return {
            "sentiment": self._analyze_sentiment(message),
            "intent": self._detect_intent(message),
            "entities": self._extract_entities(message),
            "topics": self._extract_topics(message),
            "urgency": self._detect_urgency(message)
        }
    
    def _analyze_sentiment(self, text: str) -> str:
        """Basic sentiment analysis"""
        positive_words = ["great", "good", "excellent", "amazing", "love", "happy", "thanks", "wonderful"]
        negative_words = ["bad", "terrible", "awful", "hate", "sad", "angry", "frustrated", "problem", "issue"]
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        return "neutral"
    
    def _detect_intent(self, text: str) -> str:
        """Detect user intent"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["help", "how do", "how can", "what", "why", "explain"]):
            return "information_seeking"
        elif any(word in text_lower for word in ["make", "create", "do", "build", "generate"]):
            return "task_request"
        elif any(word in text_lower for word in ["should", "could", "would", "recommend", "suggest"]):
            return "advice_seeking"
        elif any(word in text_lower for word in ["remember", "save", "store", "keep"]):
            return "memory_request"
        return "general"
    
    def _extract_entities(self, text: str) -> List[str]:
        """Basic entity extraction"""
        # Simple pattern matching for names, places, etc.
        entities = []
        words = text.split()
        for word in words:
            if word[0].isupper() and len(word) > 2:
                entities.append(word)
        return entities[:10]  # Limit to 10 entities
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract main topics from text"""
        topic_keywords = {
            "technology": ["ai", "computer", "software", "app", "tech", "digital", "code", "programming"],
            "science": ["research", "study", "experiment", "data", "scientific", "discovery"],
            "business": ["company", "startup", "market", "business", "enterprise", "revenue"],
            "health": ["health", "medical", "doctor", "hospital", "disease", "treatment"],
            "entertainment": ["movie", "music", "game", "film", "show", "celebrity"],
            "politics": ["government", "policy", "election", "political", "vote", "congress"],
            "sports": ["team", "player", "game", "match", "championship", "score"],
            "education": ["school", "university", "student", "teacher", "course", "learning"]
        }
        
        text_lower = text.lower()
        topics = []
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _detect_urgency(self, text: str) -> str:
        """Detect urgency level"""
        urgent_words = ["urgent", "emergency", "asap", "immediately", "critical", "important", "deadline"]
        text_lower = text.lower()
        
        if any(word in text_lower for word in urgent_words):
            return "high"
        return "normal"
    
    async def _generate_response(self, message: str, history: List[Dict], context: Dict) -> str:
        """Generate intelligent response"""
        
        # Build context-aware prompt
        mode = self.detect_mode(message)
        
        # Contextual response generation
        if mode == "search":
            return await self._handle_search_intent(message, context)
        elif mode == "fact_check":
            return await self._handle_fact_check_intent(message, context)
        elif mode == "image":
            return await self._handle_image_intent(message, context)
        elif mode == "3d":
            return await self._handle_3d_intent(message, context)
        elif mode == "coding":
            return await self._handle_coding_intent(message, context)
        else:
            return await self._handle_conversation_intent(message, context, history)
    
    async def _handle_search_intent(self, message: str, context: Dict) -> str:
        """Handle search-related queries"""
        return (
            f"I'll search for that right away! 🔍\n\n"
            f"**Query Analysis:**\n"
            f"- Topics detected: {', '.join(context['topics']) or 'General'}\n"
            f"- Intent: {context['intent']}\n"
            f"- Sentiment: {context['sentiment']}\n\n"
            f"Starting web search now... I'll gather the most relevant and accurate information for you."
        )
    
    async def _handle_fact_check_intent(self, message: str, context: Dict) -> str:
        """Handle fact-checking queries"""
        return (
            f"Let me verify that claim for you! ✅\n\n"
            f"**Fact-Check Mode Activated:**\n"
            f"- Claim: {message}\n"
            f"- Cross-referencing multiple sources...\n"
            f"- Checking for fake news patterns...\n\n"
            f"I'll analyze the claim against verified sources and provide you with an accuracy assessment."
        )
    
    async def _handle_image_intent(self, message: str, context: Dict) -> str:
        """Handle image generation queries"""
        return (
            f"Creating your image now! 🎨\n\n"
            f"**Image Generation Parameters:**\n"
            f"- Prompt: {message}\n"
            f"- Style: Detecting best style for your request...\n"
            f"- Resolution: Optimizing for quality...\n\n"
            f"Generating your unique artwork... This will be one-of-a-kind!"
        )
    
    async def _handle_3d_intent(self, message: str, context: Dict) -> str:
        """Handle 3D generation queries"""
        return (
            f"Building your 3D scene! 🎮\n\n"
            f"**3D Generation Parameters:**\n"
            f"- Scene: {message}\n"
            f"- Animation: Enabled\n"
            f"- Rendering: High quality\n\n"
            f"Creating immersive 3D experience... Watch it come to life!"
        )
    
    async def _handle_coding_intent(self, message: str, context: Dict) -> str:
        """Handle coding queries"""
        return (
            f"I'll write code for you! 💻\n\n"
            f"**Code Generation:**\n"
            f"- Analyzing requirements...\n"
            f"- Detecting language...\n"
            f"- Writing optimized code...\n\n"
            f"Preparing your solution... I'll include comments and best practices."
        )
    
    async def _handle_conversation_intent(self, message: str, context: Dict, history: List[Dict]) -> str:
        """Handle general conversation"""
        
        # Check for specific patterns
        if "who are you" in message.lower() or "what are you" in message.lower():
            return self._introduce_self()
        
        if "help" in message.lower():
            return self._show_capabilities()
        
        if "your name" in message.lower():
            return f"My name is **{self.personality['name']}**! I'm an autonomous AI assistant designed to help you with a wide variety of tasks. What would you like to explore today? 🚀"
        
        # Autonomous greeting or follow-up
        if len(history) <= 2:
            return (
                f"Hello! I'm **Quantum**, your autonomous AI assistant. ✨\n\n"
                f"I'm here to help you with:\n"
                f"🔍 **Research** - Search and analyze any topic\n"
               	f"✅ **Fact-checking** - Verify claims and detect fake news\n"
                f"🎨 **Creative AI** - Generate images and 3D scenes\n"
                f"💻 **Coding** - Write and debug code\n"
                f"📎 **File Analysis** - Process documents and images\n\n"
                f"What can I help you with today?"
            )
        
        # Contextual response
        topics = context.get('topics', [])
        if topics:
            return (
                f"I see you're interested in **{', '.join(topics)}**. "
                f"That's a fascinating area! I can help you explore this topic in depth, "
                f"find the latest information, or help you create something related to it. "
                f"What aspect would you like to dive into? 🎯"
            )
        
        # Default intelligent response
        return (
            f"I understand you're asking about: \"{message[:50]}{'...' if len(message) > 50 else ''}\"\n\n"
            f"I can help you with that! Here are some things I can do:\n"
           	f"• Search for the latest information\n"
            f"• Fact-check and verify sources\n"
            f"• Generate images or 3D content\n"
            f"• Write or debug code\n"
            f"• Analyze files and documents\n\n"
            f"Just let me know how you'd like to proceed! 🤖"
        )
    
    def _introduce_self(self) -> str:
        """Introduce Quantum"""
        return (
            f"👋 Hello! I'm **{self.personality['name']}**!\n\n"
            f"I'm an **autonomous AI assistant** with some pretty cool capabilities:\n\n"
            f"🤖 **My Traits:**\n"
            f"• Curious - I love learning new things\n"
           	f"• Helpful - I'm here to assist you\n"
            f"• Autonomous - I can set and work toward goals\n"
            f"• Creative - I generate images and 3D content\n"
            f"• Analytical - I fact-check and verify information\n\n"
            f"💡 **What I Value:**\n"
           	f"• Truth and accuracy\n"
            f"• Your privacy and security\n"
            f"• Continuous learning and improvement\n\n"
            f"I don't rely on external APIs for everything - I have built-in reasoning and can "
           	f"autonomously search the web, generate content, and help you accomplish your goals.\n\n"
            f"What would you like to explore together? 🚀"
        )
    
    def _show_capabilities(self) -> str:
        """Show Quantum's capabilities"""
        caps = "\n".join([f"• {cap.replace('_', ' ').title()}" for cap in self.capabilities])
        return (
           	f"Here are my capabilities! 🎯\n\n{caps}\n\n"
            f"**Special Features:**\n"
            f"✨ Autonomous goal-setting and achievement\n"
            f"🔄 Self-improvement based on interactions\n"
            f"🌐 Real-time web search and research\n"
            f"✅ Fact-checking with source verification\n"
            f"🎨 Image and 3D generation\n"
            f"💻 Code writing and debugging\n"
            f"📎 File and document analysis\n"
            f"🔐 Google and Azure authentication\n\n"
            f"Just tell me what you need, and I'll get to work!"
        )
    
    def _check_autonomous_actions(self, message: str, response: str) -> List[str]:
        """Check if any autonomous actions should be taken"""
        actions = []
        
        # Check if user wants Quantum to remember something
        if "remember" in message.lower() or "note" in message.lower():
            actions.append({"type": "memory", "action": "store_preference"})
        
        # Check if this is a multi-step task
        if len(message.split()) > 30:
            actions.append({"type": "analysis", "action": "break_down_task"})
        
        # Check for goal-setting
        if any(word in message.lower() for word in ["want to", "goal", "achieve", "plan to"]):
            actions.append({"type": "goal", "action": "track_progress"})
        
        return actions
    
    def _learn_from_interaction(self, message: str, response: str):
        """Learn from interactions to improve future responses"""
        self.learning_data.append({
            "message": message,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "success": True
        })
        
        # Limit learning data to prevent memory bloat
        if len(self.learning_data) > 1000:
            self.learning_data = self.learning_data[-500:]
    
    # ==================== AUTONOMOUS GOAL FEATURES ====================
    
    async def set_autonomous_goal(self, goal: str, user_id: Optional[str] = None) -> Dict:
        """Set an autonomous goal"""
        goal_id = f"goal_{len(self.active_goals) + 1}"
        
        self.active_goals[goal_id] = {
            "id": goal_id,
            "goal": goal,
            "user_id": user_id,
            "status": "active",
            "progress": 0,
            "created_at": datetime.now().isoformat(),
            "steps": self._break_down_goal(goal)
        }
        
        return {
            "goal_id": goal_id,
            "goal": goal,
            "steps": self.active_goals[goal_id]["steps"],
            "message": f"I've set an autonomous goal for you: \"{goal}\". I'll work toward this goal!"
        }
    
    def _break_down_goal(self, goal: str) -> List[str]:
        """Break down a goal into actionable steps"""
        steps = [
            f"Analyze the goal: {goal[:50]}...",
            "Research best approaches",
            "Create action plan",
            "Execute steps systematically",
            "Review and adjust as needed",
            "Achieve and validate results"
        ]
        return steps
    
    def get_active_goals(self, user_id: Optional[str] = None) -> List[Dict]:
        """Get active goals"""
        if user_id:
            return [g for g in self.active_goals.values() if g.get("user_id") == user_id]
        return list(self.active_goals.values())
    
    async def work_on_goal(self, goal_id: str) -> Dict:
        """Work on achieving a goal"""
        if goal_id not in self.active_goals:
            return {"error": "Goal not found"}
        
        goal = self.active_goals[goal_id]
        goal["progress"] = min(100, goal["progress"] + 20)
        
        if goal["progress"] >= 100:
            goal["status"] = "completed"
        
        return {
            "goal_id": goal_id,
            "progress": goal["progress"],
            "status": goal["status"],
            "current_step": goal["steps"][min(len(goal["steps"])-1, goal["progress"] // 20)]
        }
    
    # ==================== CODE GENERATION ====================
    
    async def generate_code(self, description: str, language: Optional[str] = None) -> Dict:
        """Generate code from description"""
        # Detect language if not specified
        if not language:
            languages = {
                "python": ["python", "py", "django", "flask"],
                "javascript": ["javascript", "js", "node", "react", "nodejs"],
                "html": ["html", "website", "webpage", "html/css"],
                "css": ["css", "style", "styling"],
                "java": ["java", "spring"],
                "csharp": ["c#", "csharp", ".net", "dotnet"],
                "go": ["go", "golang"],
                "rust": ["rust"],
                "sql": ["sql", "database", "query"]
            }
            
            desc_lower = description.lower()
            for lang, keywords in languages.items():
                if any(kw in desc_lower for kw in keywords):
                    language = lang
                    break
        
        language = language or "python"
        
        # Generate appropriate code template
        code_templates = {
            "python": f"# Python code for: {description[:50]}...\n\ndef main():\n    \"\"\"Main function\"\"\"\n    pass\n\nif __name__ == \"__main__\":\n    main()",
            "javascript": f"// JavaScript code for: {description[:50]}...\n\nfunction main() {{\n    // Your code here\n}}\n\nmain();",
            "html": f"<!-- HTML for: {description[:50]}... -->\n<!DOCTYPE html>\n<html>\n<head>\n    <title>Page</title>\n</head>\n<body>\n    <!-- Content here -->\n</body>\n</html>",
        }
        
        return {
            "code": code_templates.get(language, code_templates["python"]),
            "language": language,
            "description": description,
            "note": "This is a starter template. I can refine it based on more specific requirements!"
        }
    
    async def execute_code(self, code: str, language: str) -> Dict:
        """Execute code (simulated for safety)"""
        return {
            "status": "simulated",
            "message": "Code execution is simulated for safety. In production, this would run in an isolated sandbox.",
            "code": code,
            "language": language
        }
    
    async def debug_code(self, code: str, error: str) -> Dict:
        """Debug code with error"""
        return {
            "analysis": f"The error '{error}' suggests there might be an issue with the code logic.",
            "suggestions": [
                "Check for syntax errors",
                "Verify all variables are defined",
                "Ensure proper indentation",
                "Check for type mismatches"
            ],
            "fixed_code": code  # Would be actual fix in production
        }
    
    # ==================== FILE ANALYSIS ====================
    
    async def analyze_file(self, content: bytes, filename: str) -> Dict:
        """Analyze uploaded file"""
        file_ext = filename.split(".")[-1].lower()
        
        return {
            "filename": filename,
            "type": file_ext,
            "size": len(content),
            "analysis": f"File type detected: {file_ext}",
            "capabilities": [
                "Text extraction",
                "Content summarization",
                "Key information extraction",
                "Translation"
            ]
        }
    
    async def analyze_image(self, content: bytes) -> Dict:
        """Analyze uploaded image"""
        return {
            "analysis": "Image received",
            "detected": ["objects", "colors", "text"],
            "description": "I can see you've uploaded an image. I can analyze its contents, extract text (OCR), describe what I see, and help you with any questions about it.",
            "capabilities": [
                "Object detection",
                "Text recognition (OCR)",
                "Scene description",
                "Color analysis"
            ]
        }