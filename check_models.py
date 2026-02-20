import google.generativeai as genai
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyB9XNx8sV1H5rTi8OUfUlmVGxXNKplSqF8"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

try:
    print("Listing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error: {e}")
