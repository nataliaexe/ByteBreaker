from setuptools import setup, find_packages

setup(
    name="bytebreaker",
    version="1.0.0",
    description="Advanced Pentest Framework with 5 Integrated Modules",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "aiohttp>=3.9.0",
        "scapy>=2.5.0",
        "cryptography>=41.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "scikit-learn>=1.3.0",
        "pandas>=2.0.0",
        "rich>=13.0.0",
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "bytebreaker=cli.main:main",
        ],
    },
    python_requires=">=3.8",
)
