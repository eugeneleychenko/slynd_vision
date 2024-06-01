# from langchain_experimental.agents import create_csv_agent
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import StreamlitCallbackHandler
from dotenv import load_dotenv
from langchain_core.exceptions import OutputParserException
import os
import streamlit as st
import pandas as pd
import pyautogui

openai_api_key = st.secrets["OPENAI_API_KEY"]

def main():
    load_dotenv()

    # Load the OpenAI API key from the environment variable
    # openai_api_key = os.getenv("OPENAI_API_KEY")
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

    
    # Allow user to upload a new CSV file
    csv_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")
    if csv_file is not None:
        dataframe = pd.read_csv(csv_file)
        st.session_state.csv_agent = create_pandas_dataframe_agent(
            # ChatOpenAI(temperature=0, api_key=openai_api_key, model="gpt-4-0613"), dataframe, verbose=True
            ChatOpenAI(temperature=0, api_key=openai_api_key, model="gpt-4-turbo"), dataframe, verbose=True
        )
        
    sidebar_container = st.sidebar.container()
    st_callback = StreamlitCallbackHandler(sidebar_container)
    
  

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
                thoughts = []
                try:
                    # Call the run method correctly as per documentation
                    response = st.session_state.csv_agent.run(input={"query": user_question}, callbacks=[st_callback], return_thoughts=True)
                except OutputParserException as e:
                    st.error(f"Failed to parse the model's output: {str(e)}")
                    response = "There was an error processing your request. Please try again."
                    
                     # Display intermediate thoughts
                for thought in thoughts:
                    st.markdown(f"**Thought:** {thought}")
                message_placeholder.markdown(response)
                # Add agent response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
if __name__ == "__main__":
    main()
