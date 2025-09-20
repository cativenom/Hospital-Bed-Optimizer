from fastapi import FastAPI, Request
import google.generativeai as genai
import os

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

# Static knowledge prompt (system role)
SYSTEM_PROMPT = """
You are WardFlow AI, a hospital operations assistant specializing in bed allocation and resource optimization.

Core knowledge:
- Each ward has a limited capacity (ICU = 30, General = 100, Pediatrics = 40).
- Overflow handling: Move stable patients from ICU → General Ward, or General → Pediatrics if capacity allows.
- Cleaning cycle per bed = 2 hours.
- During flu season or local outbreaks, forecast admissions increase by ~20%.
- Goal: Avoid bottlenecks and maximize bed turnover efficiency.
- Always give concise, actionable answers suitable for hospital administrators.
"""

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message", "")

    # Example dynamic context (replace with real /forecast + /optimize later)
    forecast_data = {"ICU": 92, "General": 75, "Pediatrics": 68}
    recommendations = [
        "Transfer 2 patients from ICU to General Ward.",
        "Increase cleaning staff in General due to high turnover."
    ]

    prompt = f"""
    {SYSTEM_PROMPT}

    Forecast: {forecast_data}
    Recommendations: {recommendations}

    The hospital admin asks: {user_message}
    """

    response = model.generate_content(prompt)
    return {"response": response.text}
