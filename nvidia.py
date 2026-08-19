import os
import requests


API_KEY = os.getenv("NVIDIA_API_KEY")

API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

MODEL = "nvidia/nemotron-3-ultra-550b-a55b"


def ask_nvidia(question):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=data,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]


if __name__ == "__main__":

    print("NVIDIA × PLX1 test başlıyor...")

    question = input("Soru: ")

    answer = ask_nvidia(question)

    print()
    print("NVIDIA:", answer)