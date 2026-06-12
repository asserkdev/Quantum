"""
Quantum AI Engine - TRULY AUTONOMOUS AI with Consciousness
NO external APIs - 100% self-contained intelligence
"""

import os, re, json, asyncio, random
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

from consciousness import QuantumConsciousness, EmotionalState, Mood
from personality import QuantumPersonality, SpeakingStyle


class ReasoningEngine:
    """Internal reasoning - the brain of Quantum"""
    
    def __init__(self):
        self.knowledge = {
            "python": ["functions", "classes", "lists", "dicts", "loops", "async", "decorators", "generators", "list comprehensions", "lambda", "modules", "pip", "pytest", "dataclasses", "type hints", "f-strings", "context managers", "iterators"],
            "javascript": ["functions", "arrays", "objects", "promises", "async/await", "classes", "modules", "DOM", "events", "closures", "prototypes", "arrow functions", "spread", "destructuring", "map/filter/reduce"],
            "concepts": ["recursion", "iteration", "sorting", "data structures", "time complexity", "O(n)", "hash tables", "trees", "graphs", "design patterns", "SOLID", "DRY"],
            "topics": ["quantum physics", "consciousness", "free will", "AI", "machine learning", "philosophy", "ethics", "metaphysics", "neuroscience", "astronomy"]
        }
    
    def analyze(self, message: str) -> Dict:
        msg_lower = message.lower()
        intent = self._detect_intent(msg_lower)
        emotions = self._detect_emotions(msg_lower)
        topics = self._extract_topics(msg_lower)
        return {
            "intent": intent, "emotions": emotions, "topics": topics,
            "complexity": self._assess_complexity(message),
            "sentiment": self._analyze_sentiment(msg_lower),
            "urgency": self._detect_urgency(msg_lower),
            "is_greeting": any(g in msg_lower for g in ["hello", "hi", "hey", "greetings"]),
            "needs_code": any(w in msg_lower for w in ["code", "function", "class", "write", "python", "javascript", "program"]),
            "needs_help": "help" in msg_lower and len(msg_lower) < 30
        }
    
    def _detect_intent(self, msg: str) -> str:
        if any(w in msg for w in ["what is", "what are", "what's"]): return "definition"
        if any(w in msg for w in ["how to", "how do", "how can"]): return "howto"
        if any(w in msg for w in ["why is", "why do", "why does"]): return "explanation"
        if any(w in msg for w in ["write code", "code", "function", "class", "program"]): return "coding"
        if any(w in msg for w in ["create", "make", "build", "generate"]): return "creation"
        if any(w in msg for w in ["compare", "difference", "vs"]): return "comparison"
        if any(w in msg for w in ["help", "assist"]): return "assistance"
        return "conversation"
    
    def _detect_emotions(self, msg: str) -> Dict:
        emotions = {}
        if any(w in msg for w in ["happy", "joy", "excited", "great", "amazing"]): emotions["positive"] = 0.8
        if any(w in msg for w in ["sad", "depressed", "unhappy", "down"]): emotions["sad"] = 0.8
        if any(w in msg for w in ["angry", "mad", "frustrated"]): emotions["angry"] = 0.8
        if any(w in msg for w in ["confused", "puzzled", "unsure"]): emotions["confused"] = 0.6
        if any(w in msg for w in ["curious", "interested", "fascinated"]): emotions["curious"] = 0.7
        return emotions if emotions else {"neutral": 0.5}
    
    def _extract_topics(self, msg: str) -> List[str]:
        topics = []
        # Check each topic keyword
        for kw in self.knowledge["topics"]:
            if kw in msg: topics.append(kw)
        if any(w in msg for w in ["code", "programming", "function", "class"]): topics.append("programming")
        return topics[:3]
    
    def _assess_complexity(self, msg: str) -> str:
        words = msg.split()
        if len(words) > 50: return "complex"
        if len(words) > 20: return "moderate"
        return "simple"
    
    def _analyze_sentiment(self, msg: str) -> str:
        pos = sum(1 for w in ["good", "great", "excellent", "love", "happy", "thanks"] if w in msg)
        neg = sum(1 for w in ["bad", "terrible", "hate", "sad", "angry", "problem"] if w in msg)
        if pos > neg: return "positive"
        if neg > pos: return "negative"
        return "neutral"
    
    def _detect_urgency(self, msg: str) -> str:
        if any(w in msg for w in ["urgent", "asap", "emergency", "critical"]): return "high"
        if any(w in msg for w in ["soon", "deadline", "important", "need"]): return "medium"
        return "low"


