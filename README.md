# openai-actions-demo

This repository contains examples for using OpenAI's API.

## YouTube Shorts Prompt Generator

The script `generate_shorts_prompt.py` retrieves trending topics (using Google Trends when available) and asks the OpenAI API to craft a short video prompt for each topic.

### Prerequisites

* Set the `OPENAI_API_KEY` environment variable with your OpenAI API key.
* The script uses only Python's standard library and has no third‑party dependencies.

### Usage

Run the script from the repository root:

```bash
OPENAI_API_KEY=your_api_key python generate_shorts_prompt.py
```

The output contains a generated prompt for each trending topic. If the API key is invalid or the network request fails, the script will print an error message instead of crashing.
