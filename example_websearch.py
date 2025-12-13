from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def web_search_movie(query: str):
    """Search for movie using GPT web search and return complete results.

    Returns the full search result as text.
    """
    prompt = f"search for movie - {query}"

    completion = client.chat.completions.create(
        model="gpt-4o-mini-search-preview-2025-03-11",
        web_search_options={},
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    return completion.choices[0].message.content or "No results found."


if __name__ == "__main__":
    query = input("Enter movie title: ") or "jackie kannada"
    print(f"\nSearching for: {query}\n")
    print("="*80)
    result = web_search_movie(query)
    print(result)
    print("="*80)
