import requests

class Eternity:
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

    def get_combined_text(self, query):
        results = self.search(query)
        combined_text = ""
        for i, result in enumerate(results[:5], 1):
            combined_text += f"Result {i}:\n"
            combined_text += f"Title: {result.get('title', '')}\n"
            combined_text += f"Snippet: {result.get('snippet', '')}\n"
            combined_text += f"URL: {result.get('link', '')}\n\n"
        return combined_text

