#!/usr/bin/env python3
import os
import sys
# Add project root to Python path so 'backend' module is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import click
import openai
import git
from sqlalchemy.orm import Session
from dotenv import load_dotenv
# Database imports
from backend.db.database import SessionLocal
from backend.db.models import Project, Session as DBSession, Interaction

# Auto-create missing tables (projects, sessions, interactions)
from backend.db.database import engine, Base
import backend.db.models
Base.metadata.create_all(bind=engine)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_or_create_project(db: Session, path: str):
    from os.path import basename
    name = basename(path)
    proj = db.query(Project).filter(Project.path == path).first()
    if not proj:
        proj = Project(name=name, path=path)
        db.add(proj)
        db.commit()
        db.refresh(proj)
    return proj

def get_or_create_session(db: Session, project_id: int, title: str):
    sess = db.query(DBSession).filter(DBSession.project_id == project_id, DBSession.title == title).first()
    if not sess:
        sess = DBSession(project_id=project_id, title=title)
        db.add(sess)
        db.commit()
        db.refresh(sess)
    return sess

@click.command()
@click.option('--project', '-p', default=None, help='Project path (git repo)')
@click.option('--session', '-s', required=True, help='Session title')
@click.option('--model', '-m', default='gpt-4', help='Model name')
@click.option('--prompt', '-q', 'prompt', required=False, help='Prompt text')
def main(project, session, model, prompt):
    db = SessionLocal()
    if not project:
        try:
            repo = git.Repo('.', search_parent_directories=True)
            project = repo.working_tree_dir
        except git.InvalidGitRepositoryError:
            click.echo('Not a git repository. Use --project.', err=True)
            sys.exit(1)
    proj = get_or_create_project(db, project)
    db_sess = get_or_create_session(db, proj.id, session)
    if not prompt:
        prompt = click.prompt('Prompt', type=str)
    # Use new v1 OpenAI API: chat.completions.create instead of ChatCompletion
    resp = openai.chat.completions.create(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
    )
    content = resp.choices[0].message.content
    interaction = Interaction(
        session_id=db_sess.id,
        prompt=prompt,
        chain_of_thought=None,
        response=content,
        model=model
    )
    db.add(interaction)
    db.commit()
    click.echo(content)

if __name__ == '__main__':
    main()