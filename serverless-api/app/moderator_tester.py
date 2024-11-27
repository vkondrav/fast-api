from openai import OpenAI
from dotenv import load_dotenv
from moderator import moderate_message
import os

load_dotenv()

client = OpenAI()

while True:
    user_input = input("Enter your message (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break

    response = moderate_message(user_input, client)

    print(response)
