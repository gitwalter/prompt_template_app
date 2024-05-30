import streamlit as st
from prompt_template_database import session, PromptTemplate
from text_definitions import prompting_principles
from langchain.prompts import ChatPromptTemplate
from sqlalchemy import asc
from huggingface_chat import HuggingChatWrapper

# Function to create Streamlit input fields for string variables
def create_input_fields(variables):
    inputs = {}
    for variable in variables:
        var_name = variable
        inputs[var_name] = st.text_input(var_name)
    return inputs


# retrieve templates by topic from db
def get_templates():
    topics = PromptTemplate.get_topics(session)
    selected_topic = st.sidebar.selectbox(
        "Select Topic", ["All"] + topics
)  # Add dropdown for selecting topic
    if selected_topic == "All":
        templates = PromptTemplate.get_all_templates(session)
    else:
        templates= PromptTemplate.get_templates_by_topic(session,selected_topic)
        
    return templates


# Main function to run the Streamlit app
def main():
    st.sidebar.title("Select Action")

    action = st.sidebar.radio(
        "Action", ["Edit Template", "Use Template", "Prompting Principles"]
    )

    if action == "Prompting Principles":
        st.markdown(prompting_principles)
        

    if action == "Edit Template":
        st.sidebar.title("Select Prompt Template")
        
        templates = get_templates()
        template_names = ["New Template"]  # Make "New Template" the first option
        template_names.extend([template.name for template in templates])

        selected_template_name = st.sidebar.selectbox("Template", template_names)

        if selected_template_name == "New Template":
            selected_template = None
            st.empty()            
            name = st.text_input("Name")
            topic = st.text_input("Topic")
            purpose = st.text_area("Purpose")
            use_web_search = st.checkbox("Use Web Search")
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
                            use_web_search=use_web_search
                        )
                        session.add(new_template)
                        session.commit()
                        st.success("Template saved successfully!")
        else:
            selected_template = PromptTemplate.get_by_name(session,selected_template_name)
            if selected_template:
                topic = st.text_input("Topic", value=selected_template.topic)
                name = st.text_input("Name", value=selected_template.name)
                purpose = st.text_area("Purpose", value=selected_template.purpose)
                use_web_search = st.checkbox("Use Web Search", value=selected_template.use_web_search)
                template = st.text_area(
                    "Template", value=selected_template.template, height=400
                )  # Make the text area expand vertically
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Save", key="save_button"):
                        if not topic:
                            st.error("Please enter a topic for the template!")
                        if not name:
                            st.error("Please enter a name for the template!")
                        else:
                            if (
                                name != selected_template_name
                                and name in template_names[1:]
                            ):
                                st.error("A template with this name already exists!")
                            else:
                                selected_template.name = name
                                selected_template.purpose = purpose
                                selected_template.use_web_search = use_web_search
                                selected_template.template = template
                                session.commit()
                                st.success("Changes saved successfully!")
                with col2:
                    if st.button("Delete", key="delete_button"):
                        if selected_template:
                            session.delete(selected_template)
                            session.commit()
                            st.success("Template deleted successfully!")
    elif action == "Use Template":
        st.sidebar.title("Select Prompt Template")
        templates = get_templates()
        template_names = [template.name for template in templates]

        selected_template_name = st.sidebar.selectbox("Template", template_names)

        selected_template = PromptTemplate.get_by_name(session,selected_template_name)        

        if selected_template:
            st.write(f"Topic: {selected_template.topic}")
            st.write(f"Name: {selected_template.name}")
            st.write(f"Purpose: {selected_template.purpose}")
            st.write(f"Template: {selected_template.template}")


            chat_wrapper = HuggingChatWrapper()
            model_names = chat_wrapper.get_available_models()
            chat_wrapper.reset()
         # Display available models in selectbox
            
            model_name = st.sidebar.selectbox("Select Model", model_names)
                        
            prompt_template = ChatPromptTemplate.from_template(
                selected_template.template
            )
            input_variables = prompt_template.messages[0].prompt.input_variables
            inputs = create_input_fields(input_variables)

            

            col1, col2 = st.columns(2)
            with col1:
                use_web_search = st.checkbox("Use Web Search", selected_template.use_web_search)                            
                    
            with col2:
                if not st.checkbox("Keep chat on Server"):
                    chat_wrapper.reset()
                
            if st.button("Submit"):                
                input_values = {}
                for var_name, var_value in inputs.items():
                    input_values[var_name] = var_value
                prompt = ChatPromptTemplate.from_template(selected_template.template)
                formatted_messages = prompt.format_messages(**input_values)
                formatted_message = formatted_messages[0].content
                st.text_area(label="Prompt", value=formatted_messages,height=500, max_chars=None)
                chat_wrapper = HuggingChatWrapper()
                chat_wrapper.switch_model(model_name)            
                query_result = chat_wrapper.chat(formatted_message, use_web_search)                
                st.text_area(label="LLM Response",value=query_result,height=500)                
                
                for source in query_result.web_search_sources:
                    st.markdown(source.title + ": " + source.link)
                

if __name__ == "__main__":
    main()
