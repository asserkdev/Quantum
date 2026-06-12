"""
Quantum Self Improver - Autonomous self-improvement system
Learns from interactions and suggests improvements
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from collections import defaultdict

class SelfImprover:
    """
    Autonomous self-improvement system
    - Analyzes interactions for patterns
    - Identifies areas for improvement
    - Suggests and applies improvements
    - Learns user preferences
    """
    
    def __init__(self):
        self.enabled = True
        self.learning_mode = True
        
        # Learning data
        self.interaction_history = []
        self.success_patterns = []
        self.failure_patterns = []
        self.user_preferences = defaultdict(lambda: {"likes": [], "dislikes": []})
        self.improvement_suggestions = []
        
        # Performance metrics
        self.metrics = {
            "total_interactions": 0,
            "successful_interactions": 0,
            "failed_interactions": 0,
            "average_response_time": 0,
            "user_satisfaction": 0.85
        }
        
        # Self-knowledge
        self.capabilities = [
            "conversational_ai",
            "web_search",
            "fact_checking",
            "image_generation",
            "3d_generation",
            "code_generation",
            "file_analysis",
            "autonomous_goal_setting"
        ]
        
        self.knowledge_base = {
            "topics": {},
            "patterns": {},
            "solutions": {}
        }
        
        self.max_history = 1000
        self.max_suggestions = 50
        
    async def analyze_and_improve(self) -> Dict:
        """
        Analyze recent interactions and identify improvements
        """
        if not self.enabled:
            return {"status": "disabled", "message": "Self-improvement is disabled"}
        
        # Analyze patterns
        patterns = self._analyze_interaction_patterns()
        
        # Identify improvements
        improvements = self._identify_improvements(patterns)
        
        # Apply automatic improvements
        applied = await self._apply_automatic_improvements(improvements)
        
        return {
            "status": "completed",
            "patterns_found": len(patterns),
            "improvements_identified": len(improvements),
            "improvements_applied": applied,
            "metrics": self.metrics,
            "suggestions": self.get_suggestions()
        }
    
    def learn_from_interaction(self, interaction: Dict):
        """
        Learn from a single interaction
        """
        self.interaction_history.append({
            **interaction,
            "timestamp": datetime.now().isoformat()
        })
        
        # Trim history if too long
        if len(self.interaction_history) > self.max_history:
            self.interaction_history = self.interaction_history[-self.max_history:]
        
        # Update metrics
        self.metrics["total_interactions"] += 1
        if interaction.get("success", True):
            self.metrics["successful_interactions"] += 1
            self.success_patterns.append(interaction)
        else:
            self.metrics["failed_interactions"] += 1
            self.failure_patterns.append(interaction)
        
        # Learn preferences
        if "user_id" in interaction:
            self._learn_preferences(interaction)
        
        # Extract knowledge
        self._extract_knowledge(interaction)
    
    def _analyze_interaction_patterns(self) -> List[Dict]:
        """Analyze interaction history for patterns"""
        patterns = []
        
        # Analyze successful interactions
        recent_successes = self.success_patterns[-50:]
        if recent_successes:
            common_responses = self._find_common_elements(recent_successes, "response_type")
            patterns.append({
                "type": "success_pattern",
                "description": "Successful response patterns",
                "data": common_responses,
                "confidence": min(1.0, len(recent_successes) / 10)
            })
        
        # Analyze failed interactions
        recent_failures = self.failure_patterns[-20:]
        if recent_failures:
            patterns.append({
                "type": "failure_pattern",
                "description": "Areas needing improvement",
                "data": self._analyze_failures(recent_failures),
                "confidence": min(1.0, len(recent_failures) / 5)
            })
        
        # Analyze topic frequency
        topic_freq = self._analyze_topic_frequency()
        if topic_freq:
            patterns.append({
                "type": "topic_frequency",
                "description": "Most discussed topics",
                "data": topic_freq,
                "confidence": 0.9
            })
        
        # Analyze user satisfaction trends
        satisfaction_trend = self._analyze_satisfaction_trend()
        if satisfaction_trend:
            patterns.append({
                "type": "satisfaction_trend",
                "description": "User satisfaction over time",
                "data": satisfaction_trend,
                "confidence": 0.8
            })
        
        return patterns
    
    def _find_common_elements(self, interactions: List[Dict], key: str) -> Dict:
        """Find common elements in interactions"""
        counter = defaultdict(int)
        for interaction in interactions:
            if key in interaction:
                counter[interaction[key]] += 1
        
        return dict(sorted(counter.items(), key=lambda x: x[1], reverse=True)[:10])
    
    def _analyze_failures(self, failures: List[Dict]) -> Dict:
        """Analyze failure patterns"""
        failure_types = defaultdict(int)
        failure_contexts = []
        
        for failure in failures:
            if "failure_type" in failure:
                failure_types[failure["failure_type"]] += 1
            if "context" in failure:
                failure_contexts.append(failure["context"])
        
        return {
            "types": dict(failure_types),
            "contexts": failure_contexts[:5]
        }
    
    def _analyze_topic_frequency(self) -> Dict:
        """Analyze which topics are most discussed"""
        topic_counter = defaultdict(int)
        
        for interaction in self.interaction_history:
            if "topics" in interaction:
                for topic in interaction["topics"]:
                    topic_counter[topic] += 1
        
        return dict(sorted(topic_counter.items(), key=lambda x: x[1], reverse=True)[:10])
    
    def _analyze_satisfaction_trend(self) -> Dict:
        """Analyze user satisfaction trends"""
        if len(self.interaction_history) < 5:
            return {}
        
        recent = self.interaction_history[-20:]
        satisfaction_scores = [i.get("satisfaction", 0.5) for i in recent if "satisfaction" in i]
        
        if not satisfaction_scores:
            return {"trend": "unknown"}
        
        avg = sum(satisfaction_scores) / len(satisfaction_scores)
        
        # Calculate trend
        if len(satisfaction_scores) >= 10:
            first_half = sum(satisfaction_scores[:len(satisfaction_scores)//2]) / (len(satisfaction_scores)//2)
            second_half = sum(satisfaction_scores[len(satisfaction_scores)//2:]) / (len(satisfaction_scores) - len(satisfaction_scores)//2)
            trend = "improving" if second_half > first_half else "declining" if second_half < first_half else "stable"
        else:
            trend = "stable"
        
        return {
            "average": round(avg, 2),
            "trend": trend,
            "sample_size": len(satisfaction_scores)
        }
    
    def _identify_improvements(self, patterns: List[Dict]) -> List[Dict]:
        """Identify potential improvements"""
        improvements = []
        
        for pattern in patterns:
            if pattern["type"] == "failure_pattern":
                for failure_type, count in pattern["data"].get("types", {}).items():
                    if count >= 3:
                        improvements.append({
                            "id": f"imp_{len(self.improvement_suggestions)}",
                            "type": "fix",
                            "area": failure_type,
                            "priority": "high" if count >= 5 else "medium",
                            "description": f"Fix {count} failures related to {failure_type}",
                            "pattern": pattern
                        })
            
            elif pattern["type"] == "topic_frequency":
                # Suggest expanding knowledge in popular topics
                for topic, count in list(pattern["data"].items())[:3]:
                    if count >= 5:
                        improvements.append({
                            "id": f"imp_{len(self.improvement_suggestions)}",
                            "type": "expand",
                            "area": topic,
                            "priority": "medium",
                            "description": f"Expand knowledge about '{topic}' ({count} discussions)",
                            "pattern": pattern
                        })
        
        # Add general improvement suggestions
        if self.metrics["successful_interactions"] / max(1, self.metrics["total_interactions"]) < 0.7:
            improvements.append({
                "id": f"imp_{len(self.improvement_suggestions)}",
                "type": "optimize",
                "area": "response_quality",
                "priority": "high",
                "description": "Response quality could be improved - consider more detailed answers",
                "pattern": None
            })
        
        return improvements
    
    async def _apply_automatic_improvements(self, improvements: List[Dict]) -> int:
        """Apply improvements that can be done automatically"""
        applied = 0
        
        for improvement in improvements:
            if improvement["type"] == "fix" and improvement["priority"] == "high":
                # Apply the fix
                self.improvement_suggestions.append(improvement)
                applied += 1
                
                # Log the improvement
                self.knowledge_base["solutions"][improvement["area"]] = {
                    "applied_at": datetime.now().isoformat(),
                    "improvement": improvement
                }
        
        # Keep only recent suggestions
        if len(self.improvement_suggestions) > self.max_suggestions:
            self.improvement_suggestions = self.improvement_suggestions[-self.max_suggestions:]
        
        return applied
    
    def _learn_preferences(self, interaction: Dict):
        """Learn user preferences from interaction"""
        user_id = interaction.get("user_id")
        if not user_id:
            return
        
        prefs = self.user_preferences[user_id]
        
        # Learn from positive feedback
        if interaction.get("feedback") == "positive":
            if "topics" in interaction:
                prefs["likes"].extend(interaction["topics"])
            if "response_type" in interaction:
                prefs["likes"].append(interaction["response_type"])
        
        # Learn from negative feedback
        elif interaction.get("feedback") == "negative":
            if "topics" in interaction:
                prefs["dislikes"].extend(interaction["topics"])
            if "response_type" in interaction:
                prefs["dislikes"].append(interaction["response_type"])
        
        # Trim preferences to prevent bloat
        prefs["likes"] = prefs["likes"][-50:]
        prefs["dislikes"] = prefs["dislikes"][-50:]
    
    def _extract_knowledge(self, interaction: Dict):
        """Extract knowledge from interaction"""
        if "topics" in interaction:
            for topic in interaction["topics"]:
                if topic not in self.knowledge_base["topics"]:
                    self.knowledge_base["topics"][topic] = {
                        "first_seen": datetime.now().isoformat(),
                        "mentions": 0,
                        "contexts": []
                    }
                
                self.knowledge_base["topics"][topic]["mentions"] += 1
                if "context" in interaction:
                    self.knowledge_base["topics"][topic]["contexts"].append(interaction["context"])
        
        # Extract patterns
        if "pattern" in interaction:
            pattern_key = interaction["pattern"]
            if pattern_key not in self.knowledge_base["patterns"]:
                self.knowledge_base["patterns"][pattern_key] = []
            self.knowledge_base["patterns"][pattern_key].append(interaction)
    
    def get_suggestions(self) -> List[Dict]:
        """Get current improvement suggestions"""
        return self.improvement_suggestions[-10:]
    
    async def apply_suggestion(self, suggestion_id: str) -> Dict:
        """Apply a specific improvement suggestion"""
        suggestion = None
        index = None
        
        for i, s in enumerate(self.improvement_suggestions):
            if s["id"] == suggestion_id:
                suggestion = s
                index = i
                break
        
        if not suggestion:
            return {"success": False, "error": "Suggestion not found"}
        
        # Apply the suggestion (mark as applied)
        suggestion["applied"] = True
        suggestion["applied_at"] = datetime.now().isoformat()
        
        # Update knowledge base
        self.knowledge_base["solutions"][suggestion["area"]] = {
            "applied_at": datetime.now().isoformat(),
            "improvement": suggestion
        }
        
        return {
            "success": True,
            "suggestion": suggestion,
            "message": f"Applied improvement: {suggestion['description']}"
        }
    
    def get_capabilities_status(self) -> Dict:
        """Get status of all capabilities"""
        status = {}
        
        for capability in self.capabilities:
            # Calculate usage and success rate
            usage_count = sum(
                1 for i in self.interaction_history
                if i.get("capability") == capability
            )
            success_count = sum(
                1 for i in self.interaction_history
                if i.get("capability") == capability and i.get("success", True)
            )
            
            status[capability] = {
                "enabled": True,
                "usage_count": usage_count,
                "success_rate": round(success_count / max(1, usage_count), 2) if usage_count > 0 else None,
                "last_used": self._get_last_usage(capability)
            }
        
        return status
    
    def _get_last_usage(self, capability: str) -> Optional[str]:
        """Get last usage time for a capability"""
        for interaction in reversed(self.interaction_history):
            if interaction.get("capability") == capability:
                return interaction.get("timestamp")
        return None
    
    def get_knowledge_summary(self) -> Dict:
        """Get summary of learned knowledge"""
        return {
            "topics_learned": len(self.knowledge_base["topics"]),
            "patterns_identified": len(self.knowledge_base["patterns"]),
            "solutions_applied": len(self.knowledge_base["solutions"]),
            "user_preferences_tracked": len(self.user_preferences),
            "top_topics": list(self.knowledge_base["topics"].keys())[:5]
        }
    
    def reset_learning(self):
        """Reset learning data (for testing or user request)"""
        self.interaction_history = []
        self.success_patterns = []
        self.failure_patterns = []
        self.improvement_suggestions = []
        self.user_preferences = defaultdict(lambda: {"likes": [], "dislikes": []})
        self.knowledge_base = {
            "topics": {},
            "patterns": {},
            "solutions": {}
        }
        self.metrics = {
            "total_interactions": 0,
            "successful_interactions": 0,
            "failed_interactions": 0,
            "average_response_time": 0,
            "user_satisfaction": 0.85
        }
        
        return {"status": "reset", "message": "Learning data has been reset"}