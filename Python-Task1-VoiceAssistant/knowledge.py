import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={"timeout": 30000}
)




def answer_question(question):

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=(
                "You are a helpful voice assistant. "
                "Answer the user's question clearly and accurately. "
                "Keep the answer short and natural for speaking. "
                "If the user says 'just say', give only the direct answer. "
                "Do not give unnecessary details.\n\n"
                "Question: " + question
            )
        )

        return response.text.strip()

    except Exception as e:

        print("Gemini error:", e)

        return "Sorry, I could not answer that question."