from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
import json
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Define Request Types and Sub Request Types from the image
REQUEST_TYPES = [
    "Adjustment",
    "All Transfer",
    "Closing Notice",
    "Commitment Change",
    "Fee Payment",
    "Money Movement Intra-group",
    "Money Movement Outbound",
    "Submission Requirements"
]
SUB_REQUEST_TYPES = {
    "Adjustment": ["Reallocation Fees"],
    "All Transfer":[],
    "Closing Notice": ["Amendment Fees", "Reallocation Principal", "Cashless Roll"],
    "Commitment Change": ["Decrease", "Increase"],
    "Fee Payment": ["Ongoing Fee", "Letter of Credit Fee", "Principal", "Interest", "Principal + Interest", "FEMA/FPI Interest + Fee", "Takeout"],
    "Money Movement Intra-group":[],
    "Money Movement Outbound":[],
    "Submission Requirements":[]
}

# Define the desired output JSON format as a string
OUTPUT_JSON_FORMAT = """
{
  "request_types": [
    {
      "type": "[Request Type]",
      "confidence_score": "[Confidence Score between 0.0 and 1.0]",
      "reasoning": "[Reasoning for identifying this request type]",
      "sub_request_types": [
        {
          "type": "[Sub Request Type]",
          "confidence_score": "[Confidence Score between 0.0 and 1.0]",
          "reasoning": "[Reasoning for identifying this sub request type]"
        }
        // ... more sub request types if identified
      ]
    }
    // ... more request types if identified
  ],
  "extracted_information": {
    "amount": "[Extracted Amount, or 'Not Found']",
    "date": "[Extracted Date in<\ctrl3348>-MM-DD format, or 'Not Found']",
    "transaction_id": "[Extracted Transaction ID, or 'Not Found']",
    "loan_number": "[Extracted Loan Number, or 'Not Found']",
    "account_number": "[Extracted Account Number, or 'Not Found']",
    "expiration_date": "[Extracted Expiration Date in<\ctrl3348>-MM-DD format, or 'Not Found']",
    "deal_name": "[Extracted Deal Name, or 'Not Found']",
    "previous_allocation": "[Extracted Previous Allocation details, or 'Not Found']",
    "new_allocation": "[Extracted New Allocation details, or 'Not Found']",
    "transfer_from_account": "[Extracted Source Account for Transfer, or 'Not Found']",
    "transfer_to_account": "[Extracted Destination Account for Transfer, or 'Not Found']",
    "principal_amount": "[Extracted Principal Amount, or 'Not Found']",
    "interest_amount": "[Extracted Interest Amount, or 'Not Found']",
    "fee_type": "[Extracted Fee Type, or 'Not Found']",
    "payment_amount": "[Extracted Payment Amount, or 'Not Found']",
    "submission_document_type": "[Extracted Document Type for Submission, or 'Not Found']"
    // Add other relevant fields based on the identified request and sub-request types
  }
}
"""

# Initialize Gemini model using Langchain
def get_gemini_model(api_key=None, model_name="gemini-2.0-flash"):
    """Initializes the Gemini Pro model with Langchain."""
    if api_key is None:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
    return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)

