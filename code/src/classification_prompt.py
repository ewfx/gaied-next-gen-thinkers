import json


def create_classification_hierarchy_from_json(json_data):
    if not isinstance(json_data, dict):
        print("Error: Input must be a dictionary.")
        return []

    classification = "Classification Hierarchy List: "

    for type_name, subtypes in json_data.items():
        if not isinstance(subtypes, list):
            print(f"Error: Subtypes for Type '{type_name}' must be a list.")
            return []
        classification += f"\n• Request Type: {type_name}"
        for subtype in subtypes:
            classification += f"\n\t- Request Sub Type: {subtype}"
            
    return classification

def classify_request_type():
    json_data = {
        "Adjustment": [],
        "AU Transfer": [],
        "Closing Notice": ["Reallocation Fees", "Amendment Fees", "Reallocation Principal"],
        "Commitment Change": ["Cashless Roll", "Decrease", "Increase"],
        "Fee Payment": ["Ongoing Fee", "Letter of Credit Fee"],
        "Money Movment-Inbound": ["Principal", "Interest", "Principal and Interest", "Principal and Interest and Fees"],
        "Money Movment-Outbound": ["Timebound", "Foriegn Currency"]
    }

    return create_classification_hierarchy_from_json(json_data)
    

    # Classification Hierarchy:
    #     - Type: Adjustment
    #     - Type: AU Transfer
    #     - Type: Closing Notice
    #         - Subtype: Reallocation Fees
    #         - Subtype: Amendment Fees
    #         - Subtype: Reallocation Principal
    #     - Type: Commitment Change
    #         - Subtype: Cashless Roll
    #         - Subtype: Decrease
    #         - Subtype: Increase
    #     - Type: Fee Payment
    #         - Subtype: Ongoing Fee
    #         - Subtype: Letter of Credit Fee
    #     - Type: Money Movment-Inbound
    #         - Subtype: Principal
    #         - Subtype: Interest
    #         - Subtype: Principal and Interest
    #         - Subtype: Principal and Interest and Fees
    #     - Type: Money Movment-Outbound
    #         - Subtype: Timebound
    #         - Subtype: Foriegn Currency

def json_to_string(json_object):
    try:
        # Convert the JSON object to a JSON string
        json_string = json.dumps(json_object)
        return json_string
    except (TypeError, ValueError) as e:
        # Handle errors in case the JSON object is not valid
        return f"Error converting to string: {e}"

def outputJsonFormat() :
    expected_fields = {
        "request_types": [
            {
            "type": "[Classification Type]",
            "subtype": "[Classification Subtype]",
            "confidence_score": "[Confidence Score between 0.0-1.0]",
            "reasoning": "[Explanation for classification]"
            }
        ],
        "extracted_information": {
            "date": "[Extracted Date in YYYY-MM-DD format or 'Not Found']",
            "time": "[Extracted Time in HH:MM format or 'Not Found']",
            "pnr": "[Extracted PNR number or 'Not Found']",
            "departure": "[Extracted Departure location or 'Not Found']",
            "arrival": "[Extracted Arrival location or 'Not Found']",
            "amount": "[Extracted Amount or 'Not Found']",
            "transaction_id": "[Extracted Transaction ID or 'Not Found']",
            "loan_number": "[Extracted Loan Number or 'Not Found']",
            "account_number": "[Extracted Account Number or 'Not Found']",
            "expiration_date": "[Extracted Expiration Date in YYYY-MM-DD or 'Not Found']",
            "deal_name": "[Extracted Deal Name or 'Not Found']",
            "previous_allocation": "[Extracted Previous Allocation or 'Not Found']",
            "new_allocation": "[Extracted New Allocation or 'Not Found']",
            "principal_amount": "[Extracted Principal Amount or 'Not Found']",
            "interest_amount": "[Extracted Interest Amount or 'Not Found']",
            "fee_type": "[Extracted Fee Type or 'Not Found']",
            "submission_document_type": "[Extracted Document Type or 'Not Found']",
            "other_fields": "you can also add more fields which might be relevant to that specific request type"
        }
    }

    return json_to_string(expected_fields)