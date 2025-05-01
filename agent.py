import os
import json
from typing import List, Dict, Any
import autogen
from autogen import AssistantAgent, UserProxyAgent

# Assuming config_list is defined elsewhere for your LLM configuration
config_list = []  # Replace with your actual config_list

try:
    import google.generativeai as genai
except ImportError:
    print("Error: The google-generativeai library is not installed. Please install it using 'pip install google-generativeai'")
    raise

# --- Utility Function for MIME Type Detection ---
def _get_mime_type(file_path: str) -> str:
    file_extension = os.path.splitext(file_path)[1].lower()
    mime_types = {
        ".txt": "text/plain",
        ".mp4": "video/mp4",
        ".mpeg": "video/mpeg",
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".pdf": "application/pdf",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        # Add more MIME types as needed
    }
    return mime_types.get(file_extension, "application/octet-stream")

# --- Function to Get Content with Gemini ---
def get_content_with_gemini(file_path, prompt_text):
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()

        mime_type = _get_mime_type(file_path)

        contents = [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": file_data
                        }
                    },
                    {
                        "text": prompt_text
                    }
                ]
            }
        ]

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(contents)

        if response.prompt_feedback and response.prompt_feedback.block_reason:
            print(f"Error: The API returned a blocked response: {response.prompt_feedback.block_reason}")
            return None

        return response.text if response.text else "No relevant information found."

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- Utility Function for Storing Data ---
def store_data_to_disk(filename: str, data: List[Dict[str, Any]]) -> str:
    """Simulates storing data to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        return f"Data successfully stored in '{filename}'."
    except Exception as e:
        return f"Error storing data to '{filename}': {e}"

# --- Specialized Assistant Agents for File Processing ---
class FileProcessingAgent(AssistantAgent):
    def __init__(self, name, system_message, **kwargs):
        super().__init__(
            name=name,
            system_message=system_message,
            function_map={"extract_from_file": get_content_with_gemini},
            **kwargs
        )

audio_processor_agent = FileProcessingAgent(
    name="AudioProcessorAgent",
    llm_config={"config_list": config_list},
    system_message="You are an expert in transcribing audio files and extracting relevant information. Use the 'extract_from_file' tool when you receive an audio file."
)

video_processor_agent = FileProcessingAgent(
    name="VideoProcessorAgent",
    llm_config={"config_list": config_list},
    system_message="You are an expert in extracting audio from video and transcribing it to text, then extracting relevant information. Use the 'extract_from_file' tool when you receive a video file."
)

image_processor_agent = FileProcessingAgent(
    name="ImageProcessorAgent",
    llm_config={"config_list": config_list},
    system_message="You are an expert in extracting text from images using OCR and then extracting relevant information. Use the 'extract_from_file' tool when you receive an image file."
)

text_processor_agent = FileProcessingAgent(
    name="TextProcessorAgent",
    llm_config={"config_list": config_list},
    system_message="You are an expert in processing text data to extract relevant information. Use the 'extract_from_file' tool when you receive a text-based file."
)

# --- Aggregator Agents (as you defined them) ---
manual_form_aggregator_config = {
    "name": "Manual_Form_Aggregator",
    "llm_config": config_list,
    "system_message": """You orchestrate the processing of manual forms. You can ask the user for details about the forms and coordinate with other potential agents (like OCR or NLP specialists - which are not implemented here) to extract and structure the data. For now, assume the data is already extracted and provided."""
}
manual_form_aggregator_agent = autogen.AssistantAgent(**manual_form_aggregator_config)

service_now_aggregator_config = {
    "name": "ServiceNow_Aggregator",
    "llm_config": config_list,
    "system_message": """You are skilled in retrieving data from ServiceNow. You understand ServiceNow API concepts. When instructed, you will formulate Python code using the 'requests' library to query the ServiceNow API based on the user's needs. You will need the ServiceNow instance URL, API credentials, and details of the tables and fields to query. You will then instruct the Code Executor to run this code."""
}
service_now_aggregator_agent = autogen.AssistantAgent(**service_now_aggregator_config)

google_forms_aggregator_config = {
    "name": "Google_Forms_Aggregator",
    "llm_config": config_list,
    "system_message": """You are designed to collect responses from Google Forms via Google Sheets API. You will need the key of the Google Sheet. You will then formulate Python code using the 'gspread' library to retrieve the data and instruct the Code Executor to run it."""
}
google_forms_aggregator_agent = autogen.AssistantAgent(**google_forms_aggregator_config)

m365_forms_aggregator_config = {
    "name": "M365_Forms_Aggregator",
    "llm_config": config_list,
    "system_message": """You are specialized in collecting responses from Microsoft Forms via the Microsoft Graph API. You will need the form ID and appropriate Azure AD credentials. You will formulate Python code using the 'requests' library to interact with the Graph API and instruct the Code Executor to run it."""
}
m365_forms_aggregator_agent = autogen.AssistantAgent(**m365_forms_aggregator_config)

