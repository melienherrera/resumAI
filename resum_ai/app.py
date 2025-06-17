import streamlit as st
from langflow.load import run_flow_from_json
import tempfile
import os
from dotenv import load_dotenv
import requests

# Load env vars
load_dotenv()
openai_api_key = st.secrets["OPENAI_API_KEY"]
astra_db_token = st.secrets["ASTRA_DB_APPLICATION_TOKEN"]
astra_endpoint = st.secrets["ASTRA_DB_API_ENDPOINT"]

st.markdown(
    """
    <style>
    .main {
        background-color: #F7729C;
    }
    .title {
        font-size: 3em;
        color: #4CAF50;
    }
    .subtitle {
        font-size: 1.5em;
        color: #555555;
    }
    .subtext {
        font-size: 1em;
        color: #777777;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Get the current directory
current_dir = os.path.dirname(__file__)

# Construct the file path 
resume_image = os.path.join(current_dir, 'resume.png')

# Title of the app
# Center the title, header, image, and input form
st.markdown("<h1 style='text-align: center;'>ResumAI</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Optimize your job searching with ResumAI</h2>", unsafe_allow_html=True)

st.markdown("<h6 style='text-align: center;'>Upload your resume and enter your desired role to get personalized job recommendations</h6>", unsafe_allow_html=True)


st.image(resume_image, width=650, use_container_width='auto')

# Center the input form
desired_role = st.text_input("Desired Role:", key="desired_role", help="Enter the job role you are looking for.")

# file upload
temp_file_path = None
uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name


def run_langflow_api(input_value):
    url = "http://127.0.0.1:7860/api/v1/run/625d565a-9e49-4cc5-8799-260cb97a31c0"  # Your Langflow flow endpoint
    payload = {
        "input_value": input_value,
        "output_type": "chat",
        "input_type": "chat",
        "File-0Pm7f": {
            "path": f"{temp_file_path}",
            "silent_errors": False
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request error: {e}"}
    except ValueError as e:
        return {"error": f"Response parsing error: {e}"}

# Submit
if st.button("Submit"):
  
  st.write(f"Your desired role is: {desired_role}") 
  st.write(f"Thank you for submitting the form 🙏") 

  with st.spinner('Loading your results...'):
    result = run_langflow_api(desired_role)
    if "error" in result:
        st.error(result["error"])
    else:
      st.write(result["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"])
