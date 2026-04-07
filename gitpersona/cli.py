"""Command-line interface for GitPersona."""

import argparse
import json
import os
import sys

from .analysis import analyze_user
from .github_client import GitHubClient


def build_parser():
    p = argparse.ArgumentParser(
        prog="gitpersona", description="Analyze a GitHub user's persona and stats"
    )
    sub = p.add_subparsers(dest="cmd")

    analyze = sub.add_parser("analyze", help="Analyze a GitHub username")
    analyze.add_argument("username", help="GitHub username to analyze")
    analyze.add_argument("--output", "-o", help="Write JSON output to file")
    analyze.add_argument(
        "--token",
        "-t",
        help="GitHub API token (overrides GITHUB_TOKEN env var)",
    )

    return p


def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.cmd == "analyze":
        token = args.token or os.environ.get("GITHUB_TOKEN")
        client = GitHubClient(token=token)
        try:
            data = client.fetch_user_repos(args.username)
        except Exception as exc:  # network or GitHub errors
            print(f"Error fetching data for {args.username}: {exc}", file=sys.stderr)
            return 2

        try:
            result = analyze_user(args.username, data)
        except Exception as exc:
            print(f"Error analyzing data: {exc}", file=sys.stderr)
            return 3

        text = json.dumps(result, indent=2)
        if args.output:
            try:
                with open(args.output, "w") as f:
                    f.write(text)
                print(f"Wrote analysis to {args.output}")
            except Exception as exc:
                print(f"Error writing output file: {exc}", file=sys.stderr)
                return 4
        else:
            print(text)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
