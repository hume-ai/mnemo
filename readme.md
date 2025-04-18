 # codex-logger
 
 Open-source tool to log and organize Codex/GPT interactions by project and session.

 Getting Started
---------------
1. Copy the example env and set your keys:
   ```bash
   cp .env.example .env
   # edit .env: set OPENAI_API_KEY and DATABASE_URL if needed
   ```
2. Start the backend (from the project root, so it can import `backend` as a module):
   ```bash
   pip install -r backend/requirements.txt
   uvicorn backend.main:app --reload
   ```
3. Start the frontend (in a separate shell):
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Visit http://localhost:3000 to view the UI.
4. Seed a project, session & interaction via the CLI wrapper (from project root):
   ```bash
   # Install the package (editable mode)
   pip install -e .
   # Ensure your real `codex` CLI is on PATH, or set its location:
   export ORIGINAL_CODEX_CLI=$(which codex)
   # Run the wrapper in place of `codex`:
   codex --session "Initial Session" --approval-mode full-auto "Hello world"
   ```
   Refresh the UI to see your new project, session, and interactions.

5. Any invocation of `codex ...` now goes through your logger proxy, so you can use all standard codex flags (e.g. `--approval-mode full-auto`).