import uuid
import requests


class BaseClient:

    def __init__(self, assistant_id: str, assistant_version: str, api_key: str, host: str = "http://localhost:8080"):
        self.assistant_id = assistant_id
        self.api_key = api_key
        self.assistant_version = assistant_version
        self.host = host
        self.keep_conversation_history = True
        self.domain = ""
        self.handshake_response = self.handshake()
        self.tool_config = self.handshake_response["assistant_metadata"]["tools"]

    def handshake(self):
        response = requests.post(
            f"{self.host}/v1/assistants/{self.assistant_id}/handshake",
            json={
                "type": "handshake",
                "request_id": uuid.uuid4().hex,
                "assistant_id": self.assistant_id,
                "assistant_version": self.assistant_version,
                "device_id": str(uuid.getnode()),
            },
            headers={
                "Authorization": self.api_key,
                "Content-Type": "application/json",
            },
        )
        return response.json()
