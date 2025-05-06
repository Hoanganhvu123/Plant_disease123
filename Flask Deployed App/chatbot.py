import os
import requests
from dotenv import load_dotenv
import groq

# Load environment variables (keep for potential future use)
load_dotenv()

# Use the API key provided directly by the user for testing
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_KEY = "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"

# Initialize Groq client
if GROQ_API_KEY:
    client = groq.Client(api_key=GROQ_API_KEY)
else:
    client = None
    print("WARNING: GROQ_API_KEY not found. Chatbot will not function.")

def generate_initial_message(disease_name, confidence, description, prevent):
    """Generate initial message from chatbot about detected disease"""
    return f"Tôi đã phát hiện bệnh {disease_name} với độ chính xác {confidence}%. Bạn có thể hỏi tôi thêm về cách điều trị hoặc thông tin chi tiết về bệnh này."

def generate_response(prompt, disease_context=None):
    """Generate a response using Groq API with Llama 3"""
    if not client:
        return "Lỗi: Không thể khởi tạo Groq client. Vui lòng kiểm tra API key."

    # Create system message with context about the plant disease
    system_message = "Bạn là trợ lý AI chuyên về bệnh cây trồng, nhiệm vụ của bạn là giúp người dùng hiểu và xử lý các bệnh cây.luôn luôn trả lời bằng tiếng việt"

    # Add disease context if available
    if disease_context:
        context_str = (
            f"\n\nThông tin về bệnh đã phát hiện gần đây:\n"
            f"- Tên bệnh: {disease_context.get('name', 'Không rõ')}\n"
            f"- Mô tả: {disease_context.get('description', 'Không rõ')}\n"
            f"- Phòng tránh: {disease_context.get('prevent', 'Không rõ')}\n"
            f"- Độ chính xác phát hiện: {disease_context.get('confidence', 'Không rõ')} %"
         )
        system_message += context_str

    messages_payload = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]

    try:
        chat_completion = client.chat.completions.create(
            messages=messages_payload,
            model="deepseek-r1-distill-llama-70b", # Using confirmed Llama 3 model
            temperature=0.7,
            max_tokens=800,
            # top_p=1, # Optional parameters
            # stop=None, # Optional parameters
            # stream=False # Optional parameters
        )

        response_content = chat_completion.choices[0].message.content
        return response_content

    except Exception as e:
        # Log the error for debugging
        print(f"Error calling Groq API: {e}")
        # Check if the error object has response details
        error_details = str(e)
        if hasattr(e, 'response') and e.response is not None:
             try:
                 error_body = e.response.json()
                 error_details += f" - {error_body}"
             except: # Handle cases where response body is not JSON
                 error_details += f" - {e.response.text}"

        return f"Lỗi khi gọi API Groq: {error_details}"

# Suggested quick responses for users to click
def get_suggested_responses(disease_name):
    return [
        f"Làm thế nào để điều trị bệnh {disease_name}?",
        f"Làm cách nào để phòng ngừa bệnh {disease_name}?",
        f"Bệnh {disease_name} có lây lan không?",
        "Làm thế nào để nhận biết sớm bệnh này?"
    ] 