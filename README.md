# Prompt Template App

The Prompt Template App is a [Streamlit](https://streamlit.io/)-based application for managing and using LLM prompt templates. It leverages [LangChain](https://python.langchain.com/v0.1/docs/modules/model_io/prompts/quick_start/) for prompt management.

Hugging Face Chat integration has been removed and is no longer supported. The app now focuses on creating, editing, and formatting prompts. Optionally, it can send prompts to a locally running LLM (e.g., via Ollama). If no LLM is configured, the app returns a placeholder response.

## Features

- **Edit Template:** Create new prompt templates or modify existing ones by specifying the name, topic, purpose, template content, and whether to enable the web search flag.

- **Use Template:** Select and use existing prompt templates. View template details, fill in input variables, optionally toggle the web search flag (UI only), choose a model name, and submit. If a local LLM endpoint is available (see "Optional: Local LLM via Ollama"), the app will send the formatted prompt to it; otherwise, a placeholder response is shown.

- **Prompting Principles:** Review guiding principles for creating effective prompts.

## Installation

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/gitwalter/prompt_template_app.git
    cd prompt_template_app
    ```

2. **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the Streamlit App:**
    ```sh
    streamlit run prompt_template_app.py
    ```

## Usage

1. **Edit Template:**
   - Use the sidebar to select "Edit Template".
   - Create a new template or modify existing ones by specifying details such as name, topic, purpose, and template content.
   - Save the template to the database.

2. **Use Template:**
   - Select "Use Template" from the sidebar.
   - Choose an existing template to view details and fill in input variables.
   - Optionally select a model name and toggle the web search flag.
   - Click "Submit" to generate the formatted prompt and, if a local LLM is configured, send it to the model and display the response.

3. **Prompting Principles:**
   - Refer to the guiding principles provided in the app to craft effective prompts.

## Optional: Local LLM via Ollama

By default, the app returns a placeholder response. To enable local inference:

1. Install [Ollama](https://ollama.com) on your machine.
2. Pull and run a model (example):
   ```sh
   ollama run llama2
   ```
3. In the app, select a matching model name (e.g., `llama2`) and submit your prompt.

The app will POST to `http://localhost:11434/api/generate` from `prompt_template_app.py` (function `call_chatbot`). You can customize that function to integrate with other local or remote LLMs.

## File Structure

```sh
├── import_csv_to_db.py        # Import prompt templates from CSV into the database
├── prompt_template_app.py     # Streamlit application
├── prompt_template_database.py# SQLAlchemy entity and session for templates
├── text_definitions.py        # Prompting principles and text content
├── prompt_templates.db        # SQLite database for storing prompt templates
└── requirements.txt           # Python dependencies
```

Note: The previous Hugging Face Chat integration has been removed from the app UI and flow.

Enjoy using the Prompt Template App! 🚀
