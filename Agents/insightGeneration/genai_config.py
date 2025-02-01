import google.generativeai as genai

genai.configure(api_key="AIzaSyDphGovO3le5oZMfdCdVSuObg_9kz2tBWg")

model = genai.GenerativeModel("gemini-2.0-flash-exp")
