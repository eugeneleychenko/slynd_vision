import streamlit as st
import base64
import requests
from dotenv import load_dotenv
from dotenv import dotenv_values
import json

load_dotenv()
openai_api_key = dotenv_values(".env").get("OPENAI_API_KEY")

st.title("Image Chat with LLM")

# Initialize images_info in session state if it doesn't exist
if 'images_info' not in st.session_state:
    st.session_state.images_info = []

# Fetch and load the JSON data from the provided URL
json_url = "https://opensheet.elk.sh/1Y18J6t_XzWQuWKAv-LOl3llpvRE9CIldm3d5wMzdiqo/1"
response = requests.get(json_url)
if response.status_code == 200:
    data = response.json()
    # Extract the image URLs and PRC Codes
    images_info = [{"url": item["Preview Hosted URL"], "prc_code": item["PRC Code"]} 
                   for item in data if item["Preview Hosted URL"]]

    # Update the images_info in session state
    st.session_state.images_info = images_info[:29]  # Limit to the first 29 items

    # Display images and PRC Codes using the stored information
    for item in st.session_state.images_info:
        st.sidebar.image(item["url"], use_column_width=True)
        st.sidebar.write(f"PRC Code: {item['prc_code']}")
else:
    st.error("Failed to load JSON data.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question about the images:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        if st.session_state.get('uploaded_image_urls'):
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
                            "image_url": item["url"]
                        } for item in st.session_state.images_info[:29]  # Limit to the first 29 images
                    
                    ]
                }
            ],
            "max_tokens": 1000,
                "temperature": 0
            }
            print("Payload sent to OpenAI:", json.dumps(payload, indent=2))

            # Make the API request
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            response_data = response.json()
            print("Response from OpenAI:", json.dumps(response_data, indent=2))
            full_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response found.")
        else:
            full_response = "No images available to chat about."

        message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
