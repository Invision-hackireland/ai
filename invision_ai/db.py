class DBHandler:
    """
    A generic database handler that abstracts database operations.
    Right now, it uses a hardcoded mapping as a placeholder.
    Later, you can replace this with real DB logic.
    """
    def __init__(self):
        # Hardcoded mapping as a stub for demonstration.
        self.room_mapping = {
            "camera1": "shop front",
            "camera2": "main lobby",
            "camera3": "parking lot",
        }

    def get_room_name(self, camera_id: str) -> str:
        """
        Retrieve the room name associated with a given camera_id.

        Args:
            camera_id (str): Unique identifier for the camera.

        Returns:
            str: The room name.
        """
        # In a real implementation, you'd query your DB here.
        return self.room_mapping.get(camera_id, "shop front")
