# ChatGPT Plugin Docs

The Beta version of ChatGPT Plugins introduces the ability to link ChatGPT with third-party applications. By creating a plugin, developers can enhance the functionalities of ChatGPT by calling their APIs. This enables ChatGPT to retrieve real-time data, extract knowledge-base information, assist in various tasks, and much more.

## Overview

The plugins function through one or more API endpoints, which are detailed in a **manifest file** and an **OpenAPI specification**. The AI model uses these specifications to act as an intelligent API caller, interacting with user queries in real-time. For instance, a user inquiry about a codebase could prompt the model to call a relevant plugin API to obtain pertinent code snippets. These snippets can then be used by ChatGPT as context for the query.

## Plugin Development Flow

To develop a plugin, follow this process:

1. **Create a manifest file**: This should be hosted at `yourdomain.com/.well-known/ai-plugin.json`. It should contain metadata about your plugin, details about required authentication, and an OpenAPI specification for your desired endpoints.

2. **Register your plugin**: Do this in the ChatGPT UI. For authentication, provide an OAuth 2 `client_id` and `client_secret` or an API key.

3. **User activation of your plugin**: Users have to manually activate your plugin via the ChatGPT UI. After setting up OAuth, users will be redirected to your plugin to sign in.

4. **User-initiated conversation**: ChatGPT incorporates a brief description of your plugin into the conversation, which is invisible to end users. If a user asks a relevant question, the model may make an API call to your plugin. The results of the API call are then integrated into the model's response.
