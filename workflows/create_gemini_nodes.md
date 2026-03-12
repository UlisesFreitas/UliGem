---
description: How to create and manage Gemini custom nodes for ComfyUI
---

This workflow guides you through the process of adding new custom nodes to the `comfyUI-GemUli` extension.

### 1. Requirements Analysis
Review the specific Gemini model capabilities (e.g., Gemini 1.5 Pro, 2.0 Flash) and identify the necessary input/output types for ComfyUI.

### 2. Node Implementation
Create a new Python file in the `custom_nodes/comfyUI-GemUli/` directory following this template:

```python
import google.generativeai as genai

class YourNodeName:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "config": ("GEMINI_CONFIG",),
                "param": ("TYPE", {"default": value}),
            },
        }

    RETURN_TYPES = ("TYPE",)
    RETURN_NAMES = ("name",)
    FUNCTION = "execute"
    CATEGORY = "Gemini"

    def execute(self, config, param):
        # Implementation logic here
        return (result,)

NODE_CLASS_MAPPINGS = { "YourNodeName": YourNodeName }
NODE_DISPLAY_NAME_MAPPINGS = { "YourNodeName": "Your Display Name" }
```

### 3. Registration
Add your new node to `__init__.py`:
1. Import the class.
2. Add it to `NODE_CLASS_MAPPINGS`.
3. Add it to `NODE_DISPLAY_NAME_MAPPINGS`.

### 4. Verification
- Restart ComfyUI.
- Add the node to a workflow.
- Connect it to a `Gemini_Config` node.
- Verify the output.
