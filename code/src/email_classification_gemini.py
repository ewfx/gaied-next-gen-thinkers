from classification_prompt import classify_request_type, outputJsonFormat
import google.generativeai as genai

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
        print("nextGenThinkers", response.text)
        return response.text
    except Exception as e:
        print(f"Error classifying email: {e}")
        return None  # Or handle the error as appropriate