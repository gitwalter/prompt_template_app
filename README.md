# Prompt Template App

The Prompt Template App is a [Streamlit](https://streamlit.io/)-based application designed for managing and utilizing LLM-prompt templates for generating conversational prompts. It leverages [LangChain](https://python.langchain.com/v0.1/docs/modules/model_io/prompts/quick_start/) for prompt management and interacts with [HuggingChat](https://huggingface.co/chat/) chatbots via the unofficial [HuggingChat Python-API](https://github.com/Soulter/hugging-chat-api.git). This app provides a user-friendly interface for creating, editing, and using prompt templates efficiently.


## Features

- **Edit Template:** Allows users to create new prompt templates or modify existing ones. Users can specify the template's name, topic, purpose, template content, and whether to enable web search.
  
- **Use Template:** Enables users to select and utilize existing prompt templates. Users can view details of the selected template, including its topic, name, purpose, and template content. They can also interact with HuggingFace chatbots using the selected template and choose from available models for chat interactions.

- **Prompting Principles:** Provides users with guiding principles for creating effective prompts, enhancing their understanding of how to design useful templates.

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
   - Choose an existing template from the dropdown menu to view its details.
   - Interact with HuggingFace chatbots using the selected template and available models.

3. **Prompting Principles:**
   - Refer to the guiding principles provided in the app to create effective prompts for better interaction with chatbots.

## File Structure

```sh
├── huggingface_chat.py # Wrapper for calling the HuggingFace LLM chatbot API
├── import_csv_to_db.py # Program for importing prompt templates from CSV files into the database
├── prompt_template_app.py # Main application file with logic
├── prompt_template_database.py # Database file with SQLAlchemy entity PromptTemplate
├── prompt_templates.db # SQLite database for storing prompt templates wrapped by SQLAlchemy
└── requirements.txt # Requirements for the Streamlit app
```

Enjoy using the Prompt Template App! 🚀
