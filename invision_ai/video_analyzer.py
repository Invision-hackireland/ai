import os
import json
from datetime import datetime
from openai import OpenAI

from dotenv import load_dotenv

from .db import DBHandler

class BreachReport:
    def __init__(self, rule_id: str, timestamp: datetime, description: str):
        self.rule_id = rule_id
        self.timestamp = timestamp
        self.description = description

    def __repr__(self):
        return (
            f"BreachReport(rule_id={self.rule_id}, "
            f"timestamp={self.timestamp.isoformat()}, "
            f"description={self.description})"
        )

class VideoAnalyzer:
    def __init__(self, openai_api_key: str = None, db_handler: DBHandler = None):
        if openai_api_key is None:
            load_dotenv()
            openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("A valid OPENAI_API_KEY is required.")

        self.client = OpenAI(api_key=openai_api_key)
        self.db_handler = db_handler if db_handler is not None else DBHandler()

    def analyze(self, annotations: str, camera_id: str, user_id: str) -> list:
        camera_details = self.db_handler.get_camera_rules(camera_id, user_id)
        camera_name = camera_details.get("camera_name")
        rules = camera_details.get("rules", [])

        rules_text = "\n".join([f"Rule {rule['id']}: {rule['text']}" for rule in rules])
        prompt_step_1 = (
            f"You are a video analysis assistant. The following is a description of events "
            f"from camera '{camera_name}'. Check if any actions breach the code-of-conduct rules provided.\n\n"
            f"Video Annotations:\n<transcript>\n{annotations}</transcript>\n\n"
            f"Code-of-Conduct Rules:\n<rules>\n{rules_text}</rules>\n\n"
            "List all detected breaches with a brief explanation. Do not format it in JSON yet. "
            "Simply describe the breaches as if you were summarizing them in a report."
        )

        response_step_1 = self.client.chat.completions.create(model="o1-preview",
            messages=[{"role": "user", "content": prompt_step_1}])
        response_content_step_1 = response_step_1.choices[0].message.content.strip()
        
        prompt_step_2 = (
            f"Were there any breaches? If so, let's format the breaches you found into a valid JSON array where each item contains "
            f'"rule_id" (important), "description", and a timestamp in ISO format.\n\n'
            "Output only a JSON array, with no additional explanations. eg. { \"analysis\": [ ... ] }. If no breaches were detected, output an empty array."
        )
        
        response_step_2 = self.client.chat.completions.create(model="gpt-4o-mini",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "user", "content": prompt_step_1},
                {"role": "assistant", "content": response_content_step_1},
                {"role": "user", "content": prompt_step_2}
            ])
        response_content_step_2 = response_step_2.choices[0].message.content.strip()

        try:
            breach_list = json.loads(response_content_step_2).get("analysis")
            current_time = datetime.now()
            reports = [BreachReport(breach.get("rule_id"), current_time, breach.get("description", "")) for breach in breach_list]
            return reports
        except json.JSONDecodeError:
            breach_list = []
            print("Error parsing the response from OpenAI. No breach reports generated.")
            print("Response content:")
            print(response_content_step_2)
        except Exception as e:
            print(f"An error occurred while parsing the response: {e}")
            print("Response content:")
            print(response_content_step_2)

        return []
        
