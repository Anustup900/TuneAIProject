import os

# OPENAI

OPENAI_API_BASE_URL = "https://api.openai.com/v1"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TEXT_MODEL_ENGINE = 'gpt-4-0125-preview'

# GITHUB
GITHUB_AUTH_KEY = os.getenv("GITHUB_AUTH_KEY")

# REGEX
REPO_NAME_EXTRACTION_PATTERN = r"https://github.com/([^/]+)/([^/]+)$"

# SCHEMA
JSON_SCHEMA_FOR_GPT = {
  "type": "object",
  "properties": {
    "issues": {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "issue_title": {
              "type": "string"
            },
            "rating": {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string"
                },
                "description": {
                  "type": "string"
                }
              },
              "required": [
                "type",
                "description"
              ]
            }
          },
          "required": [
            "issue_title",
            "rating"
          ]
        }
      ]
    }
  },
  "required": [
    "issues"
  ]
}