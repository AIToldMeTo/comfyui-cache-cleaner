import requests
from server import PromptServer
from comfy.comfy_types.node_typing import IO
import json

class CacheCleaner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clean_cache": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "anything": (IO.ANY, {}),
                "image_pass": ("IMAGE",{}),
                "model_pass": ("MODEL",{}),
            }
        }
    
    RETURN_TYPES = (IO.ANY,"IMAGE", "MODEL", "STRING",)
    RETURN_NAMES = ("anything","image_pass", "model_pass", "status")
    FUNCTION = "clean_cache"
    CATEGORY = "utils/system"
    DESCRIPTION = """Calls the ComfyUI API to free model and node cache. 
Returns the inputs unchanged and provides API call status."""

    def _call_api(self, address):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "unload_models": True,
            "free_memory": True
        }
        
        try:
            response = requests.post(
                f"http://{address.replace('0.0.0.0','127.0.0.1')}/api/free", 
                headers=headers, 
                json=payload,
                timeout=10
            )
            return response.status_code
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def clean_cache(self, clean_cache, anything=None, image_pass=None, model_pass=None):
        status = "Cache cleaning skipped"
        address = f"{PromptServer.instance.address}:{PromptServer.instance.port}"
        
        if clean_cache:
            try:
                status_code = self._call_api(address)
                
                if status_code == 200:
                    status = "Cache cleaned successfully"
                else:
                    status = f"Error: API returned status code {status_code}"
            except Exception as e:
                status = f"Error: Failed to call API - {str(e)}"
                print(f"CacheCleaner Error: {str(e)}")
        
        status = f"Status: {status}\nServer address: {address}"
        print(f"CacheCleaner: {status}")
        
        return (anything, image_pass, model_pass, status)

NODE_CLASS_MAPPINGS = {
    "CacheCleaner": CacheCleaner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CacheCleaner": "Cache Cleaner"
}