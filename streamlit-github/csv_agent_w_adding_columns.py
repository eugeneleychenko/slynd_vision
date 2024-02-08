from langchain_experimental.agents import create_csv_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import streamlit as st


def main():
    load_dotenv()

    # Load the OpenAI API key from the environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None or openai_api_key == "":
        st.error("OPENAI_API_KEY is not set. Please set it in your environment variables.")
        st.stop()
    
    st.set_page_config(page_title="Ask your CSV")
    st.title("Ask your CSV 📈")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Preload the CSV agent with a default CSV file if not already loaded
    if "csv_agent" not in st.session_state:
        with open("Slynd.csv", "rb") as default_csv_file:
            st.session_state.csv_agent = create_csv_agent(
                ChatOpenAI(temperature=0.3, model="gpt-4-1106-preview"), default_csv_file, verbose=True
            )

    # Allow user to upload a new CSV file
    csv_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")
    if csv_file is not None:
        st.session_state.csv_agent = create_csv_agent(
            ChatOpenAI(temperature=0, api_key=openai_api_key), csv_file, verbose=True
        )

    # Accept user input
    if user_question := st.chat_input("Ask a question about your CSV:"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_question})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_question)

        # Display agent response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner(text="In progress..."):
                response = st.session_state.csv_agent.run(user_question)
                message_placeholder.markdown(response)
                # Add agent response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()