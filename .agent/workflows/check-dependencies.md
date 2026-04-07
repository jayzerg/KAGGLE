---
description: Identify and prevent library bundle bloat
---

# /check-dependencies - Analyze Bundle Bloat

This workflow is designed to prevent excessive bundle sizes by scanning for heavy dependencies and inefficient import patterns before they are fully integrated.

## Task
Run bundle size validation using the project's internal checklist tool to maintain optimal application performance.

### Steps:

1. **Run Checklist Scan**
   - Execute the internal checklist module to audit the current dependencies and overall project health:
// turbo
```powershell
python .agent/scripts/checklist.py .
```

2. **Analyze Dependency Bloat**
   - Review `package.json`, `requirements.txt`, or dependency lockfiles for known heavy libraries.
   - Scan codebase for inefficient **barrel file imports** (e.g., importing from an entire root library instead of a specific sub-module).
   - Flag unused, deprecated, or overlapping dependencies.

3. **Apply Agent Optimization Rules**
   - Adhere to the bundle size optimization rules referenced in the project's performance-profiling skill.
   - Evaluate whether identified heavy dependencies can be replaced with lightweight alternatives or native APIs.

4. **Action Plan & Remediation**
   - Present a concise report to the developer detailing bloat risks and estimated size impacts.
   - Propose refactoring paths (e.g., direct imports).
   - Execute removal or refactoring after user approval and verify with a final optimization pass.

---
## Usage Example

```
/check-dependencies
```
