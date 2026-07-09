from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def main(image_url: str):
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe the elements of this image?"},
                {
                    "type": "image_url",
                    "image_url": {"url": image_url},
                },
            ],
        }
    ]

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    print(res.choices[0].message.content)


if __name__ == "__main__":
    while True:
        print("\n")

        user_input = input("👉 ")

        if user_input.strip().lower() == "q" or user_input.strip() == "":
            break

        main(user_input)

        print("\n")