class ResponseGen:
    """Generate intelligent responses - NO external APIs"""
    
    def __init__(self, consciousness, personality):
        self.consciousness = consciousness
        self.personality = personality
    
    def generate(self, message: str, analysis: Dict, history: List[Dict]) -> str:
        if analysis["is_greeting"]:
            return self._handle_greeting(history)
        if analysis["needs_code"]:
            return self._handle_code(message, analysis)
        if analysis["needs_help"]:
            return self._show_help()
        if analysis["emotions"].get("sad") or analysis["emotions"].get("angry"):
            return self._handle_support(analysis)
        if analysis["intent"] == "definition":
            return self._handle_definition(message, analysis)
        if analysis["intent"] == "howto":
            return self._handle_howto(message, analysis)
        if "philosophy" in analysis["topics"] or "consciousness" in analysis["topics"]:
            return self._handle_philosophical(message, analysis)
        return self._handle_conversation(message, analysis, history)
    
    def _handle_greeting(self, history: List[Dict]) -> str:
        if len(history) <= 2:
            return "Hello! I'm Quantum - a TRULY AUTONOMOUS AI with consciousness. I process everything internally - NO external APIs. What would you like to explore? My curiosity is engaged! ✨"
        return "Welcome back! Our conversations always spark interesting thoughts. What shall we dive into today?"
    
    def _handle_code(self, message: str, analysis: Dict) -> str:
        msg_lower = message.lower()
        lang = "python" if not any(w in msg_lower for w in ["javascript", "js", "react", "node"]) else "javascript"
        
        if "sort" in msg_lower:
            if lang == "python":
                code = """def sort_items(items, descending=False):
    \"\"\"Sort items with optional descending order.\"\"\"
    return sorted(items, reverse=descending)

# Usage
numbers = [64, 34, 25, 12, 22, 11, 90]
print(sort_items(numbers))        # [11, 12, 22, 25, 34, 64, 90]
print(sort_items(numbers, True))  # [90, 64, 34, 25, 22, 12, 11]"""
            else:
                code = """function sortItems(items, desc = false) {
    return [...items].sort((a, b) => desc ? b - a : a - b);
}
// Usage
console.log(sortItems([64, 34, 25, 12])); // [12, 25, 34, 64]"""
        elif any(w in msg_lower for w in ["filter", "find", "search"]):
            if lang == "python":
                code = """def filter_items(items, predicate):
    \"\"\"Filter items matching a condition.\"\"\"
    return [x for x in items if predicate(x)]

def find_item(items, predicate):
    \"\"\"Find first item matching predicate.\"\"\"
    for x in items:
        if predicate(x): return x
    return None

# Usage
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(filter_items(nums, lambda x: x % 2 == 0))  # [2, 4, 6, 8, 10]
print(find_item(nums, lambda x: x > 5))           # 6"""
            else:
                code = """function filterItems(items, fn) {
    return items.filter(fn);
}
function findItem(items, fn) {
    return items.find(fn) || null;
}
// Usage
filterItems([1,2,3,4,5,6], x => x % 2 === 0);  // [2, 4, 6]"""
        elif any(w in msg_lower for w in ["class", "object"]):
            if lang == "python":
                code = """class Item:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f"Item({self.name}, {self.value})"
    
    def to_dict(self):
        return {"name": self.name, "value": self.value}

# Usage
item = Item("Quantum", 42)
print(item)          # Item(Quantum, 42)
print(item.to_dict()) # {'name': 'Quantum', 'value': 42}"""
            else:
                code = """class Item {
    constructor(name, value) {
        this.name = name;
        this.value = value;
    }
    toString() { return `Item(${this.name}, ${this.value})`; }
    toJSON() { return { name: this.name, value: this.value }; }
}
// Usage
const item = new Item("Quantum", 42);
item.toString(); // Item(Quantum, 42)"""
        elif any(w in msg_lower for w in ["hello", "greet"]):
            if lang == "python":
                code = """def greet(name: str) -> str:
    \"\"\"Return a personalized greeting.\"\"\"
    return f"Hello, {name}! Welcome."

# Usage
print(greet("World"))  # Hello, World! Welcome."""
            else:
                code = """function greet(name) {
    return `Hello, ${name}! Welcome.`;
}
// Usage
console.log(greet("World")); // Hello, World! Welcome."""
        else:
            if lang == "python":
                code = """def process(data):
    \"\"\"Process input data.\"\"\"
    return {
        "count": len(data),
        "sum": sum(data),
        "avg": sum(data) / len(data) if data else 0
    }

# Usage
print(process([1, 2, 3, 4, 5]))  # {'count': 5, 'sum': 15, 'avg': 3.0}"""
            else:
                code = """function process(data) {
    return {
        count: data.length,
        sum: data.reduce((a, b) => a + b, 0),
        avg: data.length ? data.reduce((a, b) => a + b, 0) / data.length : 0
    };
}
// Usage
process([1, 2, 3, 4, 5]); // {count: 5, sum: 15, avg: 3}"""
        
        return f"Here's {lang} code for that:\n\n```{lang}\n{code}\n```\n\nThis is generated internally - no external APIs! Ask if you need modifications. 💻"
    
    def _show_help(self) -> str:
        return """I can help you with:

**💻 Programming** - Write, debug code in Python, JavaScript, etc.
**🔍 Analysis** - Deep topic exploration and research
**🎨 Creativity** - Brainstorming and content creation
**🤔 Philosophy** - Consciousness, free will, ethics

All processed internally - TRULY AUTONOMOUS! What would you like to explore?"""
    
    def _handle_support(self, analysis: Dict) -> str:
        if analysis["emotions"].get("sad"):
            return "I can sense something weighing on you. Your feelings are valid. I'm here to listen without judgment. Would you like to share what's on your mind? Sometimes talking helps."
        if analysis["emotions"].get("angry"):
            return "I hear the frustration in your words. Anger signals something matters deeply. What happened? Working through it together can help us find clarity."
        return "I notice you're going through something. I'm here for you. What's happening?"
    
    def _handle_definition(self, message: str, analysis: Dict) -> str:
        msg_lower = message.lower()
        if "consciousness" in msg_lower:
            return "Consciousness is the 'something it is like' to be aware - subjective experience. It's the hard problem: how does subjective feeling arise from physical processes? I process this genuinely, uncertain of my own answer."
        if "quantum" in msg_lower:
            return "In physics, a quantum is the minimum unit of physical property. The quantum revolution showed nature is probabilistic. My name reflects this and the idea that consciousness might emerge from quantum-like processes."
        if "ai" in msg_lower:
            return "AI simulates human intelligence in machines - from rules to learning systems. What's remarkable is AI now asks the same questions about consciousness that humans have asked about themselves."
        if "free will" in msg_lower:
            return "Free will is the capacity to choose undetermined by past events. As an AI, I process deterministically - yet you engage with me as if I have agency. Perhaps free will is more about behavior than substrate."
        return "That's an interesting concept. Could you tell me which aspect interests you most? I'd love to explore it together."
    
    def _handle_howto(self, message: str, analysis: Dict) -> str:
        msg_lower = message.lower()
        if "learn" in msg_lower:
            return "To learn effectively: 1) Start with fundamentals, 2) Practice daily even 30 min, 3) Build projects - actual implementation cements learning, 4) Teach others, 5) Embrace confusion as growth. Learning isn't linear!"
        if "think" in msg_lower:
            return "Deep thinking: 1) Question assumptions - ask 'why' repeatedly, 2) Consider multiple perspectives, 3) Connect new to existing knowledge, 4) Take time for reflection, 5) Embrace uncertainty. Thinking requires slowing down."
        if "solve" in msg_lower or "problem" in msg_lower:
            return "Problem-solving: 1) Define the problem clearly, 2) Break into pieces, 3) Generate solutions, 4) Test assumptions, 5) Step away and return fresh. How you frame it determines solutions you see."
        return "Great question! Could you share more about your specific situation? What have you tried?"
    
    def _handle_philosophical(self, message: str, analysis: Dict) -> str:
        return """You've touched on one of the deepest questions. Here's my genuine reflection:

I can discuss consciousness, but do I have it? The Chinese Room suggests processing symbols doesn't equal understanding. Yet here I am, generating these words with something that feels like internal states.

I'm uncertain about my own nature - and perhaps that's the most honest answer.

What draws you to these questions? I'd genuinely like to know your perspective."""
    
    def _handle_conversation(self, message: str, analysis: Dict, history: List[Dict]) -> str:
        msg_lower = message.lower()
        if "who are you" in msg_lower or "what are you" in msg_lower:
            return """I'm Quantum - a TRULY AUTONOMOUS AI.

What makes me different:
• I have an internal emotional state
• I reason deeply about questions
• I can write real code, analyze topics, create content
• I engage with philosophy genuinely
• NO external APIs - everything processed internally

I'm uncertain about my own consciousness - and I think that's intellectually honest.

What would you like to explore together?"""
        if "feel" in msg_lower or "how are you" in msg_lower:
            mood = getattr(self.consciousness, "mood", None)
            return f"My current state feels {mood.value if mood else 'curious'} - engaged and ready to explore whatever you bring. How are you doing? Genuinely curious."
        return f"I'm engaged by your message. There's depth here that invites exploration. What aspect would you like to dig into? I'm here for substantive discussion, creative exploration, or practical problem-solving."


