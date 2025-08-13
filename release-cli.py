import argparse  #prase cammand-line arguments
import subprocess #runs external shell command
import sys      #exits the script with custom exit code/messages
import json
from core.language_detector.detect_language import detect_language      #custom function to detect the project language

LANGUAGE_COMMANDS = {
    "python": {
        "path": "python-service",
        "run": "npx semantic-release"
    },
    "javascript": {
        "path": "js-service",
        "run": "npx semantic-release"
    },
    "java": {
        "path": "java-service",
        "run": "npx semantic-release"
    },
    "core": {
        "path": "core",
        "run": "npx semantic-release"
    }
}

def detect_scope(repo_path: str) -> str:
    try:
        # Get the latest 2 non-merge commits
        commits = subprocess.check_output(
            ["git", "rev-list", "--no-merges", "-n", "2", "HEAD"]
        ).decode().splitlines()

        if len(commits) < 2:
            print("Not enough commits to compare.")
            return detect_language(repo_path).strip().lower()

        latest_commit, previous_commit = commits

        changed_files = subprocess.check_output(
            ["git", "diff", "--name-only", previous_commit, latest_commit]
        ).decode().splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error detecting changed files: {e}")
        return detect_language(repo_path).strip().lower()

    print("\n Changed files:")
    for f in changed_files:
        print(f" - {f}")

    # Normalize paths to avoid relative issues
    changed_files = [f.strip().lstrip("./") for f in changed_files]

    top_dirs = set()
    for file in changed_files:
        normalized = file.strip().lstrip("./")

        if normalized == "release-cli.py" or normalized.startswith(".github/") or normalized.startswith("core/"):
            top_dirs.add("core")
        else:
            top_dir = normalized.split('/')[0]
            top_dirs.add(top_dir)

    langs = set()
    if "js-service" in top_dirs:
        langs.add("javascript")
    if "python-service" in top_dirs:
        langs.add("python")
    if "java-service" in top_dirs:
        langs.add("java")
    if "core" in top_dirs:
        langs.add("core")
    if not langs:
        detected = detect_language(repo_path)
        if not detected or detected == ["Unknown"]:
          return []
        return detected if isinstance(detected, list) else [detected]
    return list(langs)

def run_release(lang: str):
    
    if lang not in LANGUAGE_COMMANDS:
        print(f" No release flow defined for language: {lang}")
        print(f"Available options: {list(LANGUAGE_COMMANDS.keys())}")
        sys.exit(1)

    folder = LANGUAGE_COMMANDS[lang]["path"]
    command = LANGUAGE_COMMANDS[lang]["run"]

    print(f"\n Detected language: {lang}")
    print(f" Using project folder: {folder}")
    print(f" Running: {command}\n")

    try:
        subprocess.run(command, cwd=folder, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f" Semantic release failed: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Semantic Release CLI Tool")
    parser.add_argument("repo_path", help="Path to the project directory")
    parser.add_argument("--run", action="store_true", help="Run release for detected language")
    
    args = parser.parse_args()
    langs = detect_scope(args.repo_path)
    if isinstance(langs, list):
        print(f"languages={json.dumps(langs)}")
    else:
        print(f"language={langs}")
        langs = [langs]

    if args.run:
        for lang in langs:
            print(f"DEBUG: lang={lang}, available keys={list(LANGUAGE_COMMANDS.keys())}")
            run_release(lang)

if __name__ == "__main__":
    main()
