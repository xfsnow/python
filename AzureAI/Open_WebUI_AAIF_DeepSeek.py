# title: Pipe function to connect DeepSeek model created in Azure AI Foundry in Open WebUI
# author: snowpeak
# author_url: https://github.com/xfsnow
# version: 0.1.1
# Reference: https://gist.github.com/sht2017/fa69af95941516dee947d53228bf6afc

import base64
import json
from typing import Union, Generator, Iterator
from pydantic import BaseModel
import requests
import os


class Pipe:
    class Valves(BaseModel):
        AZURE_ENDPOINT: str = os.getenv("AZURE_API_ENDPOINT", "Azure AI model inference endpoint")
        AZURE_API_KEY: str = os.getenv("AZURE_API_KEY", "Secret Key")
        AZURE_MODEL_NAME: str = os.getenv("AZURE_MODEL_NAME", "Model name")

    def __init__(self):
        self.name = "Azure AI Foundry Pipe"
        self.valves = self.Valves()

    def pipe(self, body: dict, __user__: dict) -> Union[str, Generator, Iterator]:
        url = f"{self.valves.AZURE_ENDPOINT}/chat/completions"
        headers = {
            "api-key": self.valves.AZURE_API_KEY,
            "Content-Type": "application/json",
            "x-ms-model-mesh-model-name": self.valves.AZURE_MODEL_NAME,
        }

        allowed_params = {
            "messages",
            "temperature",
            "role",
            "content",
            "contentPart",
            "contentPartImage",
            "enhancements",
            "dataSources",
            "n",
            "stream",
            "stop",
            "max_tokens",
            "presence_penalty",
            "frequency_penalty",
            "logit_bias",
            "user",
            "function_call",
            "funcions",
            "tools",
            "tool_choice",
            "top_p",
            "log_probs",
            "top_logprobs",
            "response_format",
            "seed",
        }

        if "user" in body and not isinstance(body["user"], str):
            body["user"] = (
                body["user"].get("id")
                if isinstance(body["user"], dict) and "id" in body["user"]
                else str(body["user"])
            )
        filtered_body = {k: v for k, v in body.items() if k in allowed_params}
        if body.get("messages", False):
            messages = json.dumps(body["messages"], ensure_ascii=False)
            if "<chat_history>" in messages and "</chat_history>" in messages:
                if "JSON format" in messages:
                    return {"tags": []}
                else:
                    chat_history = messages.split("<chat_history>", 1)[1].split(
                        "</chat_history>", 1
                    )[0]
                    user, assistant = chat_history.strip("\\n").split("\\n", 1)[:2]
                    return (
                        user.split("USER:", 1)[1][:3]
                        + ":"
                        + assistant.split("ASSISTANT:", 1)[1][:3]
                        + "-"
                        + base64.b64encode(chat_history.encode("utf-8")).decode("utf-8")[:10]
                    )
        try:
            r = requests.post(url=url, json=filtered_body, headers=headers, stream=True, timeout=30)
            r.raise_for_status()
            if body.get("stream", False):
                return r.iter_lines()
            else:
                return r.json()
        except Exception as e:
            print("Error calling Azure Chat Completions API")
            response_text = r.text if "r" in locals() and r is not None else ""
            return f"Error: {e} ({response_text})"