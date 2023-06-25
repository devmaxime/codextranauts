# codextranaunts README

This is the README for your extension "codextranaunts".

## Requirements

Make sure to add this into your package.json and replace defaults with anything you'd like as this is MVP.

```"contributes": {
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
