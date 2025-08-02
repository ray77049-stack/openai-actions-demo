import os
import json
from typing import List, Dict, Any


class PinterestScheduler:
    """Client for scheduling image uploads to Pinterest."""

    base_url = "https://api.pinterest.com/v5"

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    def create_pin(
        self,
        board_id: str,
        image_path: str,
        title: str,
        description: str,
        scheduled_time: str | None = None,
    ) -> Dict[str, Any]:
        """Upload an image as a Pinterest pin.

        Parameters
        ----------
        board_id:
            The identifier of the Pinterest board.
        image_path:
            Local path to the image file.
        title:
            Title for the pin.
        description:
            Description for the pin.
        scheduled_time:
            Optional ISO 8601 timestamp when the pin should be published.
        """
        url = f"{self.base_url}/pins"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data: Dict[str, Any] = {
            "board_id": board_id,
            "title": title,
            "description": description,
        }
        if scheduled_time:
            data["scheduled_time"] = scheduled_time
        import requests

        with open(image_path, "rb") as image_file:
            files = {"image": image_file}
            response = requests.post(url, headers=headers, data=data, files=files, timeout=30)
        response.raise_for_status()
        return response.json()


def load_schedule(schedule_path: str) -> List[Dict[str, Any]]:
    with open(schedule_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_schedule(schedule: List[Dict[str, Any]], dry_run: bool = False) -> None:
    access_token = os.environ.get("PINTEREST_ACCESS_TOKEN")
    if not access_token:
        raise RuntimeError("PINTEREST_ACCESS_TOKEN environment variable not set")
    scheduler = PinterestScheduler(access_token)
    for entry in schedule:
        if dry_run:
            print(
                f"Would upload {entry['image_path']} to board {entry['board_id']} at {entry.get('scheduled_time')}"
            )
        else:
            scheduler.create_pin(
                board_id=entry["board_id"],
                image_path=entry["image_path"],
                title=entry["title"],
                description=entry.get("description", ""),
                scheduled_time=entry.get("scheduled_time"),
            )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Schedule Pinterest image uploads")
    parser.add_argument("schedule", help="Path to JSON file describing pins")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show actions without calling Pinterest API"
    )
    args = parser.parse_args()

    schedule = load_schedule(args.schedule)
    run_schedule(schedule, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
