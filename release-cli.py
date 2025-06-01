import argparse  #prase cammand-line arguments
import subprocess #runs external shell command
import sys      #exits the script with custom exit code/messages
from core.language_detector.detect_language import detect_language      #custom function to detect the project language

LANGUAGE_COMMANDS = {
    "Python": {
        "path": "python-service",
        "run": "npx semantic-release"
    },
    "JavaScript": {
        "path": "js-service",
        "run": "npx semantic-release"
    },
    "Java": {
        "path": "java-service",
        "run": "npx semantic-release"
    },
    "Core": {
        "path": "core",
        "run": "npx semantic-release"
    }
}

def detect_scope(repo_path: str) -> str:
    import os

    try:
        changed_files = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD^"]
        ).decode().splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error detecting changed files: {e}")
        return detect_language(repo_path)

    print("\n📄 Changed files:")
    for f in changed_files:
        print(f" - {f}")

    # Normalize paths to avoid relative issues
    changed_files = [f.strip().lstrip("./") for f in changed_files]

    for file in changed_files:
        if (
            file == "release-cli.py"
            or file.startswith("core/")
            or file.startswith(".github/workflows/")
        ):
            print("\n Detected changes in core/shared logic.")
            print("language=Core")
            return "Core"

    # Fallback: detect based on file content
    lang = detect_language(repo_path)
    print(f"language={lang}")
    return lang

def run_release(lang: str):
    if lang not in LANGUAGE_COMMANDS:
        print(f" No release flow defined for language: {lang}")
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

    args = parser.parse_args()
    lang = detect_scope(args.repo_path)
    print(f"language={lang.lower()}")
    sys.exit(0)

if __name__ == "__main__":
    main()
