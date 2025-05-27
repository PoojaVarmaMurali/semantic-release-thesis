import os
from collections import defaultdict

# Define language signatures
SIGNATURES = {
    "Python": {
        "strong": {"setup.py", "pyproject.toml"},
        "moderate": {"requirements.txt"},
        "extensions": {".py"}
    },
    "JavaScript": {
        "strong": set(),
        "moderate": {"package.json"},
        "extensions": {".js", ".ts"}
    },
    "Java": {
        "strong": {"pom.xml", "build.gradle"},
        "moderate": set(),
        "extensions": {".java"}
    }
}

def detect_language(repo_path: str) -> str:
    scores = defaultdict(int)
    EXCLUDE_DIRS = {"node_modules", "venv", "__pycache__", ".git", ".idea", ".mvn"}
    
    print(f"Scanning repo: {repo_path}\n")
    
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)

            for lang, rules in SIGNATURES.items():
                if file in rules["strong"]:
                    scores[lang] += 10
                elif file in rules["moderate"]:
                    scores[lang] += 3
                elif ext in rules["extensions"]:
                    scores[lang] += 3

    if not scores:
        print("Scoring breakdown: none")
        return "Unknown"
    
    print("\n Scoring breakdown:")
    for lang, score in scores.items():
        print(f"  {lang}: {score}")

    return max(scores, key=scores.get)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python detect_language.py <repo_path>")
    else:
        detected = detect_language(sys.argv[1])
        print(f"\n Detected language: {detected}")
  