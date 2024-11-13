import streamlit as st
from langflow.load import run_flow_from_json
import tempfile
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()
openai_api_key = os.environ["OPENAI_API_KEY"]
astra_db_token = os.environ["ASTRA_DB_APPLICATION_TOKEN"]
astra_endpoint = os.environ["ASTRA_DB_API_ENDPOINT"]

# Title of the app
# Center the title, header, image, and input form
st.markdown("<h1 style='text-align: center;'>ResumAI</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Optimize your job searching with ResumAI</h2>", unsafe_allow_html=True)

st.image("resume.png", width=650, use_container_width='auto')

# Center the input form
desired_role = st.text_input("Desired Role:", key="desired_role", help="Enter the job role you are looking for.")

# file upload
temp_file_path = None
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name

# Langflow Implementation
TWEAKS = {
  "ParseData-EA01z": {},
  "Prompt-cwII3": {
     # "job_role": "Data Scientist",
  },
  "ChatOutput-T2xaq": {},
  "OpenAIEmbeddings-AGnvK": {
    "openai_api_key": f"{openai_api_key}",
  },
  "OpenAIModel-GM3Ha": {
    "openai_api_key": f"{openai_api_key}",
  },
  "File-S8g3y": {  
    "path": f"{temp_file_path}",
    "silent_errors": False
  },
  "ParseData-Rt5pZ": {},
  "ChatInput-ZffxB": {
      "input_value": f"{desired_role}",
      # "input_value": "Data Scientist",
  },
  "AstraDB-T7QLI": {
      "api_endpoint": f"{astra_endpoint}",
      "token": f"{astra_db_token}",
  },
  "Prompt-qGHGy": {},
  "OpenAIModel-umK6j": {
    "openai_api_key": f"{openai_api_key}",
  }
}

# Submit
if st.button("Submit"):
  st.write(f"Your desired role is: {desired_role}") 
  st.write(f"Thank you for submitting the form 🙏") 
  
  with st.spinner('Loeading your results...'):
    result = run_flow_from_json(flow="Resume Assistant.json",
                input_value=f"{desired_role}",
                fallback_to_env_vars=True, # False by default
                tweaks=TWEAKS)

  message = result[0].outputs[0].results['message'].data['text']
  st.write(message)

