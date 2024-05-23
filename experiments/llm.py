import base64
import os
import requests

api_key = os.environ['OPENAI_API_KEY'] 
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def query_gpt(system_prompt, user_prompt): # return string
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }
    payload = {}
    payload["model"] = "gpt-3.5-turbo"

    sys_msg = {"role": "system", "content":[{"type":"text", "text": system_prompt}]}
    user_msg = {"role": "user", "content": [
        {"type": "text", "text": user_prompt}
        ]}
    payload["messages"] = [sys_msg, user_msg]
    payload["max_tokens"] = 1200
    payload["temperature"] = 0

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return response.json()["choices"][0]["message"]["content"]


def query_gpt4v_with_single_image(image_path, system_prompt, user_prompt): # return string
    base64_image = encode_image(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }
    payload = {}
    payload["model"] = "gpt-4-vision-preview"

    sys_msg = {"role": "system", "content":[{"type":"text", "text": system_prompt}]}
    user_msg = {"role": "user", "content": [
        {"type": "text", "text": user_prompt},
        {"type":"image_url", "image_url":{"url":f"data:image/jpeg;base64,{base64_image}"}}
        ]}
    payload["messages"] = [sys_msg, user_msg]
    payload["max_tokens"] = 1200
    payload["temperature"] = 0

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return response.json()["choices"][0]["message"]["content"]


# note this assumes n texts and n-1 images interleaved between the texts
def query_gpt4v_with_images_and_texts(system_prompt, texts, images):
    base64_images = [encode_image(image_path) for image_path in images]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }
    payload = {}
    payload["model"] = "gpt-4-vision-preview"

    sys_msg = {"role": "system", "content":[{"type":"text", "text": system_prompt}]}
    contents = [{"type": "text", "text": texts[0]}]
    for i in range(len(images)):
        contents.append({"type":"image_url", "image_url":{"url":f"data:image/jpeg;base64,{base64_images[i]}"}})
        contents.append({"type":"text", "text":texts[i+1]})

    user_msg = {"role": "user", "content": contents}
    payload["messages"] = [sys_msg, user_msg]
    payload["max_tokens"] = 1200
    payload["temperature"] = 0

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return response.json()["choices"][0]["message"]["content"]
