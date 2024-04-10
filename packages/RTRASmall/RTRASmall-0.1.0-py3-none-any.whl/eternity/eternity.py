import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": "Bearer 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"}

class RTRASmall:
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
            print(f"Error in Google Custom Search API: {response.status_code}")
            return []

    def combine_search_results(self, query):
        results = self.search(query)
        combined_text = ""
        for i, result in enumerate(results[:5], 1):
            combined_text += result.get('snippet', '') + "\n"  # Extract snippet text
        return combined_text.strip()  # Remove leading/trailing whitespace

    def generate_detailed_response(self, query):
        combined_text = self.combine_search_results(query)
        payload = {"inputs": combined_text}
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            if isinstance(response_data, list) and len(response_data) > 0:
                return response_data[0].get("generated_text", "")
            else:
                print("Error: No response data received from Hugging Face API")
                return ""
        else:
            print(f"Error in Hugging Face API: {response.status_code}")
            return ""

# Example usage:
connector = RTRASmall("AIzaSyC9-5L3kUV-z8FKFG5uf77B8bSZimwL-X4", "92ad72674b97942f5")
query = "Who is Udit Akhouri?"
detailed_response = connector.generate_detailed_response(query)
print(detailed_response)
