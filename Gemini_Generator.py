from google import genai
from google.genai import types

class GeminiGenerator:
    """
    A node for text-to-text generation using Gemini.
    Can be used for prompt expansion, translation, or general creative writing.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "config": ("GEMINI_CONFIG",),
                "prompt": ("STRING", {"multiline": True, "default": "Enhance this prompt for Stable Diffusion: a futuristic city"}),
                "system_instruction": ("STRING", {"multiline": True, "default": "You are a helpful assistant that writes detailed image generation prompts. Focus on descriptive adjectives, lighting, and composition."}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate"
    CATEGORY = "UliGem"

    def generate(self, config, prompt, system_instruction):
        if not config or not config.get("api_key"):
            return ("Error: API Key not found in config node.",)

        api_key = config["api_key"]
        model_name = config["model_name"]
        
        try:
            # Initialize the new google-genai client
            client = genai.Client(api_key=api_key)
            
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=config["temperature"],
                    top_p=config["top_p"],
                    top_k=config["top_k"],
                    max_output_tokens=config["max_output_tokens"],
                )
            )
            
            return (response.text,)
        except Exception as e:
            return (f"Error during generation: {str(e)}",)

NODE_CLASS_MAPPINGS = {
    "Gemini_Generator": GeminiGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gemini_Generator": "UliGem Text Generator"
}
