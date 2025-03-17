from setuptools import setup, find_packages

setup(
    name="gofannon",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-cors",
        "requests",
        "python-dotenv",
        "lxml",
        "beautifulsoup4",
        "google-api-python-client",
        "openai"
    ],
)
