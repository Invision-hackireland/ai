import os
import asyncio
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

async def main():
    # Initialize the GenAI client
    client = genai.Client(
        api_key=api_key,
        http_options={"api_version": "v1alpha"}
    )

    # Define the model and configuration
    model_id = "gemini-2.0-flash-exp"
    config = {"response_modalities": ["TEXT"]}

    # Connect to the live session
    async with client.aio.live.connect(model=model_id, config=config) as session:
        # Send a message to the model
        await session.send(input="Hello, Gemini!", end_of_turn=True)

        # Receive and print the response
        async for response in session.receive():
            if not response.server_content.turn_complete:
                for part in response.server_content.model_turn.parts:
                    print(part.text, end="", flush=True)

# Run the main function
asyncio.run(main())
