import os
import io
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts.pipeline import PipelinePromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
import json
from utils.ai_utils import get_gemini_model
from utils.json_utils import open_json_file
from utils.json_utils import clean_ai_response

os.environ["GOOGLE_API_KEY"] = "AIzaSyBgD85PrdkN2M8bFQA0HYOreAFkc_Z-TSA"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def getClassificationData():
    return open_json_file('files/classifications.json')

def getClassificationResultData():
    return open_json_file('files/classification_result.json')

def getExtractionData():
    return open_json_file('files/extraction_result.json')

def classify_email(subject, body, attachment_text):

    classification_json = getClassificationData()
    output_json_example = getClassificationResultData()
    additional_information_json_format = getExtractionData()

    print("*" * 50)

    email_content = """
        ** Email Content **
            Subject: {subject}
            Body: {body}
            Attachments: {attachment_text}

        Prioritise **Body** if there is any contradictions between the **Body** and **Attachments** for financial and banking information. 
        But if it is specified or hinted in the **Body** that we have to use **Attachment** then use ignore **Body** content for analysis and summary and use **Attachment**.
        Then Summarize the email content.
    """
    email_content_prompt = PromptTemplate.from_template(email_content)

    classification_content = """
        Consider the summary from previous step, Analyze the content and provide JSON array listing all the classifications from {classification_data} in the format given below with the fitting confidence score.
        Note: We want all of the classifications to be assessed and provided in the output.
    """
    classification_content_prompt = PromptTemplate.from_template(classification_content)

    classification_example = """
        **Output JSON Example**:
            classifications = {output_data}
        Also, add one status field in the JSON object with value "new".
        Note: sub_request_type are bound to the request_type and can not be mixed.
    """
    classification_example_prompt = PromptTemplate.from_template(classification_example)

    additional_content = """
        Also, provide all of the extra financial information from the email content provided above.
    """
    additional_content_prompt = PromptTemplate.from_template(additional_content)

    additional_example = """
        **Output JSON Format:**
            additional_fields = {additional_information_data}
        Note: We have to skip all the fields from this JSON that are not found in the email content. We need the output in single JSON format.
    """
    additional_example_prompt = PromptTemplate.from_template(additional_example)
    

    prompt = """
        {email_content}
        {classification_content}
        {classification_example}
        {additional_content}
        {additional_example}
    """
    full_prompt = PromptTemplate.from_template(prompt)

    input_prompts = [
        ("email_content", email_content_prompt),
        ("classification_content", classification_content_prompt),
        ("classification_example", classification_example_prompt),
        ("additional_content", additional_content_prompt),
        ("additional_example", additional_example_prompt),
    ]

    pipeline = PipelinePromptTemplate(final_prompt = full_prompt, pipeline_prompts = input_prompts)

    formattedPrompt = pipeline.format(
        subject=subject,
        body=body,
        attachment_text=attachment_text,
        classification_data=classification_json,
        output_data=output_json_example,
        additional_information_data=additional_information_json_format
    )

    response = llm.invoke(input=formattedPrompt)
    clean_result = clean_ai_response(response.content)
    print("Response - Classifications: ", clean_result)

    print("*" * 50)
    return clean_result