def classify_email_sequential_langchain(subject, body, attachment_text):
    """Classifies email content using Langchain in a sequential manner."""
    try:
        llm = get_gemini_model()

        # Step 1: Identify Potential Request Types
        prompt_1 = PromptTemplate(
            input_variables=["subject", "body", "attachment_text", "request_types"],
            template="Analyze the content of this email (Subject: {subject}, Body: {body}, Attachments: {attachment_text}) and identify all possible service request types from the following list: {request_types}. For each identified request type, provide a confidence score (0.0 to 1.0) and a brief reasoning. Output as a JSON list of objects with 'type', 'confidence_score', and 'reasoning' keys."
        )
        chain_1 = LLMChain(llm=llm, prompt=prompt_1, output_key="potential_request_types_json")

        # Step 2: Refine Classification with Sub Request Types
        prompt_2 = PromptTemplate(
            input_variables=["potential_request_types_json", "sub_request_types"],
            template="For each request type in the following JSON list: {potential_request_types_json}, and given the sub-request types: {sub_request_types}, identify the most relevant sub-request type(s). For each identified sub-request type, provide a confidence score (0.0 to 1.0) and a brief reasoning. Output as a JSON list of objects within each request type object, with 'type', 'confidence_score', and 'reasoning' keys. If a request type has no applicable sub-request types, return an empty list for that request type."
        )
        chain_2 = LLMChain(llm=llm, prompt=prompt_2, output_key="refined_request_types_with_subtypes_json")

        # Step 3: Extract Necessary Information
        prompt_3 = PromptTemplate(
            input_variables=["subject", "body", "attachment_text", "refined_request_types_with_subtypes_json"],
            template="Based on the identified service request types and sub-request types (in JSON format: {refined_request_types_with_subtypes_json}), extract the necessary information from the email content (Subject: {subject}, Body: {body}, Attachments: {attachment_text}). Output the extracted information as a flat JSON object where keys are the field names (e.g., 'amount', 'loan_number') and values are the extracted information or 'Not Found'."
        )
        chain_3 = LLMChain(llm=llm, prompt=prompt_3, output_key="extracted_information_json")

        # Step 4: Format the Output as JSON
        prompt_4 = PromptTemplate(
            input_variables=["refined_request_types_with_subtypes_json", "extracted_information_json", "output_format"],
            template="Combine the identified request types and sub-request types (in JSON format: {refined_request_types_with_subtypes_json}) with the extracted information (in JSON format: {extracted_information_json}) into the following JSON format: {output_format}. Ensure the final JSON is well-formed and valid."
        )
        chain_4 = LLMChain(llm=llm, prompt=prompt_4, output_key="final_response")

        # Create the sequential chain
        overall_chain = SequentialChain(
            chains=[chain_1, chain_2, chain_3, chain_4],
            input_variables=["subject", "body", "attachment_text", "request_types", "sub_request_types", "output_format"],
            output_variables=["final_response"]
        )

        result = overall_chain({
            "subject": subject,
            "body": body,
            "attachment_text": attachment_text,
            "request_types": ", ".join(REQUEST_TYPES),
            "sub_request_types": json.dumps(SUB_REQUEST_TYPES),
            "output_format": OUTPUT_JSON_FORMAT
        })

        try:
            return json.loads(result["final_response"].strip().lstrip("```json").rstrip("```"))
            print(result)
            print("*"*70)
            return result["final_response"]
        except json.JSONDecodeError as e:
            print(f"Error decoding final JSON response: {e}")
            print(f"Raw final response: {result['final_response']}")
            return None

    except Exception as e:
        print(f"Error classifying email with sequential Langchain: {e}")
        return None

