from setuptools import setup, find_packages

setup(
    name="l2m2",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "cohere>=5.2.5",
        "openai>=1.17.0",
        "anthropic>=0.25.1",
        "groq>=0.5.0",
    ],
)
