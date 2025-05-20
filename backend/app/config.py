# Configuration settings for the FastAPI app
# Add environment variables, API keys, and other config here

import os

class Settings:
    PROJECT_NAME: str = "Chatbot Theme Identifier"
    GROQ_API_KEY: str = "ENTER-YOUR-API-KEY-HERE"

    # Add more settings as needed, e.g., DB connection, API keys

settings = Settings()
