# Pinecone Hackathon 2023 - Vectornauts

Context-aware code assistant.

## Config

Make sure to add this to your project's package.json. Make sure to change default

```
"contributes": {
    "configuration": {
      "title": "Codextranaunts",
      "properties": {
        "codextranaunts.githubUsername": {
          "type": "string",
          "default": "",
          "description": "Your GitHub username, this is purely used as an identifier for now, feel free to use anything"
        },
        "codextranaunts.repository": {
          "type": "string",
          "default": "",
          "description": "Your GitHub repository, this is purely used as an identifier for now, feel free to use anything"
        }
      }
    }
  },
```
