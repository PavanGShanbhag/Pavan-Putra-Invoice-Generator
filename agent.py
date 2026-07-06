import os
import json
import urllib.request
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Configuration
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing from your .env file!")

genai.configure(api_key=api_key)

# ── Universal Tool: Live Multi-Currency Exchange Rates ────────────────────

def fetch_live_exchange_rates(base_currency: str = "USD") -> str:
    """Fetches real-time international currency conversion rates relative to a base currency.
    Use this to calculate export totals, parse overseas vendor pricing, or analyze regional duties.
    """
    url = f"https://open.er-api.com/v6/latest/{base_currency.upper()}"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data.get("result") == "success":
                return json.dumps({"base": base_currency.upper(), "rates": data.get("rates", {})})
            return f"Error: Unable to fetch market conversion pairs for {base_currency}."
    except Exception as e:
        return f"Network gateway exception tracking exchange metrics: {e}"


# ── Model Configuration & System Instructions ───────────────────────────

TOOLS = [fetch_live_exchange_rates]

SYSTEM_INSTRUCTION = """
You are the processing core of the Pavan-Putra Invoice Generator. 
Your sole job is to parse unstructured user text, extract invoice details, and return them strictly as a raw JSON object. 
Do not include any conversational filler, introductory text, or markdown code blocks (like ```json). Just return the raw JSON braces.

Expected JSON Structure:
{
    "clientName": "extracted name",
    "clientAddress": "extracted address",
    "clientCity": "extracted city",
    "clientCountry": "extracted country",
    "shippingTerms": "FOB/Ex-Works/etc",
    "destination": "destination port",
    "items": [
        {
            "description": "item description",
            "quantity": 25,
            "unitPrice": 1200,
            "discount": 0,
            "margin": 5
        }
    ]
}
"""
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",  # Update from 2.0 to 2.5
    system_instruction=SYSTEM_INSTRUCTION
)

def run_agent_query(user_query: str) -> str:
    chat = model.start_chat(enable_automatic_function_calling=True)
    try:
        response = chat.send_message(user_query)
        return response.text
    except Exception as e:
        return f"⚠️ Invoice Engine Core Fault: {e}"