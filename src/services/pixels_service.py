import os
import requests
from pathlib import Path
from src.config import BASE_URL

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


class PexelsService:

    def __init__(self, api_key):
        self.api_key = api_key

    def search_and_download(
        self,
        query,
        per_page=3,
        orientation="landscape"
    ):

        headers = {
            "Authorization": self.api_key
        }

        params = {
            "query": query,
            "per_page": per_page,
            "orientation": orientation
        }

        response = requests.get(
            BASE_URL,
            headers=headers,
            params=params
        )

        data = response.json()

        downloaded_files = []

        output_dir = os.path.join(
            BASE_DIR,
            "output",
            "media",
            "videos"
        )
        Path(output_dir).mkdir(
            parents=True,
            exist_ok=True
        )

        for index, video in enumerate(
            data.get("videos", [])
        ):

            if not video["video_files"]:
                continue

            video_url = video["video_files"][0]["link"]

            file_name = os.path.join(
                output_dir,
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