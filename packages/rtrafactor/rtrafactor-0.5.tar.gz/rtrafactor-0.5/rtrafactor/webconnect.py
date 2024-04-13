from googlesearch import search
import requests
from bs4 import BeautifulSoup

class RTRAConnector:
    def __init__(self, huggingface_model, huggingface_api_token):
        self.huggingface_model = huggingface_model
        self.huggingface_api_token = huggingface_api_token
        self.max_tokens = 60000

    def search(self, query):
        try:
            results = search(query, num_results=5)  # Use num_results to limit search results
            urls = list(results)
            return urls
        except Exception as e:
            print(f"Error in Google Search: {e}")
            return []

    def scrape_and_process(self, urls):
        scraped_text = ""
        for url in urls:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = soup.get_text()
                    # Limit the text to max_tokens
                    if len(scraped_text) + len(text) < self.max_tokens:
                        scraped_text += text + "\n"
                    else:
                        break
            except Exception as e:
                print(f"Error scraping URL {url}: {e}")
        # Process the scraped text here (e.g., clean and summarize)
        # For simplicity, let's just return the scraped text
        return scraped_text

    def generate_response(self, query, data_source):
        if data_source == "Google":
            urls = self.search(query)
            scraped_text = self.scrape_and_process(urls)
            return scraped_text
        elif data_source == "HuggingFace":
            return self.generate_huggingface_response(query)

    def generate_huggingface_response(self, query):
        prompt = f"Search results for '{query}':\n{self.generate_response(query, 'Google')}\n\nNow, give answers to this query:\n"
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

    def compare_answers(self, query):
        google_response = self.generate_response(query, "Google")
        huggingface_response = self.generate_response(query, "HuggingFace")
        # Compare the responses and provide a one-shot textual answer
        # For simplicity, let's just return the Hugging Face response
        return huggingface_response
