# ComfyUI Cache Cleaner Node

A custom node for ComfyUI that provides the ability to clear the cache directly from your workflow.

## Installation

1. Clone this repository into your `ComfyUI/custom_nodes/` directory:
```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/AIToldMeTo/comfyui-cache-cleaner
```

2. Start ComfyUI. The node will be available in the "utils/system" category.

## Usage

The Cache Cleaner node can be found in the "utils/system" category. 

- **clean_cache**: Boolean input to trigger cache cleaning
- **image_pass**: Optional image input that will be passed through
- **model_pass**: Optional model input that will be passed through

The node returns:
- The input image (if provided)
- The input model (if provided)
- A status message indicating if the cache was successfully cleaned

## Status Messages

- "Cache cleaning skipped": When clean_cache is set to false
- "Cache cleaned successfully": When the cache was successfully cleared
- "Error: API returned status code {code}": When the API call failed
- "Error: Failed to call API - {error}": When an exception occurred

## License

MIT License