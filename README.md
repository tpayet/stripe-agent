# Stripe AI Assistant

## Overview

The Stripe AI Assistant is an interactive chat application that provides information about Stripe accounts. It uses OpenAI's GPT model to generate responses, offering a conversational interface for users to inquire about Stripe-related topics. The assistant maintains context throughout the conversation, allowing for more natural and coherent interactions.

## Features

- Interactive chat interface using Streamlit
- Real-time streaming responses with a typing simulation
- Context-aware conversations using conversation history
- Integration with OpenAI's GPT-3.5-turbo model
- FastAPI backend for efficient request handling

## Prerequisites

- Python 3.7+
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/stripe-ai-assistant.git
   cd stripe-ai-assistant
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage

1. Start the FastAPI backend:
   ```
   python main.py
   ```

2. In a new terminal, run the Streamlit frontend:
   ```
   streamlit run frontend.py
   ```

3. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

4. Start chatting with the Stripe AI Assistant by typing your questions or requests in the input box.

## Project Structure

- `main.py`: FastAPI backend that handles requests and interacts with the OpenAI API.
- `frontend.py`: Streamlit frontend that provides the chat interface.
- `requirements.txt`: List of Python dependencies for the project.

## Customization

- To modify the AI's behavior or knowledge base, edit the system message in `main.py`.
- To change the OpenAI model, update the `model` parameter in the `client.chat.completions.create()` call in `main.py`.

## Contributing

Contributions to improve the Stripe AI Assistant are welcome. Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

[MIT License](LICENSE)

## Disclaimer

This project is not officially affiliated with Stripe. It's a demonstration of how to create an AI-powered assistant using OpenAI's API and should not be used as an official source of Stripe information or support.
