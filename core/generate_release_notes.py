#!/usr/bin/env python3
import os
import json
import sys
import cohere

# Load Cohere API key securely from environment variable
api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise ValueError("COHERE_API_KEY environment variable not set.")

cohere_client = cohere.Client(api_key)

def classify_commit(subject):
    subject = subject.lower()
    if subject.startswith("feat:"):
        return "Features"
    if subject.startswith("fix:"):
        return "Fixes"
    if subject.startswith("chore:"):
        return "Chores"
    return "Other"

def query_batch(commits, section):
    """
    Summarizes a list of commits in one request, returning bullet points.
    """
    prompt = (
        f"Summarize the following {section.lower()} commits clearly. "
        "List each summary as a bullet point, specifying what was changed, why it was changed, "
        "and any impact on the project.\n\n"
    )
    for i, commit in enumerate(commits, 1):
        prompt += f"{i}. {commit}\n"

    response = cohere_client.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=400,
        temperature=0.2,
    )
    return response.generations[0].text.strip()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))
    commits_path = os.path.join(repo_root, "commits.json")

    if not os.path.exists(commits_path):
        print("No commits.json found. Skipping release notes generation.")
        sys.exit(0)

    with open(commits_path) as f:
        commits = json.load(f)

    if not commits:
        print("No commits to process. Skipping release notes generation.")
        sys.exit(0)

    sections = {
        "Features": [],
        "Fixes": [],
        "Chores": [],
        "Other": []
    }

    for commit in commits:
        category = classify_commit(commit["subject"])
        text = f"{commit['subject']} {commit['body']}"
        sections[category].append(text)

    markdown = "# Release Notes\n\n"

    for section, messages in sections.items():
        if not messages:
            continue

        print(f"\nSummarizing {len(messages)} commits in section '{section}'...")
        summary = query_batch(messages, section)

        markdown += f"## {section}\n\n"
        markdown += summary + "\n"

    with open("RELEASE_NOTES.md", "w") as f:
        f.write(markdown)

    print("✅ Release notes generated: RELEASE_NOTES.md")

if __name__ == "__main__":
    main()
