from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="l2m2",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "cohere>=5.2.5",
        "openai>=1.17.0",
        "anthropic>=0.25.1",
        "groq>=0.5.0",
    ],
    long_description=readme,
    long_description_content_type="text/markdown",
)
