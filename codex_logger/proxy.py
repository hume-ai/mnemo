import os
import json

import httpx
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from .db import SessionLocal, init_db, Interaction

# Ensure tables exist
init_db()

app = FastAPI(title='codex-logger-proxy')

@app.post('/v1/{full_path:path}')
async def proxy(full_path: str, request: Request):
    """
    Catch-all POST proxy for /v1/* requests to OpenAI.
    Logs the prompt and response to the local SQLite DB.
    """
    # Load request data
    payload = await request.json()
    model = payload.get('model')
    # Extract prompt text from chat messages or plain text
    messages = payload.get('messages')
    if isinstance(messages, list):
        prompt_text = '\n'.join(
            msg.get('content', '') for msg in messages if msg.get('role') == 'user'
        )
    else:
        prompt_text = payload.get('prompt', '')

    # Forward the request to the real OpenAI API
    headers = {k: v for k, v in request.headers.items() if k.lower().startswith(('authorization', 'openai-'))}
    url = f'https://api.openai.com/v1/{full_path}'
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json=payload)
        result = resp.json()

    # Record the interaction
    # Use environment variables for project/session context
    proj_id = os.getenv('CODEX_LOGGER_PROJECT_ID')
    sess_id = os.getenv('CODEX_LOGGER_SESSION_ID')
    try:
        db = SessionLocal()
        inter = Interaction(
            session_id=int(sess_id) if sess_id else None,
            prompt=prompt_text,
            chain_of_thought=None,
            response=json.dumps(result) if full_path.startswith('chat') else result.get('choices', [{}])[0].get('message', {}).get('content', str(result)),
            model=model or ''
        )
        db.add(inter)
        db.commit()
    except Exception:
        pass
    finally:
        db.close()

    return JSONResponse(status_code=resp.status_code, content=result)