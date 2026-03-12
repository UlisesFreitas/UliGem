class GeminiPositivePrompt:
    """
    A specialized node for Positive prompts with a large text area.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "A beautiful landscape, digital art"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "get_prompt"
    CATEGORY = "UliGem"

    def get_prompt(self, text):
        return (text,)

class GeminiNegativePrompt:
    """
    A specialized node for Negative prompts with a large text area.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "blurry, distorted, low quality"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "get_prompt"
    CATEGORY = "UliGem"

    def get_prompt(self, text):
        return (text,)

NODE_CLASS_MAPPINGS = {
    "Gemini_Positive_Prompt": GeminiPositivePrompt,
    "Gemini_Negative_Prompt": GeminiNegativePrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gemini_Positive_Prompt": "UliGem Positive Prompt",
    "Gemini_Negative_Prompt": "UliGem Negative Prompt"
}
