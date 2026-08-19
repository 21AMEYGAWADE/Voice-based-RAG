from openai import OpenAI

from app.config import OPENAI_API_KEY, LLM_MODEL


client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(question: str, context: str) -> str:

    prompt = f"""
You are a helpful Voice RAG assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:

"I could not find that information in the uploaded documents."

Do not invent facts.

Keep the answer natural and suitable for speaking aloud.

Context:
----------------
{context}
----------------

User question:
{question}
"""

    response = client.responses.create(
        model=LLM_MODEL,
        input=prompt
    )

    return response.output_text