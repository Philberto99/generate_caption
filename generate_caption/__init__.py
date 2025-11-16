import logging
import azure.functions as func
import requests
import json
import os
from dotenv import load_dotenv

# 🔹 Load environment variables from .env file
load_dotenv()

# 🔐 Environment variables
VISION_ENDPOINT = os.getenv("VISION_ENDPOINT")
VISION_KEY = os.getenv("VISION_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_KEY = os.getenv("OPENAI_KEY")
OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT")


def main(blob: func.InputStream):
    logging.info(f"🟡 Triggered by blob: {blob.name}, Size: {blob.length} bytes")

    # 🔹 Step 1: Read image bytes
    image_data = blob.read()
    logging.info("🟢 Image bytes read successfully")

    # 🔹 Step 2: Call Vision API
    vision_url = f"{VISION_ENDPOINT}/vision/v3.2/analyze?visualFeatures=Tags"
    vision_headers = {
        "Ocp-Apim-Subscription-Key": VISION_KEY,
        "Content-Type": "application/octet-stream"
    }
    vision_response = requests.post(vision_url, headers=vision_headers, data=image_data)
    vision_result = vision_response.json()
    tags = [tag["name"] for tag in vision_result.get("tags", [])]
    logging.info(f"🔵 Vision tags: {tags}")

    # 🔹 Step 3: Call OpenAI to rewrite tags
    prompt = f"Rewrite these image tags into a natural caption: {', '.join(tags)}"
    openai_url = (
        f"{OPENAI_ENDPOINT}/openai/deployments/"
        f"{OPENAI_DEPLOYMENT}/chat/completions?api-version=2024-02-15-preview"
    )
    openai_headers = {
        "api-key": OPENAI_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "system", "content": "You are a captioning assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 50
    }
    openai_response = requests.post(openai_url, headers=openai_headers, json=payload)
    openai_result = openai_response.json()
    caption = openai_result["choices"][0]["message"]["content"]
    logging.info(f"🟣 Caption generated: {caption}")

    # 🔹 Step 4: Log token usage (optional)
    usage = openai_result.get("usage", {})
    logging.info(f"🧮 Token usage: {usage}")

    # 🔹 Step 5: Output caption (store, return, or log)
    logging.info(f"✅ Final caption: {caption}")