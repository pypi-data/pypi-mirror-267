import requests


class RTRAConnector:
    def __init__(self, api_key, engine_id, huggingface_model, huggingface_api_token):
        self.api_key = api_key
        self.engine_id = engine_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.huggingface_model = huggingface_model
        self.huggingface_api_token = huggingface_api_token

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
        search_results = self.combine_search_results(query)
        prompt = f"Search results for '{query}':\n{search_results}\n\nNow, give answers to this query:\n"
        payload = {"inputs": prompt}
        headers = {"Authorization": f"Bearer {self.huggingface_api_token}"}
        huggingface_url = f"https://api-inference.huggingface.co/models/{self.huggingface_model}"
        response = requests.post(huggingface_url, headers=headers, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            if isinstance(response_data, list) and len(response_data) > 0:
                generated_text = response_data[0].get("generated_text", "")
                # Extract only the answer part
                start_index = generated_text.find("Now, give answers to this query:") + len("Now, give answers to this query:")
                answer = generated_text[start_index:].strip()
                return answer
            else:
                print("Error: No response data received from Hugging Face API")
                return ""
        else:
            print(f"Error in Hugging Face API: {response.status_code}")
            return ""