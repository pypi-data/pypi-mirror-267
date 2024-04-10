import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": "Bearer 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"}

class RTRAConnector:
    def __init__(self, api_key, engine_id):
        self.api_key = api_key
        self.engine_id = engine_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def search(self, query):
        url = f"{self.base_url}?key={self.api_key}&cx={self.engine_id}&q={query}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            results = data.get("items", [])
            return results
        else:
            print(f"Error: {response.status_code}")
            return []

    def combine_search_results(self, query):
        results = self.search(query)
        combined_text = ""
        for i, result in enumerate(results[:5], 1):
            combined_text += f"Result {i}:\n"
            combined_text += f"Title: {result.get('title', '')}\n"
            combined_text += f"Snippet: {result.get('snippet', '')}\n"
            combined_text += f"URL: {result.get('link', '')}\n\n"

        return combined_text

    def generate_detailed_response(self, query):
        combined_text = self.combine_search_results(query)
        payload = {"inputs": combined_text}
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        if response.status_code == 200:
            return response.json()["generated_text"]
        else:
            print(f"Error: {response.status_code}")
            return ""
