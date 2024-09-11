from pathlib import Path
import google.generativeai as genai

genai.configure(api_key="AIzaSyBRPD9PgQNOMrg30e6DI-RMYeL4PStuNPI")

generation_config = {
  "temperature": 0.4,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

while True:
    prompt = input("Prompt: ")
    image_parts = []

    while True:
        image_path = input("Enter the path for an image (or type 'done' to finish): ")

        if image_path.lower() == 'done':
            break

        try:
            image_data = {
                "mime_type": "image/jpeg",
                "data": Path(image_path).read_bytes()
            }
            image_parts.append(image_data)
        except FileNotFoundError:
            print(f"File not found: {image_path}. Please enter a valid path.")

    prompt_parts = [f"{prompt}\n"] + image_parts

    response = model.generate_content(prompt_parts)
    print(f"Answer:{response.text}")