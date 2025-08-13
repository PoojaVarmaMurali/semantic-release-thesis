import os
import json
import cohere
import subprocess
import re

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
        "List each summary as a bullet point with clear headings for Change, Reason, and Impact.\n\n"
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
    # Detect current branch
    branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    ).decode().strip()

    if branch not in ("develop", "main"):
        print(f"ℹ️ Skipping release notes generation on '{branch}' branch (only 'develop' and 'main').")
        return

    # Use CWD as the release folder
    cwd = os.getcwd()
    commits_path = os.path.join(cwd, "commits.json")
    release_notes_path = os.path.join(cwd, "RELEASE_NOTES.md")
    if not os.path.exists(release_notes_path):
        print("Creating new RELEASE_NOTES.md file...")
        with open(release_notes_path, "w") as f:
            f.write("# Release Notes\n\n")
    


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
        text = f"{commit['subject']} {commit.get('body','')}"
        sections[category].append(text)

 

    body_md = ""

    for section, messages in sections.items():
        if not messages:
            continue

        emoji = {
            "Features": "✨",
            "Fixes": "🐛",
            "Chores": "🧹",
            "Other": "🔖"
        }.get(section, "🔖")

        print(f"\nSummarizing {len(messages)} commits in section '{section}'...")
        summary = query_batch(messages, section)

        body_md += f"### {emoji} {section}\n\n{summary}\n\n"

    # Load existing release notes if any
    with open(release_notes_path, "r") as f:
        existing_content = f.read()


    # ✅ pattern to find the current Unreleased block (if present)
    unreleased_pattern = r"## \[Unreleased\](?:.|\n)*?(?=\n## |\Z)"

    # Version (only used on main)
    version = os.getenv("RELEASE_VERSION", "Unreleased")

    if branch == "develop":
        # ✅ On develop: keep exactly one [Unreleased] block at the top (idempotent)
        new_unreleased = "## [Unreleased]\n\n" + body_md.strip() + "\n"
        # remove existing Unreleased block if present
        content_wo_unreleased = re.sub(unreleased_pattern, "", existing_content, flags=re.DOTALL)
        # ensure single top header; avoid duplicating "# Release Notes"
        if content_wo_unreleased.lstrip().startswith("# Release Notes"):
            # insert new block right after the header
            combined_content = re.sub(
                r"^# Release Notes\s*\n+",
                "# Release Notes\n\n" + new_unreleased + "\n",
                content_wo_unreleased,
                count=1,
                flags=re.M
            )
        else:
            combined_content = "# Release Notes\n\n" + new_unreleased + "\n" + content_wo_unreleased

    else:
        # ✅ On main: promote Unreleased → Version {version}, or prepend version section if none exists
        version_header = f"## 📦 Version {version}\n\n"
        if re.search(unreleased_pattern, existing_content, flags=re.DOTALL):
            # replace the Unreleased block with the versioned section
            combined_content = re.sub(
                unreleased_pattern,
                (version_header + body_md.strip() + "\n"),
                existing_content,
                count=1,
                flags=re.DOTALL
            )
        else:
            # no Unreleased block — just prepend versioned notes once
            if existing_content.lstrip().startswith("# Release Notes"):
                combined_content = re.sub(
                    r"^# Release Notes\s*\n+",
                    "# Release Notes\n\n" + version_header + body_md.strip() + "\n\n",
                    existing_content,
                    count=1,
                    flags=re.M
                )
            else:
                combined_content = "# Release Notes\n\n" + version_header + body_md.strip() + "\n\n" + existing_content

    # Save file
    with open(release_notes_path, "w") as f:
        f.write(combined_content.strip() + "\n")

    print("✅ Release notes updated (prepended) in: RELEASE_NOTES.md")

if __name__ == "__main__":
    main()
