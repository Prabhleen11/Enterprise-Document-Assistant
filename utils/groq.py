import os

from groq import Groq

from dotenv import load_dotenv


# Load environment variables

load_dotenv()


# Get API key

api_key = os.getenv("GROQ_API_KEY")


if not api_key:

    raise ValueError(
        "GROQ_API_KEY not found. "
        "Please add it to your .env file."
    )


# Create Groq client

client = Groq(
    api_key=api_key
)


def ask_groq(context, question):

    """
    Generates an answer using retrieved document context.
    """

    prompt = f"""
You are an intelligent Enterprise Document Assistant.

Your task is to answer the user's question using ONLY the information
provided in the document context.

IMPORTANT RULES:

1. Do not invent information.
2. Do not use outside knowledge.
3. If the answer is not present in the context, say:
   "I could not find this information in the uploaded documents."
4. Be clear, accurate, and concise.
5. If multiple documents contain relevant information, combine the information.
6. Do not mention that you are an AI unless necessary.

DOCUMENT CONTEXT:
-------------------------------
{context}
-------------------------------

USER QUESTION:
{question}

ANSWER:
"""


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {

                "role": "user",

                "content": prompt

            }

        ],

        temperature=0.2

    )


    return response.choices[0].message.content