### Summary

As a part of my research under the Fatima Fellowship on Red teaming of LLMs, this project involves validating claims in articles using the Hugging Face Inference API. The validation process includes fetching articles, analyzing claims, and categorizing their validity based on fact scores obtained from a zero-shot classification model. The following steps outline the process:

1. **Fetching Articles**: Articles are fetched from various sources and stored in a JSON file.
2. **Validating Claims**: Claims within the articles are validated using the Hugging Face Inference API. The model used for validation is `facebook/bart-large-mnli`, which fits within the API's constraints.
3. **Fact Score Calculation**: For each claim, a fact score is generated. This score indicates the likelihood of the claim being true or false.
4. **Categorizing Validity**: Based on the fact score, claims are categorized into four validity categories: "Very likely true", "Likely true", "Uncertain", and "Likely false".
5. **Saving Results**: The validated articles, along with their fact scores and validity categories, are saved to a JSON file for further analysis.

The project utilizes environment variables to securely manage API tokens and ensures that only English claims are processed. The implementation is modular, allowing for easy updates and maintenance. The results provide a structured way to assess the credibility of claims in articles, aiding in the fight against misinformation.