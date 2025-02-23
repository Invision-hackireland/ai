import json
import edgedb

class DBHandler:
    """
    A generic database handler that abstracts database operations.
    Right now, it uses a hardcoded mapping as a placeholder.
    Later, you can replace this with real DB logic.
    """
    def __init__(self):
        self.client = edgedb.create_client()

    def get_camera_rules(self, camera_id: str, user_id: str) -> dict:
        """
        Retrieve camera details including camera name and associated code-of-conduct rules.

        Args:
            camera_id (str): Unique identifier for the camera.

        Returns:
            dict: A dictionary with keys:
                  - 'camera_name': Name of the camera (or None if not found)
                  - 'rules': List of rule objects (each with 'id' and 'text'). Returns an empty list if no rules are found.
        """
        result1 = json.loads(self.client.query_single_json("""
            with user_found := (SELECT User FILTER .id = <uuid>$user_id),
            SELECT {
                rules := (
                    SELECT user_found.rules {
                        rooms: {
                            name
                        },
                        text,
                        id,
                        shared
                    }                                  
                ),
                room_search := (
                    SELECT Camera {
                         room: {
                            name
                        }
                    }              
                    FILTER .id = <uuid>$camera_id
                    LIMIT 1
                )    
            }
        """, user_id=user_id, camera_id=camera_id))

        room_name = result1["room_search"]["room"]["name"]
        rules = result1["rules"]

        # filter rules, keep only if either: shared or rooms contain the room_name
        rules = [rule for rule in rules if rule["shared"] or room_name in [room["name"] for room in rule["rooms"]]]

        return {
            "camera_name": room_name,
            "rules": rules
        }

        

    def get_camera_name(self, camera_id: str) -> str:
        """
        Retrieve the camera name associated with a given camera_id.

        Args:
            camera_id (str): Unique identifier for the camera.

        Returns:
            str: The camera name.
        """
        result = json.loads(self.client.query_single_json(
            """
            SELECT Camera {
                name
            }
            FILTER .id = <uuid>$camera_id;
            """,
            camera_id=camera_id,
        ))
        if result:
            return result["name"]
        else:
            raise ValueError(f"Camera with ID {camera_id} not found.")

    def get_room_name(self, camera_id: str) -> str:
        """
        Retrieve the room name associated with a given camera_id.

        Args:
            camera_id (str): Unique identifier for the camera.

        Returns:
            str: The room name.
        """

        result = json.loads(self.client.query_single_json(
            """
            SELECT Camera {
                room: {
                    name
                }
            }
            FILTER .id = <uuid>$camera_id;
            """,
            camera_id=camera_id,
        ))
        if result:
            return result["room"]["name"]
        else:
            raise ValueError(f"Room with ID {camera_id} not found.")