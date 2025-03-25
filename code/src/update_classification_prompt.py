import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts.pipeline import PipelinePromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
import google.generativeai as genai
from utils.json_utils import clean_ai_response

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
        
        json_response = json.loads(cleaned_response)
        print("Updated Response: ", json_response)
        print("Updated Response: ", type(json_response))
        return json_response
    except Exception as e:
        print(f"Error classifying email: {e}")
        return None  # Or handle the error as appropriate


def update_request_prompt(new_json_response, previous_json_response):
    print("Prompt:", "function called")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    email_content = PromptTemplate(
        input_variables=["new_json_response", "previous_json_response"],
        template = """
            We have two JSON objects representing service requests. The **new_json** represents the original service request, while the **previous_json** represents the updated service request.
            **new_json**:
                {new_json_response}
            **previous_json**:
                {previous_json_response}
            JSON objects are having two keys **classification**, **status**, **summary** and **additional_fields**.:
            - **classification** contains the **request_type** and respective **sub_request_types**, both along with their **confidence_score**.
            We use the combination of **request_type** and **sub_request_type** that have top **confidence_score** to create a service request.
            If both JSON objects have different top **confidence_score** for **request_type** and **sub_request_type** 
            OR if the additional fields are different, then we need to update the **status** key of **new_json** to **update**.
            Else if both JSON objects have the same top **confidence_score** for **request_type** and **sub_request_type** and same additional fields, then we need to update the **status** key of **new_json** to **no_change**.

            Also, update the **summary** key of **new_json** with the reasoning used in decision making.
            Output the resultant **new_json** object after update.
        """
    )
    prompt = email_content.format(new_json_response=new_json_response, previous_json_response=previous_json_response)

    response = llm.invoke(input=prompt)
    print("Updated Response: ", response.content)
    clean_result = clean_ai_response(response.content)
    return clean_result