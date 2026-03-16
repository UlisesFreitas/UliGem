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
            
            # List of models that support native image generation (IMAGE modality)
            image_gen_models = ["gemini-2.5-flash-image", "gemini-3.1-flash-image-preview"]
            
            if model_name not in image_gen_models:
                print(f"[UliGem] WARNING: Model '{model_name}' might not support native IMAGE modality. Using it may cause a 400 Bad Request.")
            
            contents = []
            if image is not None:
                # Convert ComfyUI image tensor to PIL Image
                # image shape: [B, H, W, C]
                i = 255. * image[0].cpu().numpy()
                pil_img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                
                # FIX: Handle images with Alpha channel (transparency)
                # Gemini image modality expects RGB. Transparency can result in black backgrounds.
                if pil_img.mode in ('RGBA', 'LA') or (pil_img.mode == 'P' and 'transparency' in pil_img.info):
                    print(f"[UliGem] Input image has transparency (mode: {pil_img.mode}). Compositing onto white background.")
                    # Create a white background
                    background = Image.new("RGB", pil_img.size, (255, 255, 255))
                    # If it's palette mode with transparency, convert to RGBA first
                    if pil_img.mode == 'P':
                        pil_img = pil_img.convert("RGBA")
                    # Paste the image onto the background using its alpha as a mask
                    if 'A' in pil_img.getbands():
                        background.paste(pil_img, mask=pil_img.split()[3])
                    else:
                        background.paste(pil_img)
                    pil_img = background
                else:
                    pil_img = pil_img.convert("RGB")
                
                contents.append(pil_img)
            
            # Combine prompts for better understanding
            combined_prompt = f"[SYSTEM INSTRUCTIONS]: {instructions}\n\n[USER PROMPT]: {positive_prompt}\n\n[NEGATIVE INSTRUCTIONS]: Do NOT include: {negative_prompt}"
            contents.append(combined_prompt)

            # Generate content with IMAGE modality
            gen_config = types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                temperature=config.get("temperature", 1.0),
                top_p=config.get("top_p", 0.95),
                top_k=config.get("top_k", 40),
            )
            
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
                return (fallback_image, "Error: No image was generated. The model might have filtered the content or is incompatible with image modality.")

            # Custom output saving
            output_dir = folder_paths.get_output_directory()
            uligem_output_dir = os.path.join(output_dir, "output_UliGem")
            if not os.path.exists(uligem_output_dir):
                os.makedirs(uligem_output_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"UliGem_{timestamp}.png"
            filepath = os.path.join(uligem_output_dir, filename)
            
            # Save the first image
            first_img_pil = Image.fromarray((generated_images[0][0].numpy() * 255).astype(np.uint8))
            first_img_pil.save(filepath)

            return (generated_images[0], f"Success: Saved to {filepath}")

        except Exception as e:
            error_msg = str(e)
            print(f"[UliGem] API Error: {error_msg}")
            
            # Attempt to extract detailed reason from the SDK exception
            detailed_info = ""
            if "429" in error_msg:
                if "limit: 0" in error_msg:
                    detailed_info = " (Note: Your quota limit is 0. Image generation might be restricted in your region/tier for this model.)"
                elif "retry in" in error_msg:
                    import re
                    match = re.search(r"retry in ([\d\.]+s)", error_msg)
                    if match:
                        detailed_info = f" (Retry in {match.group(1)})"
                return (fallback_image, f"Error 429: Rate Limit/Quota Exceeded{detailed_info}. Check Google AI Studio billing/plan.")
            
            elif "400" in error_msg:
                return (fallback_image, f"Error 400: Bad Request. Model '{model_name}' likely does NOT support native image generation. Use 'gemini-2.5-flash-image'.")
            
            return (fallback_image, f"Error: {error_msg}")

NODE_CLASS_MAPPINGS = {
    "Gemini_Nano_Banana": GeminiNanoBanana
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gemini_Nano_Banana": "UliGem Nano Banana (Image Gen)"
}
