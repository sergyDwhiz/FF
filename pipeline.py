from fetch_articles import fetch_articles
from validate_claims import validate_claims, save_to_json

# Hardcoded variables
SPREADSHEET_ID = '1z0tPzic-a_hPtadZufK2ndEbij7NYP7m8EmZQwXGld4'
RANGE_NAME = 'All Prompts'
OUTPUT_JSON = '/Users/sergiusnyah/FF/validated_articles.json'

def main():
    # Fetch articles
    articles = fetch_articles(SPREADSHEET_ID, RANGE_NAME)

    # Validate claims
    validated_articles = validate_claims(articles)

    # Write the results to a JSON file
    save_to_json(validated_articles, OUTPUT_JSON)

    print(f"Results written to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
