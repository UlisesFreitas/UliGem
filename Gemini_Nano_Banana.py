from google import genai
from google.genai import types
import torch
import numpy as np
from PIL import Image
import io
import os
import folder_paths
from datetime import datetime

class GeminiNanoBanana:
    """
    A node for native image generation using Gemini 2.0 (Nano Banana).
    Supports Text-to-Image and Image-to-Image with Positive and Negative prompts.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "config": ("GEMINI_CONFIG",),
                "positive_prompt": ("STRING", {"multiline": True, "default": "A high-quality digital painting of a futuristic city"}),
                "negative_prompt": ("STRING", {"multiline": True, "default": "blurry, background, lightning, distorted, low quality, text, watermark"}),
                "instructions": ("STRING", {"multiline": True, "default": "Output a detailed high-quality image. Focus on cinematic lighting and sharp details."}),
            },
            "optional": {
                "image": ("IMAGE",),
                "aspect_ratio": (["1:1", "4:3", "3:4", "16:9", "9:16"], {"default": "1:1"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "status")
    FUNCTION = "generate_image"
    CATEGORY = "UliGem"

    def generate_image(self, config, positive_prompt, negative_prompt, instructions, image=None, aspect_ratio="1:1"):
        # Create a blank fallback image to prevent ComfyUI crashes
        fallback_image = torch.zeros((1, 64, 64, 3))
        
        if not config or not config.get("api_key"):
            return (fallback_image, "Error: API Key not found in config node.")

        api_key = config["api_key"]
        # Default to gemini-2.5-flash-image (Nano Banana)
        model_name = config.get("model_name", "gemini-2.5-flash-image")
        
        try:
            # Initialize the new google-genai client
            client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})
            
            contents = []
            if image is not None:
                # Convert ComfyUI image tensor to PIL Image
                i = 255. * image[0].cpu().numpy()
                pil_img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                contents.append(pil_img)
            
            # Combine prompts for better understanding if native negative_prompt isn't supported or for reinforcement
            # Gemini models often respond well to explicit instructions.
            combined_prompt = f"[SYSTEM INSTRUCTIONS]: {instructions}\n\n[USER PROMPT]: {positive_prompt}\n\n[NEGATIVE INSTRUCTIONS]: Do NOT include: {negative_prompt}"
            contents.append(combined_prompt)

            # Generate content with IMAGE modality
            # We try to pass negative_prompt in config if the model supports it natively
            # but we also include it in the combined prompt for robustness.
            gen_config = types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                temperature=config.get("temperature", 1.0),
                top_p=config.get("top_p", 0.95),
                top_k=config.get("top_k", 40),
            )
            
            # Some models in the new SDK support a native negative_prompt in the config
            # We'll use a try-set approach or just rely on the combined prompt which is safer for Gemini 2.x
            
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=gen_config
            )

            # Extract generated images from parts
            generated_images = []
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        img = Image.open(io.BytesIO(part.inline_data.data)).convert("RGB")
                        
                        # Convert PIL to ComfyUI tensor [B, H, W, C]
                        img_np = np.array(img).astype(np.float32) / 255.0
                        img_tensor = torch.from_numpy(img_np)[None,]
                        generated_images.append(img_tensor)

            if not generated_images:
                return (fallback_image, "Error: No image was generated in the response. Check API safety filters or model availability.")

            # Custom output saving
            output_dir = folder_paths.get_output_directory()
            uligem_output_dir = os.path.join(output_dir, "output_UliGem")
            if not os.path.exists(uligem_output_dir):
                os.makedirs(uligem_output_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"UliGem_{timestamp}.png"
            filepath = os.path.join(uligem_output_dir, filename)
            
            # Save the first image to the custom folder
            first_img_pil = Image.open(io.BytesIO(response.candidates[0].content.parts[0].inline_data.data)).convert("RGB")
            first_img_pil.save(filepath)

            # Return the first image
            return (generated_images[0], f"Success: Saved to {filepath}")

        except Exception as e:
            return (fallback_image, f"Error during google-genai generation: {str(e)}")

NODE_CLASS_MAPPINGS = {
    "Gemini_Nano_Banana": GeminiNanoBanana
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gemini_Nano_Banana": "UliGem Nano Banana (Image Gen)"
}
