# Skills: Gemini Integration for ComfyUI

## Core Capabilities
* **API Interaction**: Expert knowledge of Google Generative AI SDK (Python) for Gemini 1.5 Flash/Pro models.
* **ComfyUI Architecture**: Deep understanding of node classes (`INPUT_TYPES`, `RETURN_TYPES`, `FUNCTION`) and the execution loop.
* **Multimodal Processing**: Handling PIL images within ComfyUI and converting them to byte-streams compatible with Gemini Vision.
* **Prompt Engineering**: Crafting system instructions to ensure Gemini outputs clean, stable-diffusion-ready prompts.
* **Error Handling**: Managing API rate limits (especially for the free tier) and connection timeouts.

## Technical Stack
* **Language**: Python 3.10+
* **Libraries**: `google-generativeai`, `Pillow`, `torch`.
* **Environment**: Integration with `config.json` for secure API key storage.
