import os
from google import genai
from google.genai.types import HttpOptions, Part
from dotenv import load_dotenv
from .db import DBHandler

class VideoAnnotator:
    """
    VideoAnnotator leverages Google's GenAI to analyze video content.
    It uses an external DBHandler for room name retrieval, making it
    clean and scalable for future extensions.
    """

    def __init__(self, api_key: str = None, api_version: str = "v1", db_handler: DBHandler = None):
        """
        Initialize the VideoAnnotator.

        Args:
            api_key (str, optional): Your Google API key. If not provided, it will be loaded from a .env file.
            api_version (str): API version for the GenAI client.
            db_handler (DBHandler, optional): An instance of DBHandler for room retrieval.
                                               If not provided, a default instance is created.
        """
        # Load API key from environment if not provided
        if api_key is None:
            load_dotenv()
            api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError("A valid GOOGLE_API_KEY is required.")

        self.client = genai.Client(api_key=api_key, http_options=HttpOptions(api_version=api_version))
        self.db_handler = db_handler if db_handler is not None else DBHandler()

    def run(self, camera_id: str, video_file_path: str) -> str:
        """
        Process the video file and generate a detailed activity report.

        Args:
            camera_id (str): Unique identifier for the camera.
            video_file_path (str): Path to the video file.

        Returns:
            str: The analysis text generated from the video content.
        """
        # Retrieve room name using the external DBHandler.
        room_name = self.db_handler.get_room_name(camera_id)

        # Read the video file as bytes.
        try:
            with open(video_file_path, "rb") as video_file:
                video_data = video_file.read()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Video file not found at {video_file_path}") from e

        # Compose the prompt with room information.
        prompt = (
            f"This is the CCTV footage of room: `{room_name}`. Mention the room in your output\n"
            "Describe in every single details the events that happened in this CCTV footage. "
            "Make the greatest level of details on everything moving or that changes (ignore what doesn't change). "
            "List what every person or individual is doing and what happens, using bullet points."
        )

        # Generate the content using Google's GenAI.
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=[
                prompt,
                Part.from_bytes(data=video_data, mime_type="video/mp4"),
            ],
        )

        # Return the generated text report.
        return response.candidates[0].content.parts[0].text