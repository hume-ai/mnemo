from setuptools import setup, find_packages

setup(
    name='codex-logger',
    version='0.1.0',
    author='Your Name',
    description='CLI and HTTP proxy to log OpenAI/Codex interactions by project and session',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'python-dotenv',
        'click',
        'gitpython',
        'httpx'
    ],
    entry_points={
        'console_scripts': [
            'codex=codex_logger.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: FastAPI',
        'License :: OSI Approved :: MIT License',
    ],
)