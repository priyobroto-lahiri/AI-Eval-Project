import os
from google import genai
from dotenv import load_dotenv

class ModelManager:
    def __init__(self):
        load_dotenv()
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self._models = []

    def fetch_available_models(self):
        """
        Fetches all models from the API that support content generation.
        """
        try:
            # Filter for models that support 'generateContent'
            all_models = self.client.models.list()
            self._models = [
                model for model in all_models 
                if model.supported_actions and 'generateContent' in model.supported_actions
            ]
            return self._models
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []

    def list_model_names(self):
        """
        Returns a simple list of model names (e.g., ['models/gemini-1.5-flash', ...])
        """
        if not self._models:
            self.fetch_available_models()
        return [model.name for model in self._models]

if __name__ == "__main__":
    # Quick test to see it in action
    manager = ModelManager()
    print("Fetching generation-capable models...")
    names = manager.list_model_names()
    for name in names:
        print(f" - {name}")
