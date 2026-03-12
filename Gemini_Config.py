from google import genai

class GeminiConfig:
    """
    A configuration node for Gemini API.
    Provides the API key and model selection for other Gemini nodes.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": ([
                    "gemini-2.5-flash-image",        # [IMAGE GEN]
                    "gemini-3.1-flash-image-preview",# [IMAGE GEN]
                    "gemini-2.0-flash",              # [TEXT/VISION ONLY]
                    "gemini-2.5-pro",                # [TEXT/VISION ONLY]
                    "gemini-1.5-flash",              # [TEXT/VISION ONLY]
                    "gemini-1.5-pro"                 # [TEXT/VISION ONLY]
                ], {"default": "gemini-2.5-flash-image"}),
                "temperature": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "top_p": ("FLOAT", {"default": 0.95, "min": 0.0, "max": 1.0, "step": 0.01}),
                "top_k": ("INT", {"default": 40, "min": 0, "max": 100, "step": 1}),
                "max_output_tokens": ("INT", {"default": 2048, "min": 1, "max": 8192, "step": 1}),
            },
        }

    RETURN_TYPES = ("GEMINI_CONFIG",)
    RETURN_NAMES = ("config",)
    FUNCTION = "configure"
    CATEGORY = "UliGem"

    def configure(self, model_name, temperature, top_p, top_k, max_output_tokens):
        import json
        import os
        
        # Determine the path to comfy.settings.json
        # ComfyUI V1 stores it in user/default/comfy.settings.json
        # path is ../../user/default/comfy.settings.json relative to custom_nodes/UliGem/
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        settings_path = os.path.join(base_path, "user", "default", "comfy.settings.json")
        
        api_key = ""
        s_model = model_name
        s_temp = temperature
        s_top_p = top_p
        s_top_k = top_k
        s_max_tokens = max_output_tokens

        try:
            if os.path.exists(settings_path):
                with open(settings_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    # The setting ID matches our JS
                    api_key = settings.get("UliGem.ApiKey", "")
                    s_model = settings.get("UliGem.ModelName", model_name)
                    s_temp = settings.get("UliGem.Temperature", temperature)
                    s_top_p = settings.get("UliGem.TopP", top_p)
                    s_top_k = settings.get("UliGem.TopK", top_k)
                    s_max_tokens = settings.get("UliGem.MaxOutputTokens", max_output_tokens)
        except Exception:
            pass

        # Fallback to environment variable if settings fail
        if not api_key:
            api_key = os.environ.get("GOOGLE_API_KEY", "")

        config = {
            "api_key": api_key,
            "model_name": s_model,
            "temperature": float(s_temp),
            "top_p": float(s_top_p),
            "top_k": int(s_top_k),
            "max_output_tokens": int(s_max_tokens),
        }
        return (config,)

NODE_CLASS_MAPPINGS = {
    "Gemini_Config": GeminiConfig
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gemini_Config": "UliGem Configuration"
}
