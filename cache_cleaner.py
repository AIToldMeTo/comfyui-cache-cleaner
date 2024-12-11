import aiohttp
import asyncio
from server import PromptServer
import json

class CacheCleaner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clean_cache": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "image_pass": ("IMAGE",),
                "model_pass": ("MODEL",),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "MODEL", "STRING",)
    RETURN_NAMES = ("image_pass", "model_pass", "status")
    FUNCTION = "clean_cache"
    CATEGORY = "utils/system"
    DESCRIPTION = """Calls the ComfyUI API to free model and node cache. 
Returns the inputs unchanged and provides API call status."""

    async def _call_api(self):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "unload_models": True,
            "free_memory": True
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post("http://127.0.0.1:8188/api/free", 
                                  headers=headers, 
                                  json=payload) as response:
                return response.status

    def clean_cache(self, clean_cache, image_pass=None, model_pass=None):
        status = "Cache cleaning skipped"
        
        if clean_cache:
            try:
                # Create event loop for async call if one doesn't exist
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                status_code = loop.run_until_complete(self._call_api())
                
                if status_code == 200:
                    status = "Cache cleaned successfully"
                else:
                    status = f"Error: API returned status code {status_code}"
            except Exception as e:
                status = f"Error: Failed to call API - {str(e)}"
                print(f"CacheCleaner Error: {str(e)}")
        
        print(f"CacheCleaner: {status}")
        
        return (image_pass, model_pass, status)

NODE_CLASS_MAPPINGS = {
    "CacheCleaner": CacheCleaner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CacheCleaner": "Cache Cleaner"
}