import json
import os

import openai
from dotenv import load_dotenv
from groq import Groq
from langfuse import observe

import src.llm.prompt_template as prompts

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_APIKEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

openai.api_key = os.getenv("GROQ_APIKEY")
openai.api_base = "https://api.groq.com/openai/v1"


def get_groq_client():
    groq_client = Groq(api_key=GROQ_API_KEY)
    return groq_client


@observe()
def extract_info_via_llm(query: str, llm_client) -> dict:
    llm_prompt = prompts.user_query_llm_prompt(query=query)
    response = llm_client.chat.completions.create(model="llama3-8b-8192",  # Or "phi-3-mini-128k" for fallback
                                                  messages=[{"role": "user", "content": llm_prompt}], temperature=0.2, )
    try:
        content = response.choices[0].message.content.strip()
        print("🧠 Extract Info - LLM response:\n", content)
        return json.loads(content)
    except Exception as e:
        print("Error parsing Extract Info - LLM response:", e)
        return {"cve_id": None, "intent": "general"}


@observe()
def call_llm_on_prompt(llm_client, description):
    prompt = f"""
You are a cybersecurity expert. Based on the following CVE description, suggest practical remediation steps:

Description:
\"\"\"{description}\"\"\"

Respond in bullet points.
"""
    response = llm_client.chat.completions.create(model="llama3-8b-8192",
                                                  messages=[{"role": "user", "content": prompt}], temperature=0.3, )
    try:
        content = response.choices[0].message.content.strip()
        print("🧠 Prompting - LLM response:\n", content)
        return content
    except Exception as e:
        print("Error parsing Prompting - LLM response:", e)
        return {"cve_id": None, "intent": "general"}
