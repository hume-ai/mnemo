import os
import sys
import time
import shutil
import subprocess

import click
import git

from .db import SessionLocal, init_db, Project, Session as DBSession

# Allow unknown options to pass through to real 'codex'
@click.command(context_settings={
    'ignore_unknown_options': True,
    'allow_extra_args': True,
})
@click.option('--project', '-p', default=None, help='Project path (git repo)')
@click.option('--session', '-s', 'title', required=True, help='Session title')
@click.option('--port', '-P', default=5000, help='Port for local proxy')
@click.pass_context
def main(ctx, project, title, port):
    """
    Entry point for the `codex` CLI wrapper.
    Spawns a local proxy to intercept ChatCompletion calls,
    logs them by project/session, and then execs the real `codex` binary.
    """
    # Determine project path
    cwd = os.getcwd()
    if not project:
        try:
            project = git.Repo(cwd, search_parent_directories=True).working_tree_dir
        except git.InvalidGitRepositoryError:
            click.echo('Not a git repository; please specify --project', err=True)
            sys.exit(1)

    # Initialize DB and ensure tables
    init_db()
    db = SessionLocal()
    # Create or get Project record
    from os.path import basename
    proj_name = basename(project)
    proj = db.query(Project).filter(Project.path == project).first()
    if not proj:
        proj = Project(name=proj_name, path=project)
        db.add(proj); db.commit(); db.refresh(proj)
    # Create or get Session record
    sess = db.query(DBSession).filter(DBSession.project_id == proj.id, DBSession.title == title).first()
    if not sess:
        sess = DBSession(project_id=proj.id, title=title)
        db.add(sess); db.commit(); db.refresh(sess)
    db.close()

    # Prepare environment for proxy and real CLI
    env = os.environ.copy()
    env['CODEX_LOGGER_PROJECT_ID'] = str(proj.id)
    env['CODEX_LOGGER_SESSION_ID'] = str(sess.id)

    # Start the proxy server via uvicorn
    # Use 'uvicorn codex_logger.proxy:app' by default
    if shutil.which('uvicorn'):
        proxy_cmd = ['uvicorn', 'codex_logger.proxy:app', '--port', str(port)]
    else:
        proxy_cmd = [sys.executable, '-m', 'uvicorn', 'codex_logger.proxy:app', '--port', str(port)]
    proxy_proc = subprocess.Popen(proxy_cmd, env=env,
                                  stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL)
    # Give proxy time to start
    time.sleep(0.5)

    # Locate the real 'codex' CLI
    real_codex = os.getenv('ORIGINAL_CODEX_CLI') or shutil.which('codex')
    if not real_codex:
        click.echo('ERROR: cannot find real `codex` binary; set ORIGINAL_CODEX_CLI.', err=True)
        proxy_proc.terminate()
        sys.exit(1)

    # Build the command line for the real CLI, filtering out our custom opts
    extra_args = []
    skip_next = False
    for arg in ctx.args:
        if skip_next:
            skip_next = False
            continue
        if arg in ('--project','-p','--session','-s','--port','-P'):
            skip_next = True
        else:
            extra_args.append(arg)
    # Prepend the real codex
    cmd = [real_codex] + extra_args

    # Point OpenAI clients to our proxy
    env['OPENAI_API_BASE'] = f'http://127.0.0.1:{port}/v1'

    # Run the real codex CLI
    result = subprocess.run(cmd, env=env)

    # Teardown
    proxy_proc.terminate()
    sys.exit(result.returncode)

if __name__ == '__main__':
    main()