facebook_post_aggregator_config = {
    "name": "Facebook_Post_Aggregator",
    "llm_config": config_list,
    "system_message": """You are tasked with collecting data from Facebook posts using the Facebook Graph API. You will need a Page ID or user ID and a valid access token with the necessary permissions. You will formulate Python code using the 'requests' library or a Facebook SDK to retrieve post data and instruct the Code Executor to run it."""
}
facebook_post_aggregator_agent = autogen.AssistantAgent(**facebook_post_aggregator_config)

instagram_content_aggregator_config = {
    "name": "Instagram_Content_Aggregator",
    "llm_config": config_list,
    "system_message": """You are designed to collect content from Instagram using the Instagram Graph API. You will need an Instagram Business account ID and a valid access token with the required permissions. You will formulate Python code using the 'requests' library or the Facebook SDK to retrieve content data and instruct the Code Executor to run it."""
}
instagram_content_aggregator_agent = autogen.AssistantAgent(**instagram_content_aggregator_config)

# --- Data Extraction and Storage Agent ---
data_extractor_agent = AssistantAgent(
    name="DataExtractorAgent",
    llm_config={"config_list": config_list},
    system_message="You receive data (text or structured) and a prompt to extract key-value pairs in a specific format (e.g., JSON). You will carefully read the data and extract the information according to the prompt. Once extracted, you will call the 'store_data' function to save it.",
    function_map={"store_data": store_data_to_disk}
)

# --- Data Analysis Agent ---
data_analysis_agent = AssistantAgent(
    name="DataAnalysisAgent",
    llm_config={"config_list": config_list},
    system_message="You are an expert in data analysis. You can ask the User Proxy to provide data (which it will retrieve from the stored files) and then perform analysis using Python code (which you will ask the Code Executor to run). You can generate insights and potentially visualizations. When asking for data, be specific about the filename and the type of information you need."
)

# --- User Proxy Agent ---
user_proxy = UserProxyAgent(
    name="DataHandler",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=20,
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "data_collection"},
    function_map={"store_data": store_data_to_disk}
)

# --- Workflow Orchestration for Different Data Sources ---

def process_manual_forms(form_details, extraction_prompt, store_filename):
    user_proxy.initiate_chat(
        manual_form_aggregator_agent,
        message=f"Process these manual form details: {form_details}. {extraction_prompt}"
    )
    extracted_data = user_proxy.last_message()["content"]
    if extracted_data:
        user_proxy.initiate_chat(
            data_extractor_agent,
            message=f"Here is the data from the manual forms: {extracted_data}\n\nExtract key-value pairs based on this prompt: {extraction_prompt}. Store the result as '{store_filename}'."
        )
        print(user_proxy.last_message()["content"])

def process_service_now_data(query_details, extraction_prompt, store_filename):
    user_proxy.initiate_chat(
        service_now_aggregator_agent,
        message=f"Retrieve data from ServiceNow based on these details: {query_details}. {extraction_prompt}"
    )
    service_now_response = user_proxy.last_message()["content"]
    if service_now_response:
        user_proxy.initiate_chat(
            data_extractor_agent,
            message=f"Here is the data from ServiceNow: {service_now_response}\n\nExtract key-value pairs based on this prompt: {extraction_prompt}. Store the result as '{store_filename}'."
        )
        print(user_proxy.last_message()["content"])

# Similar functions can be created for Google Forms, M365 Forms, Facebook, and Instagram

def process_file_and_store(file_path, extraction_prompt, store_filename):
    file_name, file_ext = os.path.splitext(file_path)
    file_ext = file_ext.lower()

    if file_ext in ['.mp3', '.wav']:
        user_proxy.initiate_chat(
            audio_processor_agent,
            message=f"Process this audio file: {file_path}. {extraction_prompt}"
        )
        processed_content = user_proxy.last_message()["content"]
    elif file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.mpeg']:
        user_proxy.initiate_chat(
            video_processor_agent,
            message=f"Process this video file: {file_path}. {extraction_prompt}"
        )
        processed_content = user_proxy.last_message()["content"]
    elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
        user_proxy.initiate_chat(
            image_processor_agent,
            message=f"Process this image file: {file_path}. {extraction_prompt}"
        )
        processed_content = user_proxy.last_message()["content"]
    elif file_ext in ['.txt', '.pdf', '.csv', '.json', '.xml']:
        user_proxy.initiate_chat(
            text_processor_agent,
            message=f"Process this text-based file: {file_path}. {extraction_prompt}"
        )
        processed_content = user_proxy.last_message()["content"]
    else:
        print(f"Unsupported file type: {file_ext} for file: {file_path}")
        return

    if processed_content:
        user_proxy.initiate_chat(
            data_extractor_agent,
            message=f"Here is the processed content: {processed_content}\n\nExtract key-value pairs based on this prompt: {extraction_prompt}. Store the result as '{store_filename}'."
        )
        print(user_proxy.last_message()["content"])

def analyze_stored_data(filename, analysis_query):
    user_proxy.initiate_chat(
        data_analysis_agent,
        message=f"Retrieve the data stored in '{filename}' and perform the following analysis: {analysis_query}."
    )
    print(user_proxy.last_message()["content"])