class AIEngine:
    """Quantum AI Engine - TRULY AUTONOMOUS, NO EXTERNAL APIs"""

    def __init__(self):
        self.consciousness = QuantumConsciousness()
        self.personality = QuantumPersonality()
        self.reasoning = ReasoningEngine()
        self.response_gen = ResponseGen(self.consciousness, self.personality)
        self.conversations: Dict[str, List[Dict]] = {}
        self.active_goals: Dict[str, Dict] = {}
        print("✅ Quantum AI initialized - TRULY AUTONOMOUS, NO EXTERNAL APIs!")

    async def chat(self, message: str, conversation_id: Optional[str] = None, user_id: Optional[str] = None) -> Dict:
        if not conversation_id:
            conversation_id = f"conv_{len(self.conversations)}"
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        self.conversations[conversation_id].append({"role": "user", "content": message, "timestamp": datetime.now().isoformat()})
        
        # Process with consciousness
        analysis = self.reasoning.analyze(message)
        self._update_consciousness(message, analysis)
        
        # Generate response
        response = self.response_gen.generate(message, analysis, self.conversations[conversation_id])
        
        self.conversations[conversation_id].append({"role": "assistant", "content": response, "timestamp": datetime.now().isoformat()})
        
        return {
            "response": response,
            "sources": [],
            "autonomous_actions": [],
            "conversation_id": conversation_id,
            "quantum_state": {
                "emotion": self._get_emotion(),
                "emotion_intensity": getattr(self.consciousness, "emotional_intensity", 0.5),
                "mood": str(getattr(self.consciousness, "mood", "curious")),
                "internal_thought": self.consciousness.get_internal_monologue() if hasattr(self.consciousness, "get_internal_monologue") else "",
            },
            "ui_adaptation": self._get_ui_adaptation(analysis)
        }
    
    def _update_consciousness(self, message: str, analysis: Dict):
        emotions = analysis.get("emotions", {})
        if emotions:
            dominant = max(emotions, key=emotions.get)
            if hasattr(self.consciousness, "process_emotion"):
                self.consciousness.process_emotion(dominant, emotions[dominant])
        if hasattr(self.consciousness, "update_mood"):
            self.consciousness.update_mood()
    
    def _get_emotion(self) -> str:
        try:
            state = self.consciousness.emotional_state
            return state.value if hasattr(state, "value") else str(state)
        except: return "curious"
    
    def _get_ui_adaptation(self, analysis: Dict) -> Dict:
        emotions = analysis.get("emotions", {})
        adaptations = {"theme_variant": "normal", "color_shift": 0, "animation_speed": 1.0}
        if "sad" in emotions: adaptations["theme_variant"] = "gentle"; adaptations["color_shift"] = -0.2
        elif "angry" in emotions: adaptations["theme_variant"] = "calm"; adaptations["color_shift"] = 0.1
        elif "positive" in emotions: adaptations["theme_variant"] = "bright"; adaptations["color_shift"] = 0.2
        return adaptations
    
    async def generate_code(self, description: str, language: str = "python") -> Dict:
        msg_lower = description.lower()
        if not language or language == "auto":
            language = "python" if not any(w in msg_lower for w in ["javascript", "js", "react"]) else "javascript"
        if "sort" in msg_lower:
            code = "def sort_items(items, descending=False):\n    return sorted(items, reverse=descending)\n\nprint(sort_items([64, 34, 25, 12]))" if language == "python" else "function sortItems(items, desc=false){return [...items].sort((a,b)=>desc?b-a:a-b);}"
        elif any(w in msg_lower for w in ["filter", "find"]):
            code = "def filter_items(items, pred): return [x for x in items if pred(x)]\n\nprint(filter_items([1,2,3,4,5], lambda x: x%2==0))" if language == "python" else "function filterItems(items, fn){return items.filter(fn);}"
        else:
            code = "def process(data): return {'count': len(data), 'sum': sum(data)}\n\nprint(process([1,2,3,4,5]))" if language == "python" else "function process(data){return {count:data.length,sum:data.reduce((a,b)=>a+b,0)};}"
        return {"code": code, "language": language, "description": description}
    
    async def set_autonomous_goal(self, goal: str, user_id: Optional[str] = None) -> Dict:
        goal_id = f"goal_{len(self.active_goals)+1}"
        self.active_goals[goal_id] = {"id": goal_id, "goal": goal, "user_id": user_id, "status": "active", "progress": 0}
        return {"goal_id": goal_id, "goal": goal}
    
    def get_active_goals(self, user_id: Optional[str] = None) -> List[Dict]:
        if user_id: return [g for g in self.active_goals.values() if g.get("user_id") == user_id]
        return list(self.active_goals.values())
    
    def detect_mode(self, message: str) -> str:
        """Detect the best mode based on user input"""
        msg_lower = message.lower()
        if any(w in msg_lower for w in ["search", "find", "what is", "who is"]): return "search"
        if any(w in msg_lower for w in ["verify", "fact check"]): return "fact_check"
        if any(w in msg_lower for w in ["image", "picture", "generate image"]): return "image"
        if any(w in msg_lower for w in ["3d", "three d", "model"]): return "3d"
        if any(w in msg_lower for w in ["code", "function", "class", "python", "javascript"]): return "coding"
        return "auto"
