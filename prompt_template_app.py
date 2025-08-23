"""
Streamlit Application for Prompt Template Management

This application provides a user interface for managing prompt templates. The application has the following capabilities:

- **Create and Edit Prompt Templates**: Users can create new prompt templates, edit existing ones, or delete templates.
- **Use Templates to Generate Prompts**: Users can select a template, input variables, and generate formatted prompts.
- **Display Prompting Principles**: Users can view principles and guidelines for effective prompting.

Key Components:
1. **Streamlit Input Fields**: Dynamic creation of input fields for template variables.
2. **Template Management**: Functions to retrieve, create, update, and delete templates from a database.
3. **Prompt Template Handling**: Use of `ChatPromptTemplate` to format and process input data.

Functions:
    - `create_input_fields(variables)`: Creates Streamlit input fields for string variables.
    - `get_templates()`: Retrieves templates by topic from the database.
    - `main()`: Main function to run the Streamlit app.

Workflow:
- **Template Editing**: Users select "Edit Template" to modify existing templates or create new ones. Input fields for template details (name, topic, purpose, template content) are provided, along with options to save or delete the template.
- **Using Templates**: Users select "Use Template" to pick a template and provide input variables. The formatted prompt is generated and displayed.
- **Prompting Principles**: Users can view predefined principles for creating effective prompts.

Dependencies:
- `streamlit`: For creating the web interface.
- `langchain.prompts.ChatPromptTemplate`: For handling prompt templates.
- `prompt_template_database.session` and `prompt_template_database.PromptTemplate`: For database interactions.
- `text_definitions.prompting_principles`: For displaying prompting guidelines.

Usage:
- Run the script in a Streamlit environment to start the application.
- Navigate through the sidebar options to manage templates or generate prompts.

"""

import streamlit as st
from prompt_template_database import session, PromptTemplate
from text_definitions import prompting_principles
from langchain.prompts import ChatPromptTemplate


def create_input_fields(template):
    """
    Create Streamlit input fields for string variables.

    Args:
        template (str): The prompt template containing input variables.

    Returns:
        dict: A dictionary with variable names as keys and their corresponding
              Streamlit input values.
    """
    prompt_template = ChatPromptTemplate.from_template(template)

    variables = prompt_template.messages[0].prompt.input_variables
    inputs = {}
    for variable in variables:
        var_name = variable
        if len(variables) > 1:
            inputs[var_name] = st.text_input(var_name)
        else:
            inputs[var_name] = st.text_area(var_name, height=200)
    return inputs


def create_inline_input_fields(template):
    """
    Create inline input fields within the template text.

    Args:
        template (str): The prompt template containing input variables.

    Returns:
        dict: A dictionary with variable names as keys and their corresponding
              Streamlit input values.
    """
    prompt_template = ChatPromptTemplate.from_template(template)
    variables = prompt_template.messages[0].prompt.input_variables
    
    if not variables:
        st.write("**Template:**")
        st.text_area("Template Content", value=template, height=200, disabled=True)
        return {}
    
    # Split template by variables and create inline inputs
    import re
    
    # Create a pattern to match variable placeholders
    var_pattern = r'\{([^}]+)\}'
    
    # Find all variables in the template
    matches = list(re.finditer(var_pattern, template))
    
    if not matches:
        st.write("**Template:**")
        st.text_area("Template Content", value=template, height=200, disabled=True)
        return {}
    
    st.write("**Fill in the template variables:**")
    
    inputs = {}
    
    # Create input fields for each variable
    for i, match in enumerate(matches):
        var_name = match.group(1)
        
        # Create input field with better labeling
        if len(variables) > 1:
            input_value = st.text_input(f"**{var_name}**", key=f"inline_{var_name}_{i}", placeholder=f"Enter {var_name}")
        else:
            input_value = st.text_area(f"**{var_name}**", key=f"inline_{var_name}_{i}", placeholder=f"Enter {var_name}", height=100)
        
        inputs[var_name] = input_value
    
    # Show the template with variables highlighted
    st.write("**Template Preview:**")
    highlighted_template = template
    for var_name in variables:
        highlighted_template = highlighted_template.replace(f"{{{var_name}}}", f"**`[{var_name}]`**")
    
    st.markdown(highlighted_template)
    
    return inputs


def get_template_names(template_use=False):
    """
    Retrieve templates by topic from the database.

    Returns:
        list: A list of prompt templates filtered by the selected topic.
    """
    topics = PromptTemplate.get_topics(session)
    selected_topic = st.sidebar.selectbox(
        "Select Topic", ["All"] + topics
    )  # Add dropdown for selecting topic
    if selected_topic == "All":
        templates = PromptTemplate.get_all_templates(session)
    else:
        templates = PromptTemplate.get_templates_by_topic(session, selected_topic)

    if not template_use:
        template_names = ["New Template"]  # Make "New Template" the first option
        template_names.extend([template.name for template in templates])
    else:
        template_names = [template.name for template in templates]

    return template_names


def main():
    """
    Main function to run the Streamlit app.

    Initializes the session state and displays the sidebar and main content based on user actions.
    """

    st.sidebar.title("Select Action")

    action = st.sidebar.radio(
        "Action", ["Edit Template", "Use Template", "Prompting Principles"]
    )

    if action == "Prompting Principles":
        st.markdown(prompting_principles)

    if action == "Edit Template":
        st.sidebar.title("Select Prompt Template")
        template_names = get_template_names()
        selected_template_name = get_selected_template_name(template_names)

        if selected_template_name == "New Template":
            create_template(template_names)
        else:
            maintain_template(template_names, selected_template_name)

    elif action == "Use Template":
        use_template()


