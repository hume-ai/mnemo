 # Prompt for Building a Codex Session Logger with Project-Based Context

 I'm building an **open-source developer tool** that logs and organizes all my Codex (or GPT) conversations into sessions, structured around individual projects. This tool will help developers track, retrieve, and reuse AI-assisted coding workflows across different codebases.

 ## Goal

 Capture and store every Codex interaction in a session-managed, project-aware way, with a local UI to browse and retrieve all interactions.

 ## Core Requirements

 1. Codex Wrapper: intercept calls, log prompts, chain-of-thought, responses, timestamps, session & project IDs.
 2. Project-Based Session Structure: projects inferred from Git repo or created manually; sessions per project.
 3. Database Schema: Projects, Sessions, Interactions tables (id, session_id, prompt, response, model, etc.).
 4. Local Web UI: FastAPI/Flask + React/Next.js to list/search interactions.
 5. CLI Tool: start sessions, select/create projects, invoke Codex with logging, auto-detect Git project.
 6. Open-Source Project Structure as outlined in docs.

 ## Deliverables

 - Backend API + DB models
 - Frontend stack with sample pages
 - CLI wrapper to log a Codex interaction
 - DB migration scripts
 - Folder structure
 - Example: logging an interaction from a Git-tracked project