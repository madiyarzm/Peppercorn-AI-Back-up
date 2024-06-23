import os
import re
from openai import OpenAI
import pandas as pd

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_personalized_email(customer_data, general_template):
    prompt = (
        f"Generate a personalized marketing email based on the following details:\n"
        f"General Template: {general_template}\n"
        f"Customer Data: {customer_data}\n"
        f"Make the email engaging and focused on the customer's interests and needs, but avoid being overly specific or making the customer feel watched. Instead, focus on general themes that would appeal to someone with the given characteristics."
    )
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}],
    )
    
    return response.choices[0].message.content.strip()

# Example usage

customer_data = {
    "name": "Omar",
    "email": "modestantonny+omar@gmail.com",
    "income": 5000,
    "age": 23,
    "gender": "male",
    "occupation": "student and software engineer",
    "city": "New York City",
    "hobbies": "video games"
}

general_template = "Hi, exciting news, the iPhone 16 is just released."
email_content = generate_personalized_email(customer_data, general_template)
print(email_content)
