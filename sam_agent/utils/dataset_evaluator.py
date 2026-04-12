"""Utility for evaluating the agent against a public multi-object dataset.

The script downloads the dataset provided at
https://github.com/inbarhub/single_image_dataset/tree/main/images and
sends each image with a descriptive prompt to a Gemini vision model. This
is intended for quick manual checks that the agent can describe and count
objects in images with many items.

Usage:
    python -m sam_agent.utils.dataset_evaluator --prompt "Describe ..."
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

import requests

try:
    import google.genai as genai
    from google.genai import types as genai_types
except ImportError as exc:  # pragma: no cover - informative error at runtime
    raise ImportError(
        "google-genai is required for dataset evaluation; add it to your environment"
    ) from exc


DATASET_LIST_URL = (
    "https://api.github.com/repos/inbarhub/single_image_dataset/contents/images"
)
DEFAULT_PROMPT = (
    "Describe the picture: what kind of objects can you see on it, and how many of"
    " them?"
)
DEFAULT_MODEL = "gemini-1.5-flash"


@dataclass
class DatasetImageResult:
    image: str
    prompt: str
    model: str
    response_text: str


def download_dataset(target_dir: Path) -> List[Path]:
    """Download dataset images into ``target_dir``.

    Returns a list of downloaded image paths. Existing files are reused.
    """

    target_dir.mkdir(parents=True, exist_ok=True)
    response = requests.get(DATASET_LIST_URL, timeout=30)
    response.raise_for_status()
    entries = response.json()

    image_paths: List[Path] = []
    for entry in entries:
        if entry.get("type") != "file":
            continue
        download_url = entry.get("download_url")
        name = entry.get("name")
        if not download_url or not name:
            continue

        destination = target_dir / name
        if not destination.exists():
            file_response = requests.get(download_url, timeout=30)
            file_response.raise_for_status()
            destination.write_bytes(file_response.content)
        image_paths.append(destination)

    return image_paths


def evaluate_images(
    image_paths: Iterable[Path],
    prompt: str,
    model_name: str = DEFAULT_MODEL,
) -> List[DatasetImageResult]:
    """Send each image to Gemini with the provided prompt."""

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set; cannot run vision evaluation.")

    client = genai.Client(api_key=api_key)
    results: List[DatasetImageResult] = []
    for image_path in image_paths:
        image_bytes = image_path.read_bytes()
        response = client.models.generate_content(
            model=model_name,
            contents=[
                genai_types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                prompt,
            ],
            generation_config=genai_types.GenerationConfig(
                temperature=0.2, max_output_tokens=256
            ),
        )

        results.append(
            DatasetImageResult(
                image=image_path.name,
                prompt=prompt,
                model=model_name,
                response_text=response.text or "",
            )
        )

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--download-dir",
        type=Path,
        default=Path("data/single_image_dataset"),
        help="Where to store the downloaded dataset images.",
    )
    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="Prompt to send along with each image.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Gemini model name to query.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to write JSON results.",
    )
    args = parser.parse_args()

    images = download_dataset(args.download_dir)
    if not images:
        raise SystemExit("No dataset images found to evaluate.")

    results = evaluate_images(images, prompt=args.prompt, model_name=args.model)
    results_payload = [result.__dict__ for result in results]

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results_payload, indent=2))

    print(json.dumps(results_payload, indent=2))


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    main()
