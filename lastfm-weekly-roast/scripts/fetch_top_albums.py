#!/usr/bin/env python3
"""
Cross-platform Last.fm Top Albums fetcher.
Works across Windows, Linux, and macOS using only Python standard library.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# Ensure UTF-8 output across platforms and consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


def load_dotenv_values() -> dict[str, str]:
    """Reads key-value pairs from ~/.env in user home directory."""
    env_file = Path.home() / ".env"
    values: dict[str, str] = {}
    if env_file.is_file():
        try:
            with open(env_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    values[k.strip()] = v.strip().strip("\"'")
        except OSError as e:
            print(f"Warning: Failed reading {env_file}: {e}", file=sys.stderr)
    return values


def get_api_key(cli_key: str | None = None, dotenv_vals: dict[str, str] | None = None) -> str:
    """Retrieves Last.fm API key from CLI argument, environment variable, or ~/.env."""
    if cli_key:
        return cli_key.strip()

    if "LASTFM_API_KEY" in os.environ and os.environ["LASTFM_API_KEY"].strip():
        return os.environ["LASTFM_API_KEY"].strip()

    if dotenv_vals and dotenv_vals.get("LASTFM_API_KEY"):
        return dotenv_vals["LASTFM_API_KEY"]

    print("Error: LASTFM_API_KEY not found in environment or ~/.env.", file=sys.stderr)
    print("Please set LASTFM_API_KEY in your ~/.env file or pass via -k / --api-key.", file=sys.stderr)
    sys.exit(1)


def get_username(cli_user: str | None = None, dotenv_vals: dict[str, str] | None = None) -> str:
    """Retrieves Last.fm username from CLI argument, environment variable, or ~/.env."""
    if cli_user:
        return cli_user.strip()

    if "LASTFM_USERNAME" in os.environ and os.environ["LASTFM_USERNAME"].strip():
        return os.environ["LASTFM_USERNAME"].strip()

    if dotenv_vals and dotenv_vals.get("LASTFM_USERNAME"):
        return dotenv_vals["LASTFM_USERNAME"]

    print("Error: Last.fm username not specified.", file=sys.stderr)
    print("Please set LASTFM_USERNAME in your ~/.env file or pass via -u / --username.", file=sys.stderr)
    sys.exit(1)


def fetch_top_albums(username: str, api_key: str, period: str = "7day", limit: int = 10) -> tuple[list[dict], dict]:
    """Calls Last.fm API user.getTopAlbums and returns (album_list, raw_json_data)."""
    params = urllib.parse.urlencode({
        "method": "user.getTopAlbums",
        "user": username,
        "period": period,
        "limit": limit,
        "api_key": api_key,
        "format": "json",
    })
    url = f"https://ws.audioscrobbler.com/2.0/?{params}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "LastfmRoastSkill/2.0 (compatible; Python/urllib)"},
    )

    try:
        with urllib.request.urlopen(req) as resp:
            raw_bytes = resp.read()
            data = json.loads(raw_bytes.decode("utf-8-sig"))
            albums = data.get("topalbums", {}).get("album", [])
            return albums, data
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        try:
            error_body = e.read().decode("utf-8", errors="ignore")
            print(error_body, file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Fetch top albums for a Last.fm user (Windows/Linux/Mac).")
    parser.add_argument("-u", "--username", default=None, help="Last.fm username (optional; defaults to ~/.env or LASTFM_USERNAME)")
    parser.add_argument("-k", "--api-key", default=None, help="Last.fm API key (optional; defaults to ~/.env or LASTFM_API_KEY)")
    parser.add_argument(
        "-p",
        "--period",
        default="7day",
        choices=["7day", "1month", "3month", "6month", "12month", "overall"],
        help="Time period (default: 7day)",
    )
    parser.add_argument("-l", "--limit", type=int, default=10, help="Number of albums to retrieve (default: 10)")
    parser.add_argument("-o", "--out-file", default=None, help="Optional path to write formatted album text")
    parser.add_argument("--raw-json", default=None, help="Optional path to write the raw Last.fm JSON response")
    parser.add_argument("--json", action="store_true", help="Print raw JSON to stdout instead of formatted text")

    args = parser.parse_args()

    dotenv_vals = load_dotenv_values()
    api_key = get_api_key(args.api_key, dotenv_vals)
    username = get_username(args.username, dotenv_vals)
    albums, raw_data = fetch_top_albums(username, api_key, args.period, args.limit)

    # Save raw JSON if requested
    if args.raw_json:
        out_raw_path = Path(args.raw_json)
        out_raw_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_raw_path, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=2)
        print(f"Raw JSON saved to: {out_raw_path}", file=sys.stderr)

    if args.json:
        formatted = json.dumps(raw_data, ensure_ascii=False, indent=2)
    else:
        lines = []
        for a in albums[:args.limit]:
            name = a.get("name", "Unknown Album")
            artist = a.get("artist", {}).get("name", "Unknown Artist")
            playcount = a.get("playcount", "0")
            lines.append(f"{name} | {artist} | {playcount}")
        formatted = "\n".join(lines)

    # Save formatted text if requested
    if args.out_file:
        out_path = Path(args.out_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(formatted)
        print(f"Formatted text saved to: {out_path}", file=sys.stderr)

    # Print to stdout
    print(formatted)


if __name__ == "__main__":
    main()
