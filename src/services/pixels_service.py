import os
import requests
from pathlib import Path
from src.config import BASE_URL


class PexelsService:

    def __init__(self, api_key):
        self.api_key = api_key

    def search_and_download(
        self,
        query,
        per_page=3
    ):

        headers = {
            "Authorization": self.api_key
        }

        response = requests.get(
            BASE_URL,
            headers=headers,
            params={
                "query": query,
                "per_page": per_page
            }
        )

        data = response.json()

        downloaded_files = []

        Path(
            "output/media/videos"
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        for index, video in enumerate(
            data.get("videos", [])
        ):

            if not video["video_files"]:
                continue

            video_url = video["video_files"][0]["link"]

            file_name = (
                f"output/media/videos/"
                f"clip_{index}.mp4"
            )

            video_content = requests.get(
                video_url
            ).content

            with open(
                file_name,
                "wb"
            ) as file:
                file.write(video_content)

            downloaded_files.append(
                file_name
            )

        return downloaded_files