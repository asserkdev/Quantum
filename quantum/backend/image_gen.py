"""
Quantum Image Generator - Create images and 3D content
Handles image generation and 3D scene creation
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import base64
import random

class ImageGenerator:
    """
    Creative AI for image and 3D generation
    - Text-to-image generation
    - 3D scene creation
    - Animation generation
    - Style transfer
    """
    
    def __init__(self):
        self.styles = [
            "realistic", "artistic", "anime", "3d-render",
            "abstract", "impressionist", "cyberpunk", "fantasy",
            "watercolor", "oil-painting", "sketch", "pixel-art"
        ]
        
        self.sizes = {
            "small": "512x512",
            "medium": "1024x1024",
            "large": "1024x1792",
            "wide": "1792x1024"
        }
        
        self.generation_history = []
        
    async def generate(self, prompt: str, style: str = "realistic", size: str = "1024x1024") -> Dict:
        """
        Generate image from text prompt
        """
        # Validate inputs
        if style not in self.styles:
            style = "realistic"
        
        # Simulate image generation
        # In production, this would integrate with DALL-E, Stable Diffusion, etc.
        generation_id = f"img_{len(self.generation_history) + 1}_{datetime.now().timestamp()}"
        
        result = {
            "id": generation_id,
            "prompt": prompt,
            "style": style,
            "size": size,
            "status": "completed",
            "image_url": f"/generated/{generation_id}.png",
            "thumbnail_url": f"/generated/{generation_id}_thumb.png",
            "metadata": {
                "generation_time": random.uniform(2.5, 5.0),
                "model": "Quantum-Gen v1.0",
                "quality": "high",
                "steps": 30
            },
            "download_url": f"/api/download/{generation_id}",
            "share_url": f"/share/{generation_id}",
            "alternatives": await self._generate_alternatives(prompt, style),
            "created_at": datetime.now().isoformat()
        }
        
        self.generation_history.append(result)
        
        return {
            "success": True,
            "image": result,
            "message": f"Successfully generated your {style} image!",
            "prompt_analysis": self._analyze_prompt(prompt)
        }
    
    def _analyze_prompt(self, prompt: str) -> Dict:
        """Analyze the prompt for generation parameters"""
        prompt_lower = prompt.lower()
        
        # Detect elements
        elements = {
            "has_people": any(w in prompt_lower for w in ["person", "man", "woman", "child", "people", "crowd"]),
            "has_landscape": any(w in prompt_lower for w in ["landscape", "mountains", "ocean", "sky", "forest", "city"]),
            "has_objects": any(w in prompt_lower for w in ["object", "thing", "car", "building", "animal"]),
            "has_text": any(w in prompt_lower for w in ["text", "writing", "sign", "letter"]),
            "has_style_reference": any(w in prompt_lower for w in ["like", "style of", "inspired by", "similar to"])
        }
        
        # Detect mood
        moods = []
        if any(w in prompt_lower for w in ["happy", "bright", "sunny", "joyful"]):
            moods.append("bright")
        if any(w in prompt_lower for w in ["dark", "mysterious", "shadow", "gloomy"]):
            moods.append("dark")
        if any(w in prompt_lower for w in ["peaceful", "calm", "serene", "tranquil"]):
            moods.append("peaceful")
        if any(w in prompt_lower for w in ["action", "dynamic", "energetic", "fast"]):
            moods.append("dynamic")
        
        return {
            "detected_elements": [k for k, v in elements.items() if v],
            "detected_moods": moods,
            "complexity": "high" if sum(elements.values()) > 2 else "medium" if sum(elements.values()) > 0 else "simple",
            "estimated_generation_time": "3-5 seconds"
        }
    
    async def _generate_alternatives(self, prompt: str, style: str) -> List[Dict]:
        """Generate alternative versions"""
        alternatives = []
        
        # Generate a couple of style variations
        other_styles = [s for s in self.styles if s != style][:2]
        
        for alt_style in other_styles:
            alternatives.append({
                "style": alt_style,
                "prompt": prompt,
                "preview_url": f"/preview/{alt_style}_{len(self.generation_history)}.png"
            })
        
        return alternatives
    
    async def generate_3d(self, prompt: str) -> Dict:
        """
        Generate 3D scene description and configuration
        """
        scene_id = f"3d_{len(self.generation_history) + 1}_{datetime.now().timestamp()}"
        
        # Generate Three.js compatible scene
        scene_config = self._generate_scene_config(prompt)
        
        result = {
            "id": scene_id,
            "prompt": prompt,
            "status": "completed",
            "scene_config": scene_config,
            "preview_url": f"/3d/preview/{scene_id}.png",
            "model_url": f"/3d/model/{scene_id}.glb",
            "animation": await self._generate_animation(prompt),
            "metadata": {
                "format": "Three.js JSON/GLTF",
                "polygons": random.randint(10000, 50000),
                "materials": random.randint(2, 8),
                "lights": len(scene_config.get("lights", []))
            },
            "created_at": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "scene": result,
            "message": "3D scene generated successfully!",
            "three_js_code": self._generate_threejs_code(scene_config)
        }
    
    def _generate_scene_config(self, prompt: str) -> Dict:
        """Generate Three.js scene configuration"""
        prompt_lower = prompt.lower()
        
        # Determine scene type
        if any(w in prompt_lower for w in ["character", "person", "figure", "avatar"]):
            scene_type = "character"
            camera_pos = [0, 1.5, 3]
        elif any(w in prompt_lower for w in ["landscape", "outdoor", "nature", "mountain"]):
            scene_type = "landscape"
            camera_pos = [0, 5, 10]
        elif any(w in prompt_lower for w in ["room", "interior", "indoor", "home"]):
            scene_type = "interior"
            camera_pos = [0, 1.5, 2]
        elif any(w in prompt_lower for w in ["space", "galaxy", "planet", "stars", "cosmos"]):
            scene_type = "space"
            camera_pos = [0, 0, 15]
        else:
            scene_type = "abstract"
            camera_pos = [0, 0, 5]
        
        # Generate scene elements
        objects = self._generate_objects(prompt, scene_type)
        
        # Generate lighting
        lights = self._generate_lighting(prompt, scene_type)
        
        # Generate materials
        materials = self._generate_materials(prompt, scene_type)
        
        return {
            "type": scene_type,
            "camera": {
                "position": camera_pos,
                "fov": 75,
                "near": 0.1,
                "far": 1000
            },
            "objects": objects,
            "lights": lights,
            "materials": materials,
            "background": self._generate_background(prompt, scene_type),
            "fog": self._generate_fog(prompt, scene_type)
        }
    
    def _generate_objects(self, prompt: str, scene_type: str) -> List[Dict]:
        """Generate scene objects"""
        base_objects = {
            "character": [
                {"type": "mesh", "geometry": "capsule", "position": [0, 0.5, 0], "scale": [0.5, 1, 0.5]}
            ],
            "landscape": [
                {"type": "mesh", "geometry": "plane", "position": [0, 0, 0], "scale": [50, 1, 50]},
                {"type": "mesh", "geometry": "cone", "position": [-5, 1, -5], "scale": [2, 4, 2]},
                {"type": "mesh", "geometry": "cone", "position": [3, 0.8, -3], "scale": [1.5, 3, 1.5]}
            ],
            "interior": [
                {"type": "mesh", "geometry": "box", "position": [0, 0.25, 0], "scale": [3, 0.5, 2]},
                {"type": "mesh", "geometry": "box", "position": [-1, 0.75, 0], "scale": [0.5, 0.5, 0.5]}
            ],
            "space": [
                {"type": "particles", "count": 1000, "spread": 100},
                {"type": "mesh", "geometry": "sphere", "position": [0, 0, 0], "scale": [5, 5, 5]}
            ],
            "abstract": [
                {"type": "mesh", "geometry": "torus", "position": [0, 0, 0], "scale": [1.5, 1.5, 1.5]},
                {"type": "mesh", "geometry": "icosahedron", "position": [2, 1, -1], "scale": [0.8, 0.8, 0.8]}
            ]
        }
        
        return base_objects.get(scene_type, base_objects["abstract"])
    
    def _generate_lighting(self, prompt: str, scene_type: str) -> List[Dict]:
        """Generate lighting configuration"""
        lighting_presets = {
            "character": [
                {"type": "ambient", "color": 0xffffff, "intensity": 0.4},
                {"type": "directional", "color": 0xffffff, "intensity": 0.8, "position": [5, 5, 5]},
                {"type": "point", "color": 0xffd700, "intensity": 0.3, "position": [-3, 2, 2]}
            ],
            "landscape": [
                {"type": "directional", "color": 0xfffacd, "intensity": 1.0, "position": [10, 20, 10]},
                {"type": "ambient", "color": 0x87ceeb, "intensity": 0.3}
            ],
            "space": [
                {"type": "ambient", "color": 0x111133, "intensity": 0.2},
                {"type": "point", "color": 0xffaa00, "intensity": 1.0, "position": [0, 0, 0]}
            ],
            "default": [
                {"type": "ambient", "color": 0xffffff, "intensity": 0.5},
                {"type": "directional", "color": 0xffffff, "intensity": 0.7, "position": [5, 5, 5]}
            ]
        }
        
        return lighting_presets.get(scene_type, lighting_presets["default"])
    
    def _generate_materials(self, prompt: str, scene_type: str) -> List[Dict]:
        """Generate material configurations"""
        materials = {
            "character": [
                {"name": "skin", "color": 0xffccaa, "roughness": 0.7, "metalness": 0.0}
            ],
            "landscape": [
                {"name": "ground", "color": 0x228b22, "roughness": 0.9, "metalness": 0.0},
                {"name": "tree", "color": 0x006400, "roughness": 0.8, "metalness": 0.0}
            ],
            "space": [
                {"name": "planet", "color": 0x4169e1, "roughness": 0.5, "metalness": 0.3},
                {"name": "particles", "color": 0xffffff, "emissive": True}
            ],
            "default": [
                {"name": "default", "color": 0x888888, "roughness": 0.5, "metalness": 0.5}
            ]
        }
        
        return materials.get(scene_type, materials["default"])
    
    def _generate_background(self, prompt: str, scene_type: str) -> Dict:
        """Generate background configuration"""
        backgrounds = {
            "character": {"type": "gradient", "color1": 0x87ceeb, "color2": 0xf0f8ff},
            "landscape": {"type": "gradient", "color1": 0x87ceeb, "color2": 0xffffff},
            "interior": {"type": "solid", "color": 0xf5f5f5},
            "space": {"type": "solid", "color": 0x000011},
            "abstract": {"type": "gradient", "color1": 0x1a1a2e, "color2": 0x16213e}
        }
        
        return backgrounds.get(scene_type, backgrounds["abstract"])
    
    def _generate_fog(self, prompt: str, scene_type: str) -> Optional[Dict]:
        """Generate fog configuration"""
        prompt_lower = prompt.lower()
        
        if "foggy" in prompt_lower or "mist" in prompt_lower:
            return {"color": 0xcccccc, "near": 5, "far": 50}
        elif scene_type == "landscape":
            return {"color": 0xffffff, "near": 20, "far": 100}
        
        return None
    
    async def _generate_animation(self, prompt: str) -> Dict:
        """Generate animation configuration"""
        prompt_lower = prompt.lower()
        
        # Detect animation type
        if "rotate" in prompt_lower:
            anim_type = "rotation"
        elif "float" in prompt_lower or "hover" in prompt_lower:
            anim_type = "floating"
        elif "walk" in prompt_lower or "run" in prompt_lower:
            anim_type = "movement"
        elif "pulse" in prompt_lower or "breathe" in prompt_lower:
            anim_type = "pulse"
        else:
            anim_type = "auto"  # Auto-detect best animation
        
        return {
            "type": anim_type,
            "duration": 4000,  # milliseconds
            "easing": "easeInOutSine",
            "loop": True,
            "reverse": False
        }
    
    def _generate_threejs_code(self, scene_config: Dict) -> str:
        """Generate Three.js code for the scene"""
        code = f"""// Quantum 3D Scene Generator
// Generated: {datetime.now().isoformat()}

// Scene Configuration
const sceneConfig = {json.dumps(scene_config, indent=2)};

// Initialize Three.js Scene
const scene = new THREE.Scene();

// Camera
const camera = new THREE.PerspectiveCamera(
    {scene_config['camera']['fov']},
    window.innerWidth / window.innerHeight,
    {scene_config['camera']['near']},
    {scene_config['camera']['far']}
);
camera.position.set({', '.join(map(str, scene_config['camera']['position']))});

// Renderer
const renderer = new THREE.WebGLRenderer({{ antialias: true }});
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Lighting Setup
{self._generate_lighting_code(scene_config['lights'])}

// Object Creation
{self._generate_objects_code(scene_config['objects'])}

// Animation Loop
function animate() {{
    requestAnimationFrame(animate);
    // Add your animations here
    renderer.render(scene, camera);
}}
animate();
"""
        return code
    
    def _generate_lighting_code(self, lights: List[Dict]) -> str:
        """Generate Three.js lighting code"""
        code_lines = []
        
        for i, light in enumerate(lights):
            light_type = light['type'].capitalize()
            color = hex_to_js(light['color'])
            intensity = light['intensity']
            position = light.get('position', [0, 0, 0])
            
            if light['type'] == 'ambient':
                code_lines.append(f"const ambientLight = new THREE.AmbientLight({color}, {intensity});")
                code_lines.append("scene.add(ambientLight);")
            elif light['type'] == 'directional':
                code_lines.append(f"const dirLight{i} = new THREE.DirectionalLight({color}, {intensity});")
                code_lines.append(f"dirLight{i}.position.set({', '.join(map(str, position))});")
                code_lines.append(f"scene.add(dirLight{i});")
            elif light['type'] == 'point':
                code_lines.append(f"const pointLight{i} = new THREE.PointLight({color}, {intensity});")
                code_lines.append(f"pointLight{i}.position.set({', '.join(map(str, position))});")
                code_lines.append(f"scene.add(pointLight{i});")
        
        return '\n'.join(code_lines)
    
    def _generate_objects_code(self, objects: List[Dict]) -> str:
        """Generate Three.js object creation code"""
        code_lines = ["// Scene Objects"]
        
        for i, obj in enumerate(objects):
            geometry = obj.get('geometry', 'box')
            position = obj.get('position', [0, 0, 0])
            scale = obj.get('scale', [1, 1, 1])
            
            code_lines.append(f"const geometry{i} = new THREE.{geometry.capitalize()}Geometry(1, 32);")
            code_lines.append(f"const material{i} = new THREE.MeshStandardMaterial({{ color: 0x888888 }});")
            code_lines.append(f"const mesh{i} = new THREE.Mesh(geometry{i}, material{i});")
            code_lines.append(f"mesh{i}.position.set({', '.join(map(str, position))});")
            code_lines.append(f"mesh{i}.scale.set({', '.join(map(str, scale))});")
            code_lines.append(f"scene.add(mesh{i});")
        
        return '\n'.join(code_lines)
    
    async def create_3d_scene(self, prompt: str, style: str = "realistic", animation: bool = True) -> Dict:
        """Create complete 3D scene with all assets"""
        scene_result = await self.generate_3d(prompt)
        
        # Add style-specific modifications
        if style == "cyberpunk":
            scene_result["scene"]["scene_config"]["background"] = {"type": "solid", "color": 0x0a0a1a}
            scene_result["scene"]["scene_config"]["lights"].append(
                {"type": "point", "color": 0x00ffff, "intensity": 0.5, "position": [3, 2, 0]}
            )
        elif style == "fantasy":
            scene_result["scene"]["scene_config"]["fog"] = {"color": 0x8b4513, "near": 10, "far": 50}
        
        return {
            "success": True,
            "scene": scene_result["scene"],
            "three_js_code": scene_result["three_js_code"],
            "message": f"Complete {style} 3D scene created!",
            "export_options": ["GLTF", "OBJ", "FBX", "USDZ"]
        }
    
    def get_generation_history(self) -> List[Dict]:
        """Get image generation history"""
        return self.generation_history


def hex_to_js(hex_color: int) -> str:
    """Convert hex color to Three.js format"""
    return f"0x{hex_color:06x}"