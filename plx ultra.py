import json
import os


ULTRA_FILE = "ultra_knowledge.json"


def load_knowledge():

    if not os.path.exists(ULTRA_FILE):
        return {}

    with open(
        ULTRA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def find_topic(question):

    knowledge = load_knowledge()

    question = question.lower()

    for topic, data in knowledge.items():

        keywords = data.get(
            "keywords",
            []
        )

        for keyword in keywords:

            if keyword.lower() in question:
                return topic, data

    return None, None


def ultra(question):

    topic, data = find_topic(question)

    if data is None:
        return None

    return {
        "topic": topic,
        "knowledge": data.get(
            "knowledge",
            ""
        )
    }


if __name__ == "__main__":

    print("PLX ULTRA hazır.")

    while True:

        question = input("Soru: ")

        if question.lower() == "çıkış":
            break

        result = ultra(question)

        if result is None:
            print("Uzmanlık bulunamadı.")
        else:
            print()
            print("Uzmanlık:", result["topic"])
            print("Bilgi:", result["knowledge"])