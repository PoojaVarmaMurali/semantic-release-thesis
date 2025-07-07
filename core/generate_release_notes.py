import os
import json
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
    commits_path = os.path.join(repo_root, "core", "commits.json")
    release_notes_path = os.path.join(repo_root, "core", "RELEASE_NOTES.md")


    if not os.path.exists(commits_path):
        raise FileNotFoundError(f"Commits file not found: {commits_path}")

    with open(commits_path) as f:
        commits = json.load(f)

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

    # Compose new release notes
    markdown = "# Release Notes\n\n"

    for section, messages in sections.items():
        if not messages:
            continue

        print(f"\nSummarizing {len(messages)} commits in section '{section}'...")
        summary = query_batch(messages, section)

        markdown += f"## {section}\n\n"
        markdown += summary + "\n\n"

    # Load existing release notes if any
    if os.path.exists(release_notes_path):
        with open(release_notes_path, "r") as f:
            existing_content = f.read()
    else:
        existing_content = ""

    # Write new release notes with latest at the top
    with open(release_notes_path, "w") as f:
        f.write(markdown.strip() + "\n\n")
        f.write(existing_content.strip())

    print("✅ Release notes updated (prepended) in: RELEASE_NOTES.md")

if __name__ == "__main__":
    main()
