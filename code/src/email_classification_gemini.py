from classification_prompt import classify_request_type, outputJsonFormat
import google.generativeai as genai
import json

classification_data = classify_request_type()
def classify_email(subject, body, attachment_text):
    """Classifies email content using a generative AI model."""

    genai.configure(api_key="AIzaSyBgD85PrdkN2M8bFQA0HYOreAFkc_Z-TSA")  # Ensure API key is configured
    model = genai.GenerativeModel("gemini-2.0-flash")  # Choose the appropriate model

    combined_text = f"Subject: {subject}\nBody: {body}\nAttachments: {attachment_text}"
    prompt = f"""Read the content below and classify the content based on the given classifications. 

    {classification_data}
    Also provide the confidence score for each classification.
    
    **Content to Analyze:**
    Subject: {subject}
    Body: {body}
    Attachments: {attachment_text}

    **Output JSON Format:**
    {outputJsonFormat()}
    **Rules:**
    1. Provide confidence scores for  each classification
    2. Include reasoning for each classifications
    3. Use 'Not Found' for missing information
    4. Maintain all fields from both original output formats
    5. Follow strict JSON formatting

    Return only the JSON response with your analysis."""
    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().lstrip("```json").rstrip("```")
        # Now parse the cleaned string as JSON
        json_response = json.loads(cleaned_response)
        # print(json_response)
        return json_response
    except Exception as e:
        print(f"Error classifying email: {e}")
        return None  # Or handle the error as appropriate

def update_request_for_duplicate(subject, body, attachment_text, previous_json_response):
    genai.configure(api_key="AIzaSyBgD85PrdkN2M8bFQA0HYOreAFkc_Z-TSA")  # Ensure API key is configured
    model = genai.GenerativeModel("gemini-2.0-flash")  # Choose the appropriate model
    prompt_duplicate_check = f"""You have previously classified a service request email and its attachments, resulting in the following JSON output:

        previous_json_response :
            {previous_json_response}

        A new email has been received, which is a reply or forward to the original. Here are the details of the new email:

        **Subject:** {subject}
        **Content:** {body}
        **Attachments:** {attachment_text}

        Analyze this new email in the context of the previous email and its classification. Determine if this new email provides any updates or additional information to the existing service request.

        If the new email contains relevant updates (e.g., changes in amount, new dates, additional details, clarification on the request, or confirmation), update the corresponding fields in the `extracted_information` section of the `previous_json_response`. If the new email indicates a change in the primary request type or introduces a new request type, update the `request_types` list accordingly, providing new confidence scores and reasoning.

        If the new email does not provide any significant updates or is merely an acknowledgement or a minor comment without new actionable information, you can return the original `previous_json_response` without modifications.

        Output the updated JSON response object. Ensure the structure remains the same as the `previous_json_response`. If the new email clearly indicates a completely new and unrelated service request, you should generate a new JSON response object following the same format as before, but based on the content of the new email. In this case, also include a top-level field `"is_new_request": true`. Otherwise, `"is_new_request"` should be `false` or not present.
        """
    try:
        response = model.generate_content(prompt_duplicate_check)
        cleaned_response = response.text.strip().lstrip("```json").rstrip("```")
        json_response = json.loads(cleaned_response)
        return json_response
    except Exception as e:
        print(f"Error classifying email: {e}")
        return None  # Or handle the error as appropriate