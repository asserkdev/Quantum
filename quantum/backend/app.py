"""
Quantum - Autonomous AI Assistant Backend
FastAPI server with all AI capabilities
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import asyncio
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import httpx

# Import local modules
from ai_engine import AIEngine
from search_agent import SearchAgent
from fact_checker import FactChecker
from image_gen import ImageGenerator
from auth_handler import AuthHandler
from self_improver import SelfImprover

# Initialize FastAPI app
app = FastAPI(
    title="Quantum AI Assistant",
    description="Autonomous AI with web search, fact-checking, image generation, and 3D capabilities",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
ai_engine = AIEngine()
search_agent = SearchAgent()
fact_checker = FactChecker()
image_generator = ImageGenerator()
auth_handler = AuthHandler()
self_improver = SelfImprover()

# Data models
class Message(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None
    mode: Optional[str] = "auto"  # auto, search, creative, coding, analysis

class SearchRequest(BaseModel):
    query: str
    depth: Optional[str] = "basic"  # basic, advanced, deep
    topic: Optional[str] = "general"

class FactCheckRequest(BaseModel):
    claim: str
    sources: Optional[List[str]] = []

class ImageGenRequest(BaseModel):
    prompt: str
    style: Optional[str] = "realistic"
    size: Optional[str] = "1024x1024"

# Conversation storage (in-memory for demo, use database in production)
conversations: Dict[str, List[Dict]] = {}

# ==================== CORE AI ENDPOINTS ====================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "name": "Quantum",
        "version": "1.0.0",
        "capabilities": [
            "chat", "search", "fact_check", "image_generation",
            "3d_generation", "code_generation", "self_improvement"
        ],
        "autonomous_mode": True
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint with autonomous capabilities"""
    try:
        # Determine the best mode based on user input
        mode = request.mode if request.mode != "auto" else ai_engine.detect_mode(request.message)
        
        # Process based on detected mode
        if mode == "search":
            result = await search_agent.search_and_analyze(request.message)
            # Handle search results - use summary or results
            search_response = result.get("summary", "") or result.get("response", "")
            if not search_response and result.get("results"):
                search_response = f"Found {len(result['results'])} results for your query. The top results suggest: {result['results'][0].get('content', '')[:200]}..."
            result = {"response": search_response, "sources": result.get("sources", []), "autonomous_actions": []}
        elif mode == "fact_check":
            result = await fact_checker.verify(request.message)
        elif mode == "image":
            result = await image_generator.generate(request.message)
        elif mode == "3d":
            result = await image_generator.generate_3d(request.message)
        elif mode == "coding":
            result = await ai_engine.generate_code(request.message)
            # Handle both response and code return formats
            code_result = result.get("code", result.get("response", ""))
            result = {
                "response": f"Here's the {result.get('language', 'code')} code I generated:\n\n```{result.get('language', 'python')}\n{code_result}\n```\n\nFeel free to ask if you need modifications!",
                "sources": [],
                "autonomous_actions": []
            }
        else:
            # Default: conversational AI with search augmentation
            result = await ai_engine.chat(
                request.message,
                conversation_id=request.conversation_id,
                user_id=request.user_id
            )
        
        # Store conversation
        conv_id = request.conversation_id or f"conv_{datetime.now().timestamp()}"
        if conv_id not in conversations:
            conversations[conv_id] = []
        
        conversations[conv_id].append({
            "role": "user",
            "content": request.message,
            "timestamp": datetime.now().isoformat()
        })
        conversations[conv_id].append({
            "role": "assistant",
            "content": result["response"],
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "sources": result.get("sources", [])
        })
        
        return {
            "response": result["response"],
            "mode": mode,
            "conversation_id": conv_id,
            "sources": result.get("sources", []),
            "autonomous_actions": result.get("autonomous_actions", []),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat response"""
    async def generate():
        try:
            mode = request.mode if request.mode != "auto" else ai_engine.detect_mode(request.message)
            
            if mode == "search":
                result = await search_agent.search_and_analyze(request.message)
                yield f"data: {json.dumps({'type': 'response', 'content': result['response']})}\n\n"
            elif mode == "fact_check":
                result = await fact_checker.verify(request.message)
                yield f"data: {json.dumps({'type': 'response', 'content': result['response']})}\n\n"
            else:
                async for chunk in ai_engine.chat_stream(request.message):
                    yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
            
            yield f"data: {json.dumps({'type': 'done', 'mode': mode})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

# ==================== SEARCH & RESEARCH ====================

@app.post("/api/search")
async def search(request: SearchRequest):
    """Web search with analysis"""
    result = await search_agent.search_and_analyze(request.query)
    return result

@app.post("/api/research")
async def research(query: str = Body(...)):
    """Deep research on a topic"""
    result = await search_agent.deep_research(query)
    return result

@app.get("/api/trending")
async def trending():
    """Get trending topics"""
    result = await search_agent.get_trending()
    return result

# ==================== FACT CHECKING ====================

@app.post("/api/fact-check")
async def fact_check(request: FactCheckRequest):
    """Verify claims and detect fake news"""
    result = await fact_checker.verify(request.claim, request.sources)
    return result

@app.post("/api/news-analysis")
async def news_analysis(url: str = Body(...)):
    """Analyze news article for credibility"""
    result = await fact_checker.analyze_news(url)
    return result

# ==================== IMAGE GENERATION ====================

@app.post("/api/generate/image")
async def generate_image(request: ImageGenRequest):
    """Generate image from text"""
    result = await image_generator.generate(request.prompt, request.style, request.size)
    return result

@app.post("/api/generate/3d")
async def generate_3d(prompt: str = Body(...)):
    """Generate 3D scene description"""
    result = await image_generator.generate_3d(prompt)
    return result

@app.get("/api/styles")
async def get_styles():
    """Get available image styles"""
    return {
        "styles": [
            "realistic", "artistic", "anime", "3d-render", 
            "abstract", "impressionist", "cyberpunk", "fantasy"
        ]
    }

# ==================== AUTHENTICATION ====================

@app.post("/api/auth/signup")
async def signup(email: str = Body(...), password: str = Body(...)):
    """User registration"""
    result = await auth_handler.signup(email, password)
    return result

@app.post("/api/auth/login")
async def login(email: str = Body(...), password: str = Body(...)):
    """User login"""
    result = await auth_handler.login(email, password)
    return result

@app.post("/api/auth/google")
async def google_auth(token: str = Body(...)):
    """Google OAuth login"""
    result = await auth_handler.google_auth(token)
    return result

@app.post("/api/auth/azure")
async def azure_auth(token: str = Body(...)):
    """Azure AD login"""
    result = await auth_handler.azure_auth(token)
    return result

@app.get("/api/auth/me")
async def get_me(user_id: str):
    """Get current user info"""
    result = await auth_handler.get_user(user_id)
    return result

# ==================== FILE HANDLING ====================

@app.post("/api/analyze/file")
async def analyze_file(file: UploadFile = File(...)):
    """Analyze uploaded file"""
    try:
        content = await file.read()
        result = await ai_engine.analyze_file(content, file.filename)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    """Analyze uploaded image"""
    try:
        content = await file.read()
        result = await ai_engine.analyze_image(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== AUTONOMOUS FEATURES ====================

@app.post("/api/autonomous/goal")
async def set_goal(goal: str = Body(...), user_id: Optional[str] = None):
    """Set an autonomous goal for Quantum"""
    result = await ai_engine.set_autonomous_goal(goal, user_id)
    return result

@app.get("/api/autonomous/goals")
async def get_goals(user_id: str):
    """Get active autonomous goals"""
    return {"goals": ai_engine.get_active_goals(user_id)}

@app.post("/api/autonomous/achieve")
async def achieve_goal(goal_id: str):
    """Work on achieving a goal"""
    result = await ai_engine.work_on_goal(goal_id)
    return result

@app.get("/api/autonomous/status")
async def get_autonomous_status():
    """Get Quantum's autonomous system status"""
    return {
        "active_goals": len(ai_engine.active_goals),
        "capabilities": ai_engine.capabilities,
        "self_improvement_enabled": self_improver.enabled,
        "learning_mode": self_improver.learning_mode
    }

# ==================== SELF IMPROVEMENT ====================

@app.post("/api/improve/analyze")
async def analyze_for_improvement():
    """Analyze recent interactions for self-improvement"""
    result = await self_improver.analyze_and_improve()
    return result

@app.get("/api/improve/suggestions")
async def get_improvement_suggestions():
    """Get improvement suggestions"""
    return {"suggestions": self_improver.get_suggestions()}

@app.post("/api/improve/apply")
async def apply_improvement(suggestion_id: str):
    """Apply an improvement"""
    result = await self_improver.apply_suggestion(suggestion_id)
    return result

# ==================== CONVERSATION MANAGEMENT ====================

@app.get("/api/conversation/{conv_id}")
async def get_conversation(conv_id: str):
    """Get conversation history"""
    if conv_id not in conversations:
        return {"messages": []}
    return {"messages": conversations[conv_id]}

@app.delete("/api/conversation/{conv_id}")
async def delete_conversation(conv_id: str):
    """Delete conversation"""
    if conv_id in conversations:
        del conversations[conv_id]
    return {"status": "deleted"}

# ==================== CODE GENERATION ====================

@app.post("/api/code/generate")
async def generate_code(
    description: str = Body(...),
    language: Optional[str] = None
):
    """Generate code from description"""
    result = await ai_engine.generate_code(description, language)
    return result

@app.post("/api/code/execute")
async def execute_code(code: str = Body(...), language: str = Body(...)):
    """Execute code in sandbox"""
    result = await ai_engine.execute_code(code, language)
    return result

@app.post("/api/code/debug")
async def debug_code(code: str = Body(...), error: str = Body(...)):
    """Debug code with error"""
    result = await ai_engine.debug_code(code, error)
    return result

# ==================== 3D SCENE ENDPOINTS ====================

@app.post("/api/3d/generate")
async def generate_3d_scene(request: dict):
    """Generate complete 3D scene"""
    result = await image_generator.create_3d_scene(
        request.get("prompt", ""),
        request.get("style", "realistic"),
        request.get("animation", True)
    )
    return result

@app.get("/api/3d/templates")
async def get_3d_templates():
    """Get 3D scene templates"""
    return {
        "templates": [
            "character", "environment", "abstract", 
            "sci-fi", "fantasy", "minimalist"
        ]
    }

# Run with: uvicorn app:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)