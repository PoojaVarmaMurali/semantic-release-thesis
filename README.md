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

Javascript:

All Semantic Release config and dependencies for JavaScript live inside js-service/.