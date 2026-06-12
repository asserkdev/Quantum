"""
Quantum Models - Data models for conversations and interactions
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ConversationMode(str, Enum):
    AUTO = "auto"
    SEARCH = "search"
    FACT_CHECK = "fact_check"
    IMAGE = "image"
    THREE_D = "3d"
    CODING = "coding"

@dataclass
class Message:
    """Chat message model"""
    role: MessageRole
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    mode: Optional[ConversationMode] = None
    sources: List[Dict[str, str]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp,
            "mode": self.mode.value if self.mode else None,
            "sources": self.sources,
            "metadata": self.metadata
        }

@dataclass
class Conversation:
    """Conversation model"""
    id: str
    user_id: Optional[str] = None
    messages: List[Message] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_message(self, message: Message):
        self.messages.append(message)
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "messages": [m.to_dict() for m in self.messages],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata
        }

@dataclass
class User:
    """User model"""
    id: str
    email: str
    name: str
    avatar_url: Optional[str] = None
    auth_provider: str = "email"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    settings: Dict[str, Any] = field(default_factory=lambda: {
        "theme": "dark",
        "language": "en",
        "notifications": True,
        "autonomous_mode": True
    })
    stats: Dict[str, int] = field(default_factory=lambda: {
        "conversations": 0,
        "images_generated": 0,
        "searches": 0
    })

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "avatar_url": self.avatar_url,
            "auth_provider": self.auth_provider,
            "created_at": self.created_at,
            "settings": self.settings,
            "stats": self.stats
        }

@dataclass
class Goal:
    """Autonomous goal model"""
    id: str
    goal: str
    user_id: Optional[str] = None
    status: str = "active"
    progress: int = 0
    steps: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None

    def update_progress(self, progress: int):
        self.progress = min(100, max(0, progress))
        if self.progress >= 100:
            self.status = "completed"
            self.completed_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "goal": self.goal,
            "user_id": self.user_id,
            "status": self.status,
            "progress": self.progress,
            "steps": self.steps,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }

@dataclass
class SearchResult:
    """Search result model"""
    title: str
    url: str
    content: str
    score: float = 0.0
    source: Optional[str] = None
    published_date: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "url": self.url,
            "content": self.content,
            "score": self.score,
            "source": self.source,
            "published_date": self.published_date
        }

@dataclass
class FactCheckResult:
    """Fact check result model"""
    claim: str
    verdict: str
    confidence: float = 0.0
    explanation: str = ""
    sources: List[Dict] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "claim": self.claim,
            "verdict": self.verdict,
            "confidence": self.confidence,
            "explanation": self.explanation,
            "sources": self.sources,
            "recommendations": self.recommendations
        }

@dataclass
class GeneratedImage:
    """Generated image model"""
    id: str
    prompt: str
    style: str
    size: str
    status: str = "pending"
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "prompt": self.prompt,
            "style": self.style,
            "size": self.size,
            "status": self.status,
            "image_url": self.image_url,
            "thumbnail_url": self.thumbnail_url,
            "created_at": self.created_at,
            "metadata": self.metadata
        }

@dataclass
class Scene3D:
    """3D scene model"""
    id: str
    prompt: str
    scene_config: Dict[str, Any]
    status: str = "pending"
    model_url: Optional[str] = None
    preview_url: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "prompt": self.prompt,
            "scene_config": self.scene_config,
            "status": self.status,
            "model_url": self.model_url,
            "preview_url": self.preview_url,
            "created_at": self.created_at
        }