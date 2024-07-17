import os
from dotenv import load_dotenv

load_dotenv()

import google.generativeai as genai

genai.configure(api_key=os.getenv("gemini_key"))

file_one_path = "star1.jpg"
file_two_path = "star2.jpg"

def upload_to_gemini(path):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  safety_settings=[
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "block_none"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "block_none"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "block_none"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "block_none"
    }
]
)

files = [
  upload_to_gemini("images/photo_2024-07-17_18-37-59.jpg"),
  upload_to_gemini("images/photo_2024-07-17_18-47-22.jpg"),
  upload_to_gemini("images/photo_2024-07-17_18-37-59.jpg"),
  upload_to_gemini("images/photo_2024-07-17_18-46-46.jpg"),
  upload_to_gemini("images/photo_2024-07-17_18-53-58.jpg"),
  upload_to_gemini("images/photo_2024-07-17_18-39-38.jpg"),
  upload_to_gemini(file_one_path),
  upload_to_gemini(file_two_path),
]

while True:
  try:
    response = model.generate_content([
      "You have to compare two images and output similarity as JSON.",
      "Image: ",
      files[0],
      files[1],
      "similarity: {\"similarity\":80}",
      "Image: ",
      files[2],
      files[3],
      "similarity: {\"similarity\":100}",
      "Image: ",
      files[4],
      files[5],
      "similarity: {\"similarity\":0}",
      "Image: ",
      files[6],
      files[7],
      "similarity: ",
    ])
    break
  except:
    print("retrying")

print(response.text)