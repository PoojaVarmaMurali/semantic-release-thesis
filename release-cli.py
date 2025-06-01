import argparse  #prase cammand-line arguments
import subprocess #runs external shell command
import sys      #exits the script with custom exit code/messages
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
        changed_files = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD~1"]
        ).decode().splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error detecting changed files: {e}")
        return detect_language(repo_path).strip().lower()

    print("\n Changed files:")
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
            return "core"

    return detect_language(repo_path).strip().lower()

def run_release(lang: str):
    print(f"DEBUG: lang={lang}, available keys={list(LANGUAGE_COMMANDS.keys())}")

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
    parser.add_argument("--run", action="store_true", help="Run release for detected language")
    
    args = parser.parse_args()
    lang = detect_scope(args.repo_path).strip().lower()
    print(f"language={lang}") 

    if args.run:
        print(f"DEBUG: lang={lang}, available keys={list(LANGUAGE_COMMANDS.keys())}")
        run_release(lang)

if __name__ == "__main__":
    main()
