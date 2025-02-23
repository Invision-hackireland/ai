class DBHandler:
    """
    A generic database handler that abstracts database operations.
    Right now, it uses a hardcoded mapping as a placeholder.
    Later, you can replace this with real DB logic.
    """
    def __init__(self):
        # Hardcoded mapping as a stub for demonstration.
        self.room_mapping = {
            "camera1": "backyard",
            "camera2": "main lobby",
            "camera3": "parking lot",
        }

        self.camera_details = {
            "camera1": {
                "camera_name": "Shop Front",
                "rules": [
                    {"id": "1", "text": "No unauthorized entry."},
                    {"id": "2", "text": "Do not obstruct walkways."},
                    {"id": "3", "text": "No throwing packages into the lawn."},
                ],
            },
            "camera2": {
                "camera_name": "Main Lobby",
                "rules": [
                    {"id": "3", "text": "Maintain professional behavior."},
                    {"id": "4", "text": "No loitering in the corridors."},
                ],
            },
            # Add more cameras as needed.
        }

    def get_camera_details(self, camera_id: str) -> dict:
        """
        Retrieve camera details including camera name and associated code-of-conduct rules.

        Args:
            camera_id (str): Unique identifier for the camera.

        Returns:
            dict: A dictionary with keys:
                  - 'camera_name': Name of the camera (or None if not found)
                  - 'rules': List of rule objects (each with 'id' and 'text'). Returns an empty list if no rules are found.
        """
        return self.camera_details.get(camera_id, {"camera_name": None, "rules": []})

    def get_room_name(self, camera_id: str) -> str:
        """
        Retrieve the room name (i.e. camera name) associated with the provided camera_id.

        Args:
            camera_id (str): Unique identifier for the camera.

        Returns:
            str: The camera name, or None if not found.
        """
        details = self.get_camera_details(camera_id)
        return details.get("camera_name", None)


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
