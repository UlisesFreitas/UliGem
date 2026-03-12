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

### Option 1: ComfyUI Portable (Windows)
If you are using the portable version of ComfyUI, your folder structure should look like this:
```text
ComfyUI_windows_portable/
├── ComfyUI/
│   └── custom_nodes/
│       └── UliGem/  <-- You are here
├── python_embeded/
├── update/
└── run_nvidia_gpu.bat
```

1. Open a terminal (CMD or PowerShell) in the `ComfyUI\custom_nodes\UliGem` directory.
2. Run the following command:
   ```bash
   ..\..\..\python_embeded\python.exe -m pip install -r requirements.txt
   ```

### Option 2: Standard ComfyUI / Manual Install
If you installed ComfyUI manually or are using a virtual environment:

1. Open a terminal in the `ComfyUI\custom_nodes\UliGem` directory.
2. Run:
   ```bash
   pip install -r requirements.txt
   ```

### Quick Install Script (Windows Portable)
You can create a file named `install.bat` inside the `UliGem` folder with this content and double-click it:
```batch
@echo off
..\..\..\python_embeded\python.exe -m pip install -r requirements.txt
pause
```

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

## 🛠️ Troubleshooting

### ⚠️ Common API Errors

- **Error 429 (Rate Limit Exceeded)**: 
  - **Cause**: You are using a Free Tier API key and have exceeded the requests-per-minute limit.
  - **Solution**: Wait 1 minute and try again. Consider upgrading to a Pay-as-you-go plan in Google AI Studio for higher limits.

- **Error 400 (Bad Request)**:
  - **Cause**: You selected a model that does not support native image generation (like `gemini-2.0-flash`).
  - **Solution**: Use `gemini-2.5-flash-image` or `gemini-3.1-flash-image-preview` for the **Nano Banana** node. Other models are for text/vision tasks only.

- **Black Image / No Output**:
  - **Cause**: The API safety filters might have blocked the content, or there was a temporary server failure.
  - **Solution**: Check the ComfyUI console for detailed error messages. Try a different prompt.

## 📂 Output Folder

Generated images are saved in:
`ComfyUI/output/output_UliGem/`

## 🤝 Credits

- Created by **Ulises Freitas**.
- Powered by [Google Gemini AI](https://deepmind.google/technologies/gemini/).

---
*Disclaimer: Use this extension responsibly and in accordance with Google's Generative AI TOS.*
