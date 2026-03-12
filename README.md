# 🍌 UliGem: Google Gemini Integration for ComfyUI

UliGem is a powerful suite of custom nodes for ComfyUI that integrates **Google Gemini** models directly into your generative workflows. It features native support for image generation using **Gemini 2.0 (Nano Banana)**, advanced image interrogation, and seamless prompt management.

![UliGem Header](assets/logo.png)

## ✨ Key Features

- **🍌 Nano Banana (Image Gen)**: Native text-to-image and image-to-image generation using Gemini 2.0 Flash models.
- **👁️ Image Interrogator**: Analyze any image to generate detailed descriptions, prompts, or extract information.
- **⚙️ Integrated Settings**: Securely manage your API Key and default parameters directly from the ComfyUI Settings panel.
- **📁 Custom Output Management**: Automatically saves generated images to a dedicated `output_UliGem` folder.
- **🧠 Prompt Helpers**: Optimized nodes for positive and negative prompt construction.

## 🚀 Installation

1. **Clone the repository**:
   Navigate to your ComfyUI `custom_nodes` directory and run:
   ```bash
   git clone https://github.com/UlisesFreitas/UliGem.git
   ```

2. **Install dependencies**:
   Ensure you have the required Python packages installed:
   ```bash
   pip install -r requirements.txt
   ```
   *Required: `google-genai`, `pillow`, `torch`, `numpy`*

3. **Restart ComfyUI**.

## 🔑 Configuration

UliGem integrates directly with the ComfyUI Settings menu for a secure and clean configuration:

1. Open **ComfyUI Settings** (gear icon).
2. Look for the **UliGem** section.
3. Enter your **Google Gemini API Key**.
   *Get one for free at [Google AI Studio](https://aistudio.google.com/app/apikey).*
4. (Optional) Set your default model (e.g., `gemini-2.0-flash`) and generation parameters.

*Note: You can also use the `GOOGLE_API_KEY` environment variable as a fallback.*

## 🧩 Node Reference

### 🛠️ Configuration
- **UliGem Configuration**: Fetch settings from the UI and provide them to generator nodes.

### 🎨 Generation
- **UliGem Nano Banana (Image Gen)**: The core node for generating images.
  - **Inputs**: Positive Prompt, Negative Prompt, System Instructions, Optional Image (for I2I), Aspect Ratio.
  - **Outputs**: Generated IMAGE and a status string.

### 🔍 Analysis
- **UliGem Image Interrogator**: Describe or analyze images using Gemini's vision capabilities.

### 📝 Prompting
- **UliGem Positive Prompt**: Multi-line text area for positive instructions.
- **UliGem Negative Prompt**: Multi-line text area for negative constraints.
- **UliGem Text Generator**: General-purpose LLM generation for prompt expansion or creative writing.

## 📂 Output Folder

Generated images are saved in:
`ComfyUI/output/output_UliGem/`

## 🤝 Credits

- Created by **Ulises Freitas**.
- Powered by [Google Gemini AI](https://deepmind.google/technologies/gemini/).

---
*Disclaimer: Use this extension responsibly and in accordance with Google's Generative AI TOS.*
