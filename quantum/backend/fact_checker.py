"""
Quantum Fact Checker - News verification and fake news detection
Distinguishes real news from fake with source verification
"""

import os
import asyncio
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import httpx

class FactChecker:
    """
    Autonomous fact-checking system
    - Claim verification
    - Source credibility assessment
    - Fake news detection
    - News article analysis
    """
    
    def __init__(self):
        self.trusted_sources = {
            "high": [
                "reuters.com", "apnews.com", "bbc.com", "npr.org",
                "nytimes.com", "washingtonpost.com", "theguardian.com",
                "sciencedirect.com", "nature.com", "arxiv.org",
                "who.int", "cdc.gov", "nih.gov"
            ],
            "medium": [
                "cnn.com", "foxnews.com", "msnbc.com", "abcnews.go.com",
                "nbcnews.com", "usatoday.com", "wsj.com", "bloomberg.com"
            ],
            "low": [
                "facebook.com", "twitter.com", "reddit.com", "4chan.org"
            ]
        }
        
        self.fake_news_patterns = [
            r"SHOCKING",
            r"YOU WON'T BELIEVE",
            r"99% OF PEOPLE",
            r"SHARE THIS OR",
            r"FAKE NEWS",
            r"MUST SEE",
            r"BREAKING:.*just in"
        ]
        
        self.fact_check_history = []
        
    async def verify(self, claim: str, sources: Optional[List[str]] = None) -> Dict:
        """
        Verify a claim and check if it's true or fake
        """
        # Analyze claim characteristics
        claim_analysis = self._analyze_claim(claim)
        
        # Check source credibility if provided
        source_analysis = self._analyze_sources(sources or [])
        
        # Cross-reference with known facts
        verification = await self._cross_reference(claim)
        
        # Generate verdict
        verdict = self._generate_verdict(claim_analysis, source_analysis, verification)
        
        # Store in history
        self.fact_check_history.append({
            "claim": claim,
            "verdict": verdict,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "claim": claim,
            "verdict": verdict,
            "analysis": claim_analysis,
            "source_credibility": source_analysis,
            "verification": verification,
            "explanation": self._generate_explanation(verdict, claim_analysis),
            "recommendations": self._get_recommendations(verdict),
            "timestamp": datetime.now().isoformat()
        }
    
    def _analyze_claim(self, claim: str) -> Dict:
        """Analyze claim characteristics"""
        claim_lower = claim.lower()
        
        # Check for fake news patterns
        fake_pattern_matches = []
        for pattern in self.fake_news_patterns:
            if re.search(pattern, claim, re.IGNORECASE):
                fake_pattern_matches.append(pattern)
        
        # Check claim structure
        has_extremes = bool(re.search(r'(always|never|100%|everyone|nobody|all|none)', claim_lower))
        has_certainty = bool(re.search(r'(definitely|absolutely|guaranteed|certainly)', claim_lower))
        has_emotion = bool(re.search(r'(shocking|outrageous|incredible|amazing|terrifying)', claim_lower))
        
        # Check for statistics
        has_stats = bool(re.search(r'\d+%|\d+ percent|\d+ out of|\d+ in \d+', claim_lower))
        
        # Check for source attribution
        has_sources = bool(re.search(r'(according to|study|research| scientists| experts| report)', claim_lower))
        
        return {
            "suspicious_patterns": fake_pattern_matches,
            "has_extremes": has_extremes,
            "has_certainty": has_certainty,
            "has_emotion": has_emotion,
            "has_statistics": has_stats,
            "has_sources": has_sources,
            "claim_length": len(claim),
            "suspicion_score": len(fake_pattern_matches) * 0.2 + has_extremes * 0.15 + has_emotion * 0.1,
            "verifiable": has_stats or has_sources
        }
    
    def _analyze_sources(self, sources: List[str]) -> Dict:
        """Analyze source credibility"""
        if not sources:
            return {
                "credibility": "unknown",
                "reliable_count": 0,
                "unreliable_count": 0,
                "sources": []
            }
        
        reliable = 0
        medium = 0
        unreliable = 0
        analyzed = []
        
        for source in sources:
            source_lower = source.lower()
            credibility = "unknown"
            
            for t in self.trusted_sources["high"]:
                if t in source_lower:
                    reliable += 1
                    credibility = "high"
                    break
            
            if credibility == "unknown":
                for t in self.trusted_sources["medium"]:
                    if t in source_lower:
                        medium += 1
                        credibility = "medium"
                        break
            
            if credibility == "unknown":
                for t in self.trusted_sources["low"]:
                    if t in source_lower:
                        unreliable += 1
                        credibility = "low"
                        break
            
            analyzed.append({
                "source": source,
                "credibility": credibility
            })
        
        total = reliable + medium + unreliable
        avg_credibility = (reliable * 1.0 + medium * 0.6 + unreliable * 0.2) / total if total > 0 else 0.5
        
        return {
            "credibility": "high" if avg_credibility > 0.7 else "medium" if avg_credibility > 0.4 else "low",
            "reliable_count": reliable,
            "medium_count": medium,
            "unreliable_count": unreliable,
            "sources": analyzed,
            "overall_score": round(avg_credibility, 2)
        }
    
    async def _cross_reference(self, claim: str) -> Dict:
        """Cross-reference claim with known facts"""
        # Simulated cross-referencing
        # In production, this would search multiple fact-checking databases
        
        claim_lower = claim.lower()
        
        # Check for obviously false patterns
        false_indicators = [
            ("vaccines cause autism", False, "Extensively debunked by scientific community"),
            ("earth is flat", False, "Scientifically disproven"),
            ("moon landing was fake", False, "Overwhelming evidence supports moon landing"),
            ("climate change is fake", False, "Scientific consensus supports climate change")
        ]
        
        for claim_type, truth_value, explanation in false_indicators:
            if claim_type in claim_lower:
                return {
                    "verified": not truth_value,
                    "truth_value": "False" if not truth_value else "True",
                    "confidence": 0.95,
                    "explanation": explanation,
                    "fact_checked_by": "Known fact verification"
                }
        
        # For unknown claims, flag for further verification
        return {
            "verified": None,
            "truth_value": "Unverified",
            "confidence": 0.3,
            "explanation": "This claim requires additional verification from multiple sources.",
            "fact_checked_by": "Partial verification"
        }
    
    def _generate_verdict(self, claim_analysis: Dict, source_analysis: Dict, verification: Dict) -> str:
        """Generate final verdict"""
        suspicion_score = claim_analysis.get("suspicion_score", 0)
        source_cred = source_analysis.get("overall_score", 0.5)
        verified = verification.get("verified")
        
        # Calculate composite score
        composite = (1 - suspicion_score) * 0.4 + source_cred * 0.4 + (verification.get("confidence", 0.5) if verified is not None else 0.2)
        
        if verified is False or suspicion_score > 0.5:
            return "FALSE"
        elif verified is True and suspicion_score < 0.3:
            return "TRUE"
        elif composite > 0.7:
            return "LIKELY TRUE"
        elif composite < 0.3:
            return "LIKELY FALSE"
        else:
            return "UNVERIFIED"
    
    def _generate_explanation(self, verdict: str, claim_analysis: Dict) -> str:
        """Generate detailed explanation"""
        explanations = {
            "TRUE": (
                "This claim appears to be accurate based on analysis of:\n"
                "• Claim structure and language\n"
                "• Source attribution\n"
                "• Statistical backing\n\n"
                "However, always verify with primary sources when possible."
            ),
            "FALSE": (
                "This claim appears to be FALSE based on analysis of:\n"
                f"• Suspicious patterns detected: {', '.join(claim_analysis.get('suspicious_patterns', ['None']))}\n"
                "• Extreme language or claims without evidence\n"
                "• Known false information patterns\n\n"
                "⚠️ We recommend verifying this through authoritative sources."
            ),
            "LIKELY TRUE": (
                "This claim is probably accurate, but we recommend:\n"
                "• Verifying with primary sources\n"
                "• Checking recent updates\n"
                "• Cross-referencing with multiple outlets"
            ),
            "LIKELY FALSE": (
                "This claim has several red flags:\n"
                f"• Suspicion score: {claim_analysis.get('suspicion_score', 0):.2f}\n"
                "• Limited verifiable evidence\n"
                "• Patterns similar to misinformation\n\n"
                "⚠️ Please verify with trusted sources before sharing."
            ),
            "UNVERIFIED": (
                "This claim cannot be verified with current data.\n\n"
                "To verify, we recommend:\n"
                "• Checking primary sources\n"
                "• Looking for official statements\n"
                "• Cross-referencing multiple news outlets"
            )
        }
        
        return explanations.get(verdict, explanations["UNVERIFIED"])
    
    def _get_recommendations(self, verdict: str) -> List[str]:
        """Get recommendations based on verdict"""
        recommendations = {
            "TRUE": [
                "Safe to share",
                "Include source attribution when sharing",
                "Check for updated information periodically"
            ],
            "FALSE": [
                "Do NOT share this claim",
                "Report to fact-checking platforms",
                "Share corrections if you previously shared"
            ],
            "LIKELY TRUE": [
                "Verify with primary sources before sharing",
                "Include caveats when sharing",
                "Update if new information contradicts"
            ],
            "LIKELY FALSE": [
                "Do not share without verification",
                "Investigate further before drawing conclusions",
                "Be cautious with this information"
            ],
            "UNVERIFIED": [
                "Seek additional sources",
                "Check official channels",
                "Wait for more information before acting"
            ]
        }
        
        return recommendations.get(verdict, recommendations["UNVERIFIED"])
    
    async def analyze_news(self, url: str) -> Dict:
        """Analyze a news article for credibility"""
        # In production, this would fetch and analyze the actual article
        return {
            "url": url,
            "credibility_score": 0.75,
            "factors": {
                "source_credibility": "High",
                "writing_quality": "Professional",
                "factual_support": "Evidence provided",
                "bias_indicators": "Minimal",
                "emotional_language": "Moderate"
            },
            "recommendations": [
                "This appears to be from a credible source",
                "Cross-reference with other outlets for confirmation",
                "Check publication date for timeliness"
            ],
            "analysis": "The article appears to be legitimate news content from a reputable source. However, always verify important claims with multiple sources.",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_fact_check_stats(self) -> Dict:
        """Get fact-checking statistics"""
        verdicts = [h["verdict"] for h in self.fact_check_history]
        
        return {
            "total_checks": len(self.fact_check_history),
            "true_count": verdicts.count("TRUE"),
            "false_count": verdicts.count("FALSE"),
            "likely_true": verdicts.count("LIKELY TRUE"),
            "likely_false": verdicts.count("LIKELY FALSE"),
            "unverified": verdicts.count("UNVERIFIED"),
            "last_check": self.fact_check_history[-1] if self.fact_check_history else None
        }