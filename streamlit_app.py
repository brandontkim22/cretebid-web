import base64
import os
import requests
import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
    "Upload a document (.pdf)", type=("pdf")
)

# Ask the user for a question via `st.text_area`.
question = st.text_area(
    "Now ask a question about the document!",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)


if uploaded_file:
    # Get contents of file in binary
    pdf_bytes = uploaded_file.getvalue()
    st.write("PDF uploaded successfully! Now sending to API...")
    
    api_ingest_url = "http://127.0.0.1:8000/v1/ingest/run"
    
    headers = {"Content-type": "application/json"}
    
    # Create JSON object
    encoded_pdf = encoded_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
    payload = {
            "project_id": "cretebid-example",
            "files": [
                {
                    "filename": "example.pdf",
                    "uri": f"data:application/pdf;base64,{encoded_pdf}",
                    "sha256": "string"
                }
            ],
        }
    
    try:
        response = requests.post(api_ingest_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            st.success("PDF sent to API successfully!")
            st.write("API Response:", response.json()) # Assuming API returns JSON
        else:
            st.error(f"Error sending PDF to API: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Network error or API not reachable: {e}")

# if uploaded_file and question:

#     # Process the uploaded file and question.
#     document = uploaded_file.read().decode()
#     messages = [
#         {
#             "role": "user",
#             "content": f"Here's a document: {document} \n\n---\n\n {question}",
#         }
#     ]

#     # Generate an answer using the OpenAI API.
#     stream = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=messages,
#         stream=True,
#     )

#     # Stream the response to the app using `st.write_stream`.
#     st.write_stream(stream)
