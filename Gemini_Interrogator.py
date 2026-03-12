from google import genai
from google.genai import types
import torch
import numpy as np
from PIL import Image

class GeminiInterrogator:
    """
    A node for image-to-text generation (image interrogation) using Gemini's vision capabilities.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "config": ("GEMINI_CONFIG",),
                "image": ("IMAGE",),
                "prompt": ("STRING", {"multiline": True, "default": "Describe this image in detail for a Stable Diffusion prompt."}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("description",)
    FUNCTION = "interrogate"
    CATEGORY = "UliGem"

    def interrogate(self, config, image, prompt):
        if not config or not config.get("api_key"):
            return ("Error: API Key not found in config node.",)

        api_key = config["api_key"]
        model_name = config["model_name"]

        try:
            # Initialize the new google-genai client
            client = genai.Client(api_key=api_key)
            
            # Convert ComfyUI image tensor [B, H, W, C] to PIL Image
            # ComfyUI typically passes a batch of images, we'll take the first one
            i = 255. * image[0].cpu().numpy()
            pil_img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            # Multimodal request
            response = client.models.generate_content(
                model=model_name,
                contents=[pil_img, prompt],
                config=types.GenerateContentConfig(
                    temperature=config["temperature"],
                    top_p=config["top_p"],
                    top_k=config["top_k"],
                    max_output_tokens=config["max_output_tokens"],
                )
            )
            
            return (response.text,)
        except Exception as e:
            return (f"Error during interrogation: {str(e)}",)

NODE_CLASS_MAPPINGS = {
    "Gemini_Interrogator": GeminiInterrogator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gemini_Interrogator": "UliGem Image Interrogator"
}
