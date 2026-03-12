from .Gemini_Config import GeminiConfig
from .Gemini_Generator import GeminiGenerator
from .Gemini_Interrogator import GeminiInterrogator
from .Gemini_Nano_Banana import GeminiNanoBanana
from .Gemini_Prompts import GeminiPositivePrompt, GeminiNegativePrompt

NODE_CLASS_MAPPINGS = {
    "Gemini_Config": GeminiConfig,
    "Gemini_Generator": GeminiGenerator,
    "Gemini_Interrogator": GeminiInterrogator,
    "Gemini_Nano_Banana": GeminiNanoBanana,
    "Gemini_Positive_Prompt": GeminiPositivePrompt,
    "Gemini_Negative_Prompt": GeminiNegativePrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gemini_Config": "UliGem Configuration",
    "Gemini_Generator": "UliGem Text Generator",
    "Gemini_Interrogator": "UliGem Image Interrogator",
    "Gemini_Nano_Banana": "UliGem Nano Banana (Image Gen)",
    "Gemini_Positive_Prompt": "UliGem Positive Prompt",
    "Gemini_Negative_Prompt": "UliGem Negative Prompt"
}

WEB_DIRECTORY = "web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
