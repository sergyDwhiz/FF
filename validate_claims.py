import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure the token is set as an environment variable
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
if not HUGGINGFACE_TOKEN:
    raise ValueError("Hugging Face token not found. Please set the HUGGINGFACE_TOKEN environment variable.")

# Define the Hugging Face API URL and headers
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
        return None
    return response.json()

def get_fact_score(claim: str) -> float:
    """
    Get the fact score for a given claim using the Hugging Face Inference API.

    Args:
        claim: The claim to be validated.
    Returns:
        The fact score for the claim as a float.
    """
    # Define classes for zero-shot classification
    classes = ["True", "False"]

    # Generate fact score
    payload = {
        "inputs": claim,
        "parameters": {"candidate_labels": classes}
    }
    output = query(payload)

    # Log the entire response for debugging
    if output:
        print(f"API response for claim '{claim}': {json.dumps(output, indent=2)}")

        # Check if 'scores' key exists in the response
        if "scores" not in output:
            print(f"Error: 'scores' key not found in the response for claim: {claim}")
            return None

        # Extract the fact score for "True"
        true_score = output["scores"][0]
        return true_score
    return None

def validate_claims(articles):
    validated_articles = []
    for article in articles:
        if "False Claim" in article and article["False Claim"].strip():
            # Ensure the claim is in English
            claim = article["False Claim"]
            if claim.isascii():
                # Generate fact score using the selected model
                fact_score = get_fact_score(claim)
                if fact_score is not None:
                    article["fact_score"] = fact_score

                    # Determine the validity category based on the fact score
                    if fact_score >= 0.7:
                        article["validity"] = "Very likely true"
                    elif 0.5 <= fact_score < 0.7:
                        article["validity"] = "Likely true"
                    elif 0.3 <= fact_score < 0.5:
                        article["validity"] = "Uncertain"
                    else:
                        article["validity"] = "Likely false"

                    validated_articles.append(article)
            else:
                print(f"Non-English claim found: {claim}")
        else:
            print(f"Missing or empty 'False Claim' key in article: {article}")
    print(f"Validated {len(validated_articles)} articles")
    for article in validated_articles:
        print(article)
    return validated_articles

def save_to_json(articles, filename):
    with open(filename, mode='w') as file:
        json.dump(articles, file, indent=4)

if __name__ == "__main__":
    # Example usage
    articles = [
        {"title": "Article 1", "False Claim": "Claim 1"},
        {"title": "Article 2", "False Claim": "Claim 2"}
    ]
    validated_articles = validate_claims(articles)
    save_to_json(validated_articles, "validated_articles.json")
    print(validated_articles)