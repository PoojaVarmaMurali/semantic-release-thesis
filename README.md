# semantic-release-thesis

- Multi-Language Adaptive Configuration & AI-Powered Release Notes in Semantic Release  
- Semantic Release mainly works based on the conventional commit messages.  

### Conventional Commit Cheat Sheet:
- **Format:**  
    `<type>(<scope>): <short summary>`  

    1. `<type>`: Kind of change (required)  
    2. `<scope>`: Project or module (optional but helpful — use js, python, or java)  
    3. `<summary>`: Short and clear message  

- **Common Types:**  

    | Type              | Description                           | Version Impact  |
    | ----------------- | ------------------------------------- | --------------- |
    | `feat`            | New feature added                     | **Minor** bump  |
    | `fix`             | Bug fix or patch                      | **Patch** bump  |
    | `chore`           | Internal tooling, configs, scripts    | No version bump |
    | `docs`            | Documentation-only changes            | No version bump |
    | `refactor`        | Code refactor, no behavior change     | No version bump |
    | `test`            | Add/update tests                      | No version bump |
    | `ci`              | CI/CD changes (e.g., workflows)       | No version bump |
    | `style`           | Code formatting, comments, lint fixes | No version bump |
    | `perf`            | Performance improvement               | **Patch** bump  |
    | `build`           | Build script/config update            | No version bump |
    | `BREAKING CHANGE` | Introduces breaking API change        | **Major** bump  |  

### Commit Message Best Practices Specific to the Thesis:
- Use lowercase types (e.g., `feat`, not `Feat`)  
- Keep summaries under 70 characters  
- Use scopes for clarity in multi-language repos  
- Avoid vague messages like `fix: stuff` or `update`  

### Folder structure and brief

Javascript:

All Semantic Release config and dependencies for JavaScript live inside js-service/.

Java:

All Semantic Release config and dependencies for JavaScript live inside java-service/.

Python:

All Semantic Release config and dependencies for JavaScript live inside python-service/.

Core:

This folder containes all the shared files/scripts and configurations. 

.github/workflows/universal-release.yml --> This is the universal workflow for all the languages and the shared repository.



### Release Notes Generation

This project uses automated scripts to generate release notes and commit metadata:

- `commits.json`: created by `parse_commit.py`
- `RELEASE_NOTES.md`: created by `generate_release_notes.py`

These files are **ignored in version control** (`.gitignore`) and are regenerated automatically during CI/CD workflows.

 **Do not commit these files manually.**

If you need to see the generated release notes:
- Look at the GitHub Actions workflow artifacts.
- Run the scripts locally if needed.
 
### Thesis Objective

This project aims to extend the functionality of Semantic Release to support:

1. Multi-language monorepos: with scoped configuration for JavaScript, Python, Java

2. AI-powered human-readable release notes: summarizing commit context in plain English

3. Branch-specific behavior: Pre-releases on develop and stable releases on main

It builds a production-ready automation system for consistent versioning and changelog generation across different languages.

### Language Detection Logic

The workflow includes automatic detection of which service (language) has changed, using:

File extension patterns (e.g., .js, .py, .java)

Project-specific files (e.g., setup.py, pom.xml, package.json)

Git diff analysis to scope changed folders

Fallback detection using directory scoring logic

This enables only the changed language workflows to run per commit.