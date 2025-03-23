import google.generativeai as genai
import json

def update_request_for_duplicate(subject, body, attachment_text, previous_json_response):
    genai.configure(api_key="AIzaSyBgD85PrdkN2M8bFQA0HYOreAFkc_Z-TSA")  # Ensure API key is configured
    model = genai.GenerativeModel("gemini-2.0-flash")  # Choose the appropriate model
    prompt_duplicate_check = f"""
        You have previously classified a service request email and its attachments, resulting in the following JSON output:

        previous_json_response :
            {previous_json_response}

        A new email has been received, which is a reply or forward to the original. Here are the details of the new email:

        **Subject:** {subject}
        **Content:** {body}
        **Attachments:** {attachment_text}

        Analyze this new email in the context of the previous email and its classification. Determine if this new email provides any updates or additional information to the existing service request.

        If the new email contains relevant updates (e.g., changes in amount, new dates, additional details, clarification on the request, or confirmation), update the corresponding fields of the `previous_json_response`. If the new email indicates a change in the primary request type or introduces a new request type, update the `request_types` list accordingly, providing new confidence scores and reasoning.

        If the new email does not provide any significant updates or is merely an acknowledgement or a minor comment without new actionable information, you can return the original `previous_json_response` without modifications.

        Output the updated JSON response object. Ensure the structure remains the same as the `previous_json_response`. If the new email clearly indicates a completely new and unrelated service request, you should generate a new JSON response object following the same format as before, but based on the content of the new email. In this case, also include a top-level field `"is_new_request": true`. Otherwise, `"is_new_request"` should be `false` or not present.
        """
    try:
        response = model.generate_content(prompt_duplicate_check)
        cleaned_response = response.text.strip().lstrip("```json").rstrip("```")
        print("Updated Response: ", cleaned_response)
        json_response = json.loads(cleaned_response)
        return json_response
    except Exception as e:
        print(f"Error classifying email: {e}")
        return None  # Or handle the error as appropriate