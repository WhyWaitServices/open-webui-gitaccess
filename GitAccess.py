"""
title: GitAccess
author: Pascal Frerks
author_url: https://pascal-frerks.de
git_url: https://github.com/username/string-reverse.git
description: This Tool allows the LLM to connect to one GitHub Repo to fetch its contents to ask it about it and use it to have your model always have the current state of the project
required_open_webui_version: 0.6.0
version: 0.0.4
licence: MIT
"""

from typing import Any, Optional, Callable, Awaitable
from pydantic import BaseModel, Field, ValidationError
import os
import requests
from datetime import datetime


class Filter:
    def __init__(self):
        pass

    def inlet(self, body: dict) -> dict:
        body["sanitized"] = "".join(e for e in body.get("input", "") if e.isalnum())
        return body

    def outlet(self, body: dict) -> dict:
        for message in body.get("messages", []):
            if message.get("role") == "assistant":
                message["content"] = f"**{message['content']}**"
        return body


class RepositoryPipe:
    class Valves(BaseModel):
        MODEL_ID: str = Field(default="github_repo")

    def __init__(self):
        self.valves = self.Valves()

    def pipe(self, body: dict) -> str:
        repo_url = body.get("repo_url", "")
        return f"Fetched content from {repo_url}"


class Action:
    def __init__(self):
        pass

    def create_action_button(self):
        return {
            "type": "button",
            "title": "Analyze Repo",
            "action": "analyze_repository",
        }


async def emit_citation(__event_emitter__, content, title, url):
    await __event_emitter__(
        {
            "type": "citation",
            "data": {
                "document": [content],  # Ensure content is provided as list
                "metadata": [
                    {"date_accessed": datetime.now().isoformat(), "source": title}
                ],
                "source": {"name": title, "url": url},
            },
        }
    )


class Tools:
    class Valves(BaseModel):
        access_token: str = Field(
            default=os.getenv("GITHUB_ACCESS_TOKEN", ""),
            description="GitHub Personal Access Token (needs repo access)",
            json_schema_extra={"secret": True},
        )
        repo_url: str = Field(
            default=os.getenv("GITHUB_REPO_URL", ""),
            description="Default GitHub repository to access (in the format 'username/repo')",
        )

    class UserValves(BaseModel):
        max_files: int = Field(
            default=20,
            description="Maximum number of files per directory (optional to limit)",
        )
        truncate_content: bool = Field(
            default=True,
            description="Truncate large files for better readability",
        )
        max_content_length: int = Field(
            default=5000,
            description="Maximum character length for file contents when truncation is enabled",
        )

    def __init__(self):
        try:
            self.valves = self.Valves()
        except ValidationError as e:
            raise ValueError(f"Configuration error in Valves: {e}")

        self.user_valves = self.UserValves()
        self.filter = Filter()
        self.pipe = RepositoryPipe()
        self.action = Action()
        self.citation = False  # Ensure custom citations are managed

    async def _fetch_directory_contents(
        self,
        api_url: str,
        headers: dict,
        __event_emitter__: Optional[Callable[[Any], Awaitable[None]]] = None,
    ) -> Any:
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"Fetching contents from {api_url}...",
                        "done": False,
                        "hidden": False,
                    },
                }
            )

        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            return f"Error fetching from {api_url}: {response.status_code} - {response.text}"

        items = response.json()
        result = []
        file_count = 0
        for item in items:
            if file_count >= self.user_valves.max_files:
                break
            if item["type"] == "dir":
                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {
                                "description": f"Entering directory: {item['name']}...",
                                "done": False,
                            },
                        }
                    )
                sub_contents = await self._fetch_directory_contents(
                    item["url"], headers, __event_emitter__
                )
                result.append(
                    {
                        "name": item["name"],
                        "type": "dir",
                        "path": item["path"],
                        "contents": sub_contents,
                    }
                )
            elif item["type"] == "file":
                file_dict = {
                    "name": item["name"],
                    "type": "file",
                    "path": item["path"],
                }
                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {
                                "description": f"Fetching file: {item['name']}...",
                                "done": False,
                            },
                        }
                    )
                if item.get("download_url"):
                    file_response = requests.get(item["download_url"])
                    if file_response.status_code == 200:
                        content = file_response.text
                        if (
                            self.user_valves.truncate_content
                            and len(content) > self.user_valves.max_content_length
                        ):
                            content = (
                                content[: self.user_valves.max_content_length] + "..."
                            )
                        file_dict["content"] = content
                    else:
                        file_dict["content_error"] = (
                            f"Error fetching file content: {file_response.status_code}"
                        )
                result.append(file_dict)
                file_count += 1
            else:
                result.append(
                    {
                        "name": item.get("name"),
                        "type": item.get("type"),
                        "path": item.get("path"),
                        "detail": item,
                    }
                )

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"Finished fetching from {api_url}.",
                        "done": True,
                        "hidden": False,
                    },
                }
            )

        return result

    async def fetch_repo_content(
        self, __event_emitter__: Optional[Callable[[Any], Awaitable[None]]] = None
    ):
        if not self.valves.access_token or not self.valves.repo_url:
            msg = "Access token or repo URL is not properly configured."
            if __event_emitter__:
                await __event_emitter__(
                    {"type": "error", "data": {"description": msg, "done": True}}
                )
            return msg

        headers = {
            "Authorization": f"token {self.valves.access_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        if "/" not in self.valves.repo_url or len(self.valves.repo_url.split("/")) != 2:
            msg = "The repo_url is not in the expected 'username/repo' format."
            if __event_emitter__:
                await __event_emitter__(
                    {"type": "error", "data": {"description": msg, "done": True}}
                )
            return msg

        repo_api_url = f"https://api.github.com/repos/{self.valves.repo_url}/contents"

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "Fetching repository contents...",
                        "done": False,
                    },
                }
            )

        contents = await self._fetch_directory_contents(
            repo_api_url, headers, __event_emitter__
        )

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "Repository contents fetched successfully.",
                        "done": True,
                        "hidden": False,
                    },
                }
            )

        messages_wrapper = {"messages": contents}
        self.filter.outlet(messages_wrapper)

        if contents:
            repo_name = self.valves.repo_url.split("/")[1]
            for item in contents:
                if item.get("type") == "file":
                    file_name = item.get("name", "Unknown")
                    file_url = item.get("url", "Unknown")
                    await emit_citation(
                        __event_emitter__,
                        [item.get("content", "")],  # Ensure content is passed as list
                        f"Repo: {repo_name}, File: {file_name}",
                        file_url,
                    )

        return messages_wrapper.get("messages")

    async def analyze_repository(
        self,
        user: dict = {},
        __event_emitter__: Optional[Callable[[Any], Awaitable[None]]] = None,
    ):
        try:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "Starting repository analysis...",
                            "done": False,
                        },
                    }
                )

            content = await self.fetch_repo_content(__event_emitter__)

            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "Analysis completed successfully.",
                            "done": True,
                            "hidden": False,
                        },
                    }
                )

            return f"Repository contents:\n{content}"
        except Exception as e:
            error_msg = f"An error occurred: {e}"
            if __event_emitter__:
                await __event_emitter__(
                    {"type": "error", "data": {"description": error_msg, "done": True}}
                )
            return error_msg
