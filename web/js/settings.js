import { app } from "../../../scripts/app.js";

app.registerExtension({
	name: "UliGem.Settings",
	init() {
		app.ui.settings.addSetting({
			id: "UliGem.ApiKey",
			name: "UliGem: Google Gemini API Key",
			type: "text",
			defaultValue: "",
		});

		app.ui.settings.addSetting({
			id: "UliGem.ModelName",
			name: "UliGem: Default Model",
			type: "combo",
			options: [
				"gemini-2.5-flash-image",
				"gemini-3.1-flash-image-preview",
				"gemini-2.0-flash",
				"gemini-2.5-pro",
				"gemini-1.5-flash", 
				"gemini-1.5-pro"
			],
			defaultValue: "gemini-2.5-flash-image",
		});

		app.ui.settings.addSetting({
			id: "UliGem.Temperature",
			name: "UliGem: Default Temperature",
			type: "number",
			attrs: {
				min: 0,
				max: 2,
				step: 0.1
			},
			defaultValue: 1.0,
		});

		app.ui.settings.addSetting({
			id: "UliGem.TopP",
			name: "UliGem: Default Top P",
			type: "number",
			attrs: {
				min: 0,
				max: 1,
				step: 0.01
			},
			defaultValue: 0.95,
		});

		app.ui.settings.addSetting({
			id: "UliGem.TopK",
			name: "UliGem: Default Top K",
			type: "number",
			attrs: {
				min: 0,
				max: 100,
				step: 1
			},
			defaultValue: 40,
		});

		app.ui.settings.addSetting({
			id: "UliGem.MaxOutputTokens",
			name: "UliGem: Default Max Output Tokens",
			type: "number",
			attrs: {
				min: 1,
				max: 8192,
				step: 1
			},
			defaultValue: 2048,
		});

		app.ui.settings.addSetting({
			id: "UliGem.Links",
			name: "UliGem: Links & Help",
			type: "text",
			defaultValue: "API Keys: https://aistudio.google.com/app/apikey | Docs: https://github.com/google-gemini/generative-ai-python",
			attrs: {
				readonly: true
			}
		});
	}
});
