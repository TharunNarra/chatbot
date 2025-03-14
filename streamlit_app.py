import streamlit as st
from openai import OpenAI
import google.generativeai as genai

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT models and Google's Gemini models to generate responses. "
    "To use this app, you need to provide an OpenAI or Gemini API key. "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Sidebar for model selection
st.sidebar.header("Model Selection")
model = st.sidebar.selectbox(
    "Choose a model:",
    [
        "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo",
        "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"
    ]
)

# Ask user for their API key
api_key = st.text_input("API Key", type="password")
if not api_key:
    st.info("Please add your API key to continue.", icon="🗝️")
else:
    # Determine which API to use based on model selection
    if "gemini" in model:
        genai.configure(api_key=api_key)
    else:
        client = OpenAI(api_key=api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response based on the selected model
        if "gemini" in model:
            gemini_model = genai.GenerativeModel(model)
            response = gemini_model.generate_content(prompt).text
        else:
            stream = client.chat.completions.create(
                model=model,  # Use the selected model
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
