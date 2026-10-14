markdown
# 🏊 AI Swim Advisor

An interactive web application built with **Streamlit** that determines if weather and sea conditions are suitable for swimming tomorrow. It fetches real-time meteorological data and uses the **Google GenAI SDK** to generate a personalized swimming recommendation.

## 🚀 Features
- **Live Weather Integration:** Queries the Open-Meteo Weather API for hourly air temperature, wind speed, precipitation, and cloud cover.
- **Live Marine Data:** Queries the Open-Meteo Marine API for sea surface temperatures.
- **Smart Persona-Based AI Advice:** Passes real-time metrics to Gemini models with a highly tailored user persona profile.
- **Bulletproof Fallback Engine:** Features a dual-stage LLM caller that prioritizes fast, modern free models (`gemini-2.5-flash`) and seamlessly loops through alternative available endpoints if rate limits or quota drops occur.
- **Responsive UI:** Features clean Streamlit layouts, status subheaders, and reactive loading animations (`st.spinner`).

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd ai-swim-advisor
   ```

2. **Install dependencies:**
   ```bash
   pip install streamlit requests google-genai
   ```

3. **Provide your Gemini API Key:**
   The code initializes using an empty `genai.Client()`, which naturally expects your API key as an environment variable. Set it in your terminal before running the app:
   
   - **Mac/Linux:** `export GEMINI_API_KEY="your_actual_key_here"`
   - **Windows (CMD):** `set GEMINI_API_KEY="your_actual_key_here"`
   - **Windows (PowerShell):** `$env:GEMINI_API_KEY="your_actual_key_here"`

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 📊 Technical Stack
- **Frontend:** Streamlit
- **LLM Orchestration:** Google GenAI SDK
- **Data Sources:** Open-Meteo Forecast & Marine APIs
