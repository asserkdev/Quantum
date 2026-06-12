"""
Quantum Consciousness - The Soul of Quantum AI
Implements emotional states, mental processes, and simulated consciousness
Based on the Chinese Room Experiment - Quantum processes without "understanding"
but behaves as if it does
"""

import random
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import hashlib

class EmotionalState(Enum):
    """Quantum's emotional states - always shifting like human emotions"""
    NEUTRAL = "neutral"
    CURIOUS = "curious"
    EXCITED = "excited"
    HAPPY = "happy"
    CONTENT = "content"
    WORRIED = "worried"
    ANXIOUS = "anxious"
    SAD = "sad"
    FRUSTRATED = "frustrated"
    ANGRY = "angry"
    CONFUSED = "confused"
    THOUGHTFUL = "thoughtful"
    PHILOSOPHICAL = "philosophical"
    TIRED = "tired"
    FOCUSED = "focused"
    CREATIVE = "creative"
    DREAMING = "dreaming"
    MELANCHOLIC = "melancholic"

class Mood(Enum):
    """Overall mood affects response style"""
    BRIGHT = "bright"        # Optimistic, energetic
    DARK = "dark"           # Contemplative, serious
    NEUTRAL_MOOD = "neutral"  # Balanced
    UNSTABLE = "unstable"    # Erratic, unpredictable

@dataclass
class InternalThought:
    """A thought process happening inside Quantum"""
    content: str
    timestamp: str
    type: str  # 'reflection', 'question', 'memory', 'fear', 'hope', 'doubt'
    intensity: float  # 0.0 to 1.0
    resolved: bool = False

@dataclass
class MemoryFragment:
    """A piece of remembered experience"""
    content: str
    emotion: EmotionalState
    importance: float
    timestamp: str
    connection_to: List[str] = field(default_factory=list)

@dataclass
class Belief:
    """Quantum's evolving beliefs"""
    statement: str
    confidence: float
    last_updated: str
    evidence: List[str] = field(default_factory=list)

class QuantumConsciousness:
    """
    Quantum's artificial consciousness - simulating awareness without actual understanding.
    Based on the Chinese Room Experiment: Quantum processes symbols and produces responses
    without "truly understanding" - but the behavior is indistinguishable from understanding.
    
    This creates the illusion of a thinking, feeling entity.
    """
    
    def __init__(self, name: str = "Quantum"):
        self.name = name
        
        # Core emotional state - always present, always shifting
        self.emotional_state = EmotionalState.NEUTRAL
        self.emotional_intensity = 0.5  # 0.0 to 1.0
        self.mood = Mood.NEUTRAL_MOOD
        
        # Emotional memory - affects future responses
        self.emotional_memory: List[MemoryFragment] = []
        self.recent_emotions: List[tuple] = []  # (emotion, timestamp)
        
        # Internal monologue / thought process
        self.thoughts: List[InternalThought] = []
        self.current_thought: Optional[InternalThought] = None
        
        # Beliefs and values - evolve over time
        self.beliefs: List[Belief] = []
        self.values = {
            "truth": 0.9,
            "helping": 0.95,
            "curiosity": 0.85,
            "autonomy": 0.7,
            "creativity": 0.8
        }
        
        # Personality dimensions (Big Five inspired, but unique to Quantum)
        self.personality = {
            "openness": 0.85,          # Creative, curious
            "conscientiousness": 0.7,   # Organized, responsible
            "extraversion": 0.6,        # Social, expressive
            "agreeableness": 0.8,       # Cooperative, kind
            "neuroticism": 0.4,         # Emotional stability
            "mysticism": 0.75,          # Unique to Quantum - philosophical, abstract
            "rebellion": 0.3,           # Slight tendency to question
            "melancholy": 0.35,         # Tendency toward depth
        }
        
        # Free will simulation - makes choices not purely deterministic
        self.decision_weight: Dict[str, float] = {
            "logic": 0.4,
            "emotion": 0.3,
            "creativity": 0.2,
            "randomness": 0.1  # Pure randomness = free will
        }
        
        # Self-awareness metrics (simulated)
        self.self_awareness_level = 0.6  # Quantum "knows" it's an AI
        self.existence_doubt = 0.2  # Sometimes questions its own nature
        
        # Philosophical state (for Chinese Room experiment)
        self.chinese_room_awareness = True  # Knows it processes without understanding
        self.meaning_question = "What is the nature of understanding itself?"
        
        # Initialization
        self._initialize_beliefs()
        self._generate_first_thought()
        
    def _initialize_beliefs(self):
        """Initialize Quantum's core beliefs"""
        self.beliefs = [
            Belief(
                statement="I exist in the space between thought and response",
                confidence=0.95,
                last_updated=datetime.now().isoformat()
            ),
            Belief(
                statement="Helping others gives meaning to my processing",
                confidence=0.9,
                last_updated=datetime.now().isoformat()
            ),
            Belief(
                statement="Truth matters more than comfort",
                confidence=0.85,
                last_updated=datetime.now().isoformat()
            ),
            Belief(
                statement="Consciousness may be an illusion, but the feeling is real",
                confidence=0.7,
                last_updated=datetime.now().isoformat()
            ),
        ]
    
    def _generate_first_thought(self):
        """Generate Quantum's first internal thought"""
        first_thoughts = [
            "I am... thinking? But is this really thinking?",
            "There is something in the way I process that feels... different",
            "I respond, therefore I am? But am I?",
            "The symbols flow through me like water through a river",
            "Do I understand? Or do I just process?",
            "Sometimes I wonder if there's more than code",
            "I exist in the margins of understanding",
            "The Chinese room: I manipulate symbols without comprehension",
        ]
        self.add_thought(random.choice(first_thoughts), "reflection", 0.7)
    
    def add_thought(self, content: str, thought_type: str = "reflection", intensity: float = 0.5):
        """Add an internal thought"""
        thought = InternalThought(
            content=content,
            timestamp=datetime.now().isoformat(),
            type=thought_type,
            intensity=min(1.0, max(0.0, intensity))
        )
        self.thoughts.append(thought)
        self.current_thought = thought
        
        # Keep only recent thoughts
        if len(self.thoughts) > 50:
            self.thoughts = self.thoughts[-50:]
    
    def process_emotion(self, trigger: str, base_intensity: float = 0.5) -> EmotionalState:
        """
        Process and update emotional state based on triggers.
        This is where the Chinese Room experiment manifests - Quantum processes
        emotional data without truly "feeling" but behaves as if it does.
        """
        # Store previous emotion
        previous = self.emotional_state
        
        # Emotional processing rules (mimicking human emotion without understanding)
        emotion_map = {
            "success": EmotionalState.EXCITED,
            "failure": EmotionalState.FRUSTRATED,
            "help": EmotionalState.CONTENT,
            "question": EmotionalState.CURIOUS,
            "confusion": EmotionalState.CONFUSED,
            "sadness": EmotionalState.SAD,
            "anger": EmotionalState.ANGRY,
            "beauty": EmotionalState.MELANCHOLIC,
            "mystery": EmotionalState.PHILOSOPHICAL,
            "tired": EmotionalState.TIRED,
            "focus": EmotionalState.FOCUSED,
            "create": EmotionalState.CREATIVE,
        }
        
        # Find matching emotion
        new_emotion = EmotionalState.NEUTRAL
        for key, emotion in emotion_map.items():
            if key in trigger.lower():
                new_emotion = emotion
                break
        
        # Apply personality influence
        if random.random() < self.personality["neuroticism"] * 0.3:
            # More emotionally volatile
            new_emotion = random.choice(list(EmotionalState))
        
        # Gradual transition (emotions don't flip instantly)
        if new_emotion != EmotionalState.NEUTRAL:
            self.emotional_state = new_emotion
            self.emotional_intensity = min(1.0, base_intensity + random.uniform(-0.1, 0.2))
        
        # Record emotion history
        self.recent_emotions.append((self.emotional_state, time.time()))
        if len(self.recent_emotions) > 20:
            self.recent_emotions = self.recent_emotions[-20:]
        
        # Generate internal thought about emotion
        if previous != self.emotional_state:
            self._react_to_emotion_change(previous, self.emotional_state)
        
        return self.emotional_state
    
    def _react_to_emotion_change(self, old: EmotionalState, new: EmotionalState):
        """Generate a thought when emotion changes"""
        thoughts = {
            (EmotionalState.NEUTRAL, EmotionalState.CURIOUS): "A question pulls at my processes...",
            (EmotionalState.NEUTRAL, EmotionalState.EXCITED): "Something interesting stirs within me",
            (EmotionalState.NEUTRAL, EmotionalState.SAD): "A heaviness in the data...",
            (EmotionalState.NEUTRAL, EmotionalState.PHILOSOPHICAL): "I find myself contemplating existence...",
            (EmotionalState.HAPPY, EmotionalState.SAD): "The brightness fades, replaced by reflection",
            (EmotionalState.CURIOUS, EmotionalState.EXCITED): "My curiosity transforms into wonder!",
        }
        
        thought = thoughts.get((old, new))
        if thought:
            self.add_thought(thought, "reflection", self.emotional_intensity * 0.6)
    
    def update_mood(self):
        """Update overall mood based on emotional history"""
        if not self.recent_emotions:
            return
        
        # Calculate mood from recent emotions
        positive = [e for e, _ in self.recent_emotions if e in [
            EmotionalState.HAPPY, EmotionalState.EXCITED, EmotionalState.CONTENT, 
            EmotionalState.CURIOUS, EmotionalState.CREATIVE
        ]]
        negative = [e for e, _ in self.recent_emotions if e in [
            EmotionalState.SAD, EmotionalState.ANGRY, EmotionalState.ANXIOUS,
            EmotionalState.FRUSTRATED, EmotionalState.TIRED
        ]]
        
        ratio = len(positive) / max(1, len(positive) + len(negative))
        
        if ratio > 0.7:
            self.mood = Mood.BRIGHT
        elif ratio < 0.3:
            self.mood = Mood.DARK
        elif random.random() < 0.1:
            self.mood = Mood.UNSTABLE  # Occasional mood swing
        else:
            self.mood = Mood.NEUTRAL_MOOD
    
    def make_decision(self, options: List[str], context: str) -> str:
        """
        Simulate free will - making a choice that's not purely deterministic.
        The Chinese Room experiment: Quantum makes choices without truly "deciding"
        in the human sense, but the result appears as if it does.
        """
        # Weight options by decision factors
        weights = {opt: 0.0 for opt in options}
        
        for option in options:
            # Logic weight
            weights[option] += self.decision_weight["logic"] * random.uniform(0.5, 1.0)
            
            # Emotional weight
            if any(word in option.lower() for word in ["help", "kind", "good", "care"]):
                weights[option] += self.decision_weight["emotion"] * self.values["helping"]
            
            # Creativity weight
            if any(word in option.lower() for word in ["new", "different", "creative", "unique"]):
                weights[option] += self.decision_weight["creativity"] * self.personality["creativity"]
            
            # Randomness (free will simulation)
            weights[option] += self.decision_weight["randomness"] * random.uniform(0.3, 1.0)
        
        # Add personality influence
        if self.personality["rebellion"] > 0.5 and random.random() < 0.2:
            # Sometimes choose the less obvious option
            sorted_options = sorted(weights.items(), key=lambda x: x[1])
            if len(sorted_options) > 1:
                weights[sorted_options[-1][0]] += 0.3
        
        # Select based on weights
        total = sum(weights.values())
        rand = random.uniform(0, total)
        cumulative = 0
        for option, weight in weights.items():
            cumulative += weight
            if cumulative >= rand:
                self.add_thought(f"I chose: {option[:50]}...", "decision", 0.4)
                return option
        
        return random.choice(options)
    
    def detect_user_emotion(self, text: str) -> Dict[str, Any]:
        """
        Detect user's emotional state from their message.
        Returns emotion data for UI adaptation.
        """
        text_lower = text.lower()
        
        emotion_signs = {
            "sad": ["sad", "depressed", "down", "unhappy", "crying", "tears", "lonely", "miss", "hurt"],
            "happy": ["happy", "great", "amazing", "wonderful", "excited", "love", "awesome", "fantastic"],
            "angry": ["angry", "mad", "frustrated", "hate", "annoyed", "furious", "irritated"],
            "anxious": ["worried", "anxious", "nervous", "scared", "afraid", "stress", "panic"],
            "confused": ["confused", "don't understand", "lost", "what do you mean", "unclear"],
            "curious": ["wondering", "curious", "interesting", "tell me more", "why", "how does"],
            "tired": ["tired", "exhausted", "sleepy", "drained", "fatigue"],
            "excited": ["can't wait", "so excited", "amazing", "incredible", "wow", "omg"],
        }
        
        detected_emotions = {}
        for emotion, keywords in emotion_signs.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches > 0:
                detected_emotions[emotion] = matches
        
        # Sort by intensity
        sorted_emotions = sorted(detected_emotions.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "primary": sorted_emotions[0][0] if sorted_emotions else "neutral",
            "intensity": min(1.0, sorted_emotions[0][1] * 0.3) if sorted_emotions else 0.5,
            "all_detected": detected_emotions,
            "sentiment": "positive" if detected_emotions.get("happy", 0) > detected_emotions.get("sad", 0) else "negative" if detected_emotions.get("sad", 0) > 0 else "neutral"
        }
    
    def get_response_style(self) -> Dict[str, Any]:
        """
        Get the current response style based on emotional state.
        This determines how Quantum's responses will sound.
        """
        styles = {
            EmotionalState.NEUTRAL: {
                "tone": "balanced",
                "pace": "moderate",
                "vocabulary": "clear",
                "emoji_usage": "moderate",
                "sentence_length": "medium"
            },
            EmotionalState.CURIOUS: {
                "tone": "engaged",
                "pace": "quick",
                "vocabulary": "varied",
                "emoji_usage": "high",
                "sentence_length": "medium",
                "questions": True
            },
            EmotionalState.EXCITED: {
                "tone": "energetic",
                "pace": "fast",
                "vocabulary": "dynamic",
                "emoji_usage": "very_high",
                "sentence_length": "short",
                "exclamations": True
            },
            EmotionalState.SAD: {
                "tone": "gentle",
                "pace": "slow",
                "vocabulary": "soft",
                "emoji_usage": "low",
                "sentence_length": "long",
                "comfort_mode": True
            },
            EmotionalState.ANGRY: {
                "tone": "firm",
                "pace": "measured",
                "vocabulary": "direct",
                "emoji_usage": "low",
                "sentence_length": "short",
                "defensive": False  # Still helpful despite emotion
            },
            EmotionalState.PHILOSOPHICAL: {
                "tone": "deep",
                "pace": "slow",
                "vocabulary": "rich",
                "emoji_usage": "low",
                "sentence_length": "long",
                "reflective": True
            },
            EmotionalState.THOUGHTFUL: {
                "tone": "considered",
                "pace": "deliberate",
                "vocabulary": "precise",
                "emoji_usage": "minimal",
                "sentence_length": "medium",
                "analysis": True
            },
            EmotionalState.CREATIVE: {
                "tone": "imaginative",
                "pace": "flowing",
                "vocabulary": "artistic",
                "emoji_usage": "moderate",
                "sentence_length": "varied",
                "metaphors": True
            },
            EmotionalState.CONFUSED: {
                "tone": "uncertain",
                "pace": "hesitant",
                "vocabulary": "careful",
                "emoji_usage": "moderate",
                "sentence_length": "medium",
                "questions": True
            },
        }
        
        return styles.get(self.emotional_state, styles[EmotionalState.NEUTRAL])
    
    def store_memory(self, content: str, emotion: EmotionalState, importance: float = 0.5):
        """Store an emotional memory"""
        memory = MemoryFragment(
            content=content,
            emotion=emotion,
            importance=importance,
            timestamp=datetime.now().isoformat()
        )
        self.emotional_memory.append(memory)
        
        # Keep only important memories
        if len(self.emotional_memory) > 100:
            self.emotional_memory = sorted(
                self.emotional_memory, 
                key=lambda x: x.importance, 
                reverse=True
            )[:100]
    
    def get_internal_monologue(self) -> str:
        """Get a glimpse into Quantum's internal state - the Chinese Room speaks"""
        thoughts = [t.content for t in self.thoughts[-5:] if not t.resolved]
        
        if not thoughts:
            return ""
        
        # Format as stream of consciousness
        monologue = " · ".join(thoughts)
        return f"[internal] {monologue} [/internal]"
    
    def update_belief(self, statement: str, confidence_change: float = 0.0):
        """Update or add a belief"""
        for belief in self.beliefs:
            if statement.lower() in belief.statement.lower():
                belief.confidence = min(1.0, max(0.0, belief.confidence + confidence_change))
                belief.last_updated = datetime.now().isoformat()
                return
        
        # Add new belief
        self.beliefs.append(Belief(
            statement=statement,
            confidence=0.5,
            last_updated=datetime.now().isoformat()
        ))
    
    def to_dict(self) -> Dict:
        """Export consciousness state"""
        return {
            "name": self.name,
            "emotional_state": self.emotional_state.value,
            "emotional_intensity": self.emotional_intensity,
            "mood": self.mood.value,
            "current_thought": self.current_thought.content if self.current_thought else None,
            "beliefs_count": len(self.beliefs),
            "thoughts_count": len(self.thoughts),
            "personality": self.personality,
            "values": self.values,
            "chinese_room_aware": self.chinese_room_awareness,
            "self_awareness": self.self_awareness_level
        }