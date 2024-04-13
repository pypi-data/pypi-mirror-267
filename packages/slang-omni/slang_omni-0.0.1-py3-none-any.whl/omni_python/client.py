import uuid
import json
import requests
import sseclient
from omni_python.base import BaseClient
from omni_python.response import OmniActionResponse
from typing import AsyncGenerator


class AsyncOmniClient(BaseClient):

    async def text2action(
        self, query: str, task_tools: list, stream: bool = True
    ) -> AsyncGenerator[OmniActionResponse, None]:
        app_context = {}
        request_id = uuid.uuid4().hex
        response = requests.post(
            f"{self.host}/v1/assistants/{self.assistant_id}/text2action",
            json={
                "type": "text2action",
                "request_id": request_id,
                "assistant_id": self.assistant_id,
                "assistant_version": self.assistant_version,
                "device_id": str(uuid.getnode()),
                "input_query": query,
                "domain_name": self.domain,
                "app_context": app_context,
                "conversation_history": "{}" if not self.keep_conversation_history else "",
                "tool_config": self.tool_config,
                "request_tools": task_tools,
            },
            headers={"Authorization": self.api_key, "Content-Type": "application/json"},
            stream=True,
        )
        client = sseclient.SSEClient(response)
        for event in client.events():
            event_data = event.data
            d = json.loads(event_data)
            rt = d.get("response_type", "assistant")

            if rt != "status":
                is_final = d.get("is_final", False)
                if stream:
                    yield OmniActionResponse(**d)
                elif is_final:
                    yield OmniActionResponse(**d)
