def json_to_string(json_object):
    """
    Convert a JSON object to a JSON string.

    Args:
        json_object (dict): The JSON object to convert.

    Returns:
        str: The JSON string representation of the object, or an error message if conversion fails.
    """
    try:
        # Convert the JSON object to a JSON string
        json_string = json.dumps(json_object)
        return json_string
    except (TypeError, ValueError) as e:
        # Handle errors in case the JSON object is not valid
        return f"Error converting to string: {e}"

def clean_json(json):
    """
    Cleans a JSON string by removing unnecessary formatting, such as code block markers.

    Args:
        json (str): The JSON string to clean.

    Returns:
        str: The cleaned JSON string with leading and trailing markers removed.
    """
    return json.text.strip().lstrip("```json").rstrip("```")