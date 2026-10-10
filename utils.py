"""Reusable helpers: configuration, Ollama access, formatting and file handling."""

import json
import os
import re

import ollama

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
MODEL_DIR = os.path.join(BASE_DIR, "models")

RECOMMENDATION_FILE = os.path.join(OUTPUT_DIR, "recommendations.txt")
PROFILE_FILE = os.path.join(OUTPUT_DIR, "user_profile.json")
RESULT_FILE = os.path.join(OUTPUT_DIR, "recommendation_result.json")

OLLAMA_MODEL = "llama3.2:latest"

LINE = "=" * 64
DASH = "-" * 64

_client = ollama.Client()


class ModelError(Exception):
    """Raised when the local model cannot serve the request."""


def check_model():
    """Verify the Ollama server is reachable and the model is installed."""
    try:
        models = _client.list()
    except Exception:
        raise ModelError("Cannot reach Ollama. Start it with:  ollama serve")
    names = [m.get("model") or m.get("name") for m in models.get("models", [])]
    if OLLAMA_MODEL not in names:
        raise ModelError("Model {} is not installed. Run:  ollama pull {}".format(
            OLLAMA_MODEL, OLLAMA_MODEL.split(":")[0]))
    return names


def ask(system_prompt, user_prompt, temperature=0.6):
    """Send a prompt to the local model served by Ollama."""
    try:
        response = _client.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_prompt}],
            options={"temperature": temperature},
        )
    except Exception as exc:
        raise ModelError("Model request failed: {}".format(exc))
    text = response["message"]["content"].strip()
    if not text:
        raise ModelError("The model returned an empty response.")
    return text


def banner(title):
    print(LINE)
    print(title)
    print(LINE)


def clean_item(text):
    """Strip list markers and quotes from one line of a model reply."""
    return re.sub(r"^\s*(?:\d+[\.\)]|[-*])\s*", "", text).strip().strip('"').strip()


# ------------------------------------------------------------------- files
def _write_json(path, data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def _read_json(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def save_profile(profile):
    _write_json(PROFILE_FILE, profile)


def load_profile():
    return _read_json(PROFILE_FILE)


def save_result(result):
    _write_json(RESULT_FILE, result)


def load_result():
    return _read_json(RESULT_FILE)


def require_profile():
    profile = load_profile()
    if profile is None:
        print("No user profile found. Please enter your details first.")
    return profile


def require_recommendations():
    result = load_result()
    if not result or not result.get("items"):
        print("No recommendations found. Please generate recommendations first.")
        return None
    return result
