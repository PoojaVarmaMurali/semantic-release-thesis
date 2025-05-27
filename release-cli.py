import argparse
import subprocess
import sys
from language_detector.detect_language import detect_language 

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
    }
}

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
    run_release(lang)

if __name__ == "__main__":
    main()
