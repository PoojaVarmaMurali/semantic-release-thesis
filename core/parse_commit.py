#Get commits since the last tag, Extraxt their messages and store it in JSON
import subprocess
import json
import os

def get_latest_tag():
    try:
        tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode().strip()
    except subprocess.CalledProcessError:
        tag = None
    return tag

def get_commits(since_tag=None):
    if since_tag:
        range_arg = f"{since_tag}..HEAD"
    else:
        range_arg = "HEAD"

    raw = subprocess.check_output(
        ["git", "log", "--no-merges", "--pretty=format:%H||%s||%b", range_arg]
    ).decode()

    commits = []
    for line in raw.strip().split("\n"):
        parts = line.split("||")
        if len(parts) >= 2:
            subject = parts[1].lower()
            if subject.startswith("chore(release)"):
                continue  # skip release commits
            commits.append({
                "hash": parts[0],
                "subject": parts[1],
                "body": parts[2] if len(parts) > 2 else ""
            })
    return commits


if __name__ == "__main__":
    # Write commits.json in the current working directory
    cwd = os.getcwd()
    commits_path = os.path.join(cwd, "commits.json")

    tag = get_latest_tag()
    commits = get_commits(tag)

    with open(commits_path, "w") as f:
        json.dump(commits, f, indent=2)

    print(f"Extracted {len(commits)} commits since {tag} into {commits_path}")
