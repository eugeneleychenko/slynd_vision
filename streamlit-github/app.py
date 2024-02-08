import streamlit as st
import base64
import requests
from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv()
openai_api_key = dotenv_values(".env").get("OPENAI_API_KEY")



st.title("Image Chat with LLM")

# Initialize chat history and uploaded image
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Allow user to upload an image
uploaded_files = st.file_uploader("Upload images to chat about (up to 29)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
if uploaded_files:
    base64_images = [base64.b64encode(uploaded_file.getvalue()).decode('utf-8') for uploaded_file in uploaded_files]
    st.session_state.uploaded_images = base64_images
    for uploaded_file, base64_image in zip(uploaded_files, base64_images):
        st.sidebar.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

# Accept user input
if prompt := st.chat_input("Ask a question about the uploaded images:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        if st.session_state.get('uploaded_images'):
            # Prepare headers and payload for the API request
            api_key = openai_api_key
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ] + [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image}"
                                }
                            } for image in st.session_state.uploaded_images[:4]  # Limit to the first 4 images
                        ]
                    }
                ],
                "max_tokens": 800,
                "temperature": 0
            }

            # Make the API request
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            response_data = response.json()
            full_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response found.")

        else:
            full_response = "Please upload an image to chat about."

        message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