def update_request_for_duplicate_sequential_langchain(subject, body, attachment_text, previous_json_response, api_key=None):
    """Updates a previous request based on a potential duplicate email using Langchain in a sequential manner."""
    try:
        llm = get_gemini_model(api_key)

        previous_json_response_str = json.dumps(previous_json_response)
        print("12"*12)

        # Step 1: Determine if the new email is related and if it provides updates
        prompt_1 = PromptTemplate(
            input_variables=["subject", "body", "attachment_text", "previous_json_response_str"],
            template="""You have a previously classified email with the following JSON response:
            {previous_json_response_str}

            A new email has the following details:
            Subject: {subject}
            Content: {body}
            Attachments: {attachment_text}

            Analyze this new email. Does it provide any significant updates or additional information to the existing service request? Answer with 'update', 'no_update', or 'new_request'."""
        )
        chain_1 = LLMChain(llm=llm, prompt=prompt_1, output_key="update_status")
        print("13"*12)

        # Step 2: Identify updates to extracted information (if 'update')
        prompt_2_update_info = PromptTemplate(
            input_variables=["subject", "body", "attachment_text", "previous_json_response_str"],
            template="""The following is the JSON response from a previous email:
            {previous_json_response_str}

            A new related email has the following details:
            Subject: {subject}
            Content: {body}
            Attachments: {attachment_text}

            Identify any new or updated information in this new email that should update the 'extracted_information' section of the JSON. Output the updates as a JSON object where keys are the fields to update and values are the new values. If no updates, output {previous_json_response_str}."""
        )
        chain_2_update_info = LLMChain(llm=llm, prompt=prompt_2_update_info, output_key="extracted_info_updates")
        print("14"*12)

        # Step 3: Identify updates to request types (if 'update')
        prompt_3_update_types = PromptTemplate(
            input_variables=["subject", "body", "attachment_text", "previous_json_response_str"],
            template="""Using the previous JSON response:
            {previous_json_response_str}

            And the new email details:
            Subject: {subject}
            Content: {body}
            Attachments: {attachment_text}

            Does the new email indicate any changes to the primary request type or introduce a new request type? If so, output the entire updated 'request_types' list as a JSON array of objects, including confidence scores and reasoning for any changes or additions. If no changes, output ''."""
        )
        chain_3_update_types = LLMChain(llm=llm, prompt=prompt_3_update_types, output_key="request_type_updates")
        print("126"*12)

        # Step 4: Classify as new request (if 'new_request')
        prompt_4_new_request = PromptTemplate(
            input_variables=["subject", "body", "attachment_text", "request_types_list", "sub_request_types_dict", "output_format"],
            template="""The following is the content of a new, unrelated email:
            Subject: {subject}
            Body: {body}
            Attachments: {attachment_text}

            Classify this email into service request types from the following list: {request_types_list}, {sub_request_types_dict}. For each type, provide a confidence score and reasoning. Extract the necessary information based on the type, following this JSON format: {output_format}. Include '"is_new_request": true' at the top level."""
        )
        chain_4_new_request = LLMChain(llm=llm, prompt=prompt_4_new_request, output_key="new_classification_json")


        # Define the sequential chain
        overall_chain = SequentialChain(
            input_variables=["subject", "body", "attachment_text", "previous_json_response_str", "request_types_list", "sub_request_types_dict", "output_format"],
            output_variables=["update_status", "extracted_info_updates", "request_type_updates", "new_classification_json"],
            chains=[
                chain_1,
                chain_2_update_info,
                chain_3_update_types,
                chain_4_new_request
            ]
        )

        result = overall_chain({
            "subject": subject,
            "body": body,
            "attachment_text": attachment_text,
            "previous_json_response_str": previous_json_response_str,
            "request_types_list": REQUEST_TYPES,
            "sub_request_types_dict": json.dumps(SUB_REQUEST_TYPES),
            "output_format": OUTPUT_JSON_FORMAT
        })
        print("1hf2"*12)

        update_status = result.get("update_status", "").lower()
        print("12ret"*12)

        if update_status == "update":
            extracted_info_updates_str = result.get("extracted_info_updates", "{}")
            request_type_updates_str = result.get("request_type_updates", "")
            try:
                extracted_info_updates = json.loads(extracted_info_updates_str)
                request_type_updates = json.loads(request_type_updates_str)

                updated_json = previous_json_response.copy()
                if "extracted_information" in updated_json and isinstance(updated_json["extracted_information"], dict):
                    updated_json["extracted_information"].update(extracted_info_updates)
                if request_type_updates:
                    updated_json["request_types"] = request_type_updates
                return updated_json
            except json.JSONDecodeError as e:
                print(f"Error decoding updates JSON: {e}")
                return previous_json_response
        elif update_status == "new_request":
            new_classification_json_str = result.get("new_classification_json", "{}")
            try:
                new_classification = json.loads(new_classification_json_str)
                return new_classification
            except json.JSONDecodeError as e:
                print(f"Error decoding new classification JSON: {e}")
                return None
        else:  # no_update or other cases
            return previous_json_response

    except Exception as e:
        print(f"Error updating request for duplicate with sequential Langchain: {e}")
        return None
if __name__ == "__main__":
    # Example usage for classify_email_sequential_langchain
    sample_subject = "Loan Adjustment Request - Reallocation of Funds"
    sample_body = "This email is to request an adjustment for our commercial loan, account number LN-54321. We would like to request a reallocation of funds amounting to INR 1,500.00 from Department A to Department B, effective immediately."
    sample_attachment_text = "**Fund Reallocation Request**\n\n**Date:** March 5, 2025\n\n**Loan Account Number:** Lhk678hj\n\n**Requesting Party:** [Your Name/Company Name]\n\n**Details of Reallocation:**\n\n* **Amount to be Reallocated:** INR 978800.00\n* **Source of Funds (Department):** Department A\n* **Destination of Funds (Department):** Department B\n\n**Reason for Reallocation:** Operational needs\n\n**Requested Effective Date:** Immediately\n\nPlease process this request at your earliest convenience.\n\nThank you,\n\n[Your Name/Company Name]"

    classified_response_sequential = classify_email_sequential_langchain(sample_subject, sample_body, sample_attachment_text)
    print(classified_response_sequential)
    if classified_response_sequential:
        print("Sequential Classification Response:")
        print(json.dumps(classified_response_sequential, indent=2))

        # Example usage for update_request_for_duplicate
        sample_subject_reply = "Re: Loan Adjustment Request - Reallocation of Funds"
        sample_body_reply = "Just to clarify, the effective date for the reallocation should be March 25, 2025."
        sample_attachment_text_reply = ""

        updated_response = update_request_for_duplicate_sequential_langchain(
            sample_subject_reply,
            sample_body_reply,
            sample_attachment_text_reply,
            classified_response_sequential
        )
        if updated_response:
            print("\nUpdated Response for Duplicate:")
            print(json.dumps(updated_response, indent=2))