def get_selected_template_name(template_names):
    """
    Get the name of the selected template.

    Parameters:
    - template_names (list): A list of strings representing the names of available templates.

    Returns:
    - str: The name of the selected template.
    """
    selected_template_name = st.sidebar.selectbox("Template", template_names)
    return selected_template_name


def use_template():
    """
    Handle the use of a selected prompt template.

    Displays the template with inline input fields and shows the formatted prompt.
    """
    st.sidebar.title("Select Prompt Template")
    template_names = get_template_names(template_use=True)

    selected_template_name = st.sidebar.selectbox("Template", template_names)

    selected_template = PromptTemplate.get_by_name(session, selected_template_name)

    if selected_template:
        display_template(selected_template)
        
        # Create inline input fields within the template
        inputs = create_inline_input_fields(selected_template.template)
        
        if st.button("Generate Prompt"):
            formatted_message = get_formatted_message(selected_template, inputs)
            st.text_area(
                label="Generated Prompt", value=formatted_message, height=500, max_chars=None
            )


def display_template(selected_template):
    """
    Display the selected template's details.

    Args:
        selected_template (PromptTemplate): The selected prompt template.
    """
    st.write(f"Topic: {selected_template.topic}")
    st.write(f"Name: {selected_template.name}")
    st.write(f"Purpose: {selected_template.purpose}")
    st.write(f"Template: {selected_template.template}")


def get_formatted_message(selected_template, inputs):
    """
    Format the message based on the selected template and input values.

    Args:
        selected_template (PromptTemplate): The selected prompt template.
        inputs (dict): The dictionary of input values.

    Returns:
        str: The formatted message.
    """
    input_values = {}
    for var_name, var_value in inputs.items():
        input_values[var_name] = var_value
    prompt = ChatPromptTemplate.from_template(selected_template.template)
    formatted_messages = prompt.format_messages(**input_values)
    formatted_message = formatted_messages[0].content
    return formatted_message


def maintain_template(template_names, selected_template_name):
    """
    Maintain the selected template, providing options to update or delete it.

    Args:
        template_names (list): A list of all template names.
        selected_template_name (str): The name of the selected template.
    """
    selected_template = PromptTemplate.get_by_name(session, selected_template_name)
    if selected_template:
        topic, name, purpose, template = get_template_values(
            selected_template
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save", key="save_button"):
                update_template(
                    template_names,
                    selected_template_name,
                    selected_template,
                    topic,
                    name,
                    purpose,
                    template,
                )
        with col2:
            delete_template(selected_template)


def get_template_values(selected_template):
    """
    Get the values of the selected template's fields.

    Args:
        selected_template (PromptTemplate): The selected prompt template.

    Returns:
        tuple: A tuple containing the topic, name, purpose, and template content.
    """
    topic = st.text_input("Topic", value=selected_template.topic)
    name = st.text_input("Name", value=selected_template.name)
    purpose = st.text_area("Purpose", value=selected_template.purpose)
    template = st.text_area("Template", value=selected_template.template, height=400)
    return topic, name, purpose, template


def update_template(
    template_names,
    selected_template_name,
    selected_template,
    topic,
    name,
    purpose,
    template,
):
    """
    Update the selected template with new values.

    Args:
        template_names (list): A list of all template names.
        selected_template_name (str): The name of the selected template.
        selected_template (PromptTemplate): The selected prompt template instance.
        topic (str): The updated topic.
        name (str): The updated name.
        purpose (str): The updated purpose.
        template (str): The updated template content.
    """
    if not topic:
        st.error("Please enter a topic for the template!")
    if not name:
        st.error("Please enter a name for the template!")
    else:
        if name != selected_template_name and name in template_names[1:]:
            st.error("A template with this name already exists!")
        else:
            selected_template.name = name
            selected_template.purpose = purpose
            selected_template.template = template
            session.commit()
            st.success("Changes saved successfully!")


def delete_template(selected_template):
    """
    Delete the selected template from the database.

    Args:
        selected_template (PromptTemplate): The selected prompt template to be deleted.
    """
    if st.button("Delete", key="delete_button") and selected_template:
        session.delete(selected_template)
        session.commit()
        st.success("Template deleted successfully!")


def create_template(template_names):
    """
    Create a new template based on user input.

    Args:
        template_names (list): A list of existing template names.
    """
    st.empty()
    name = st.text_input("Name")
    topic = st.text_input("Topic")
    purpose = st.text_area("Purpose")
    template = st.text_area(
        "Template", height=250
    )  # Make the text area expand vertically
    if st.button("Save New Template"):
        if not topic:
            st.error("Please enter a topic for the template!")
        if not name:
            st.error("Please enter a name for the template!")
        else:
            if name in template_names[1:]:
                st.error("A template with this name already exists!")
            else:
                new_template = PromptTemplate(
                    topic=topic,
                    name=name,
                    purpose=purpose,
                    template=template,
                    use_web_search=False,  # Default value
                )
                session.add(new_template)
                session.commit()
                st.success("Template saved successfully!")


if __name__ == "__main__":
    main()
