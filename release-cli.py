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

    # Check if the core/shared logic has changed
    changed_files = subprocess.check_output(["git", "diff", "--name-only", "HEAD^"]).decode().splitlines()

    for file in changed_files:
        if (
            file.startswith("core/")
            or file == "release-cli.py"
            or file == ".github/workflows/universal-release.yml"
            or file.startswith(".github/workflows/")
        ):
            print("\n Detected changes in core/shared logic")
            print("language=Core")
            return "Core"
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
    lang = detect_language(args.repo_path)
    print(f"language={lang}")
    run_release(lang)

if __name__ == "__main__":
    main()
