#!/usr/bin/env python3
"""
Setup configuration for ULTRATHINK PyPI package
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

# Read requirements
def read_requirements(filename):
    req_file = Path(__file__).parent / filename
    if req_file.exists():
        with open(req_file) as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

setup(
    name="ultrathink",
    version="1.0.0",
    author="ULTRATHINK Team",
    author_email="support@ultrathink.ai",
    description="Advanced orchestration framework for Claude API with 8-layer guardrails",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ultrathink/ultrathink",
    project_urls={
        "Documentation": "https://ultrathink.readthedocs.io",
        "Source": "https://github.com/ultrathink/ultrathink",
        "Tracker": "https://github.com/ultrathink/ultrathink/issues",
    },
    packages=find_packages(exclude=["tests*", "archive*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
        "cache": ["diskcache>=5.6.0"],
        "secrets": ["keyring>=24.0.0"],
        "logging": ["structlog>=24.0.0"],
        "metrics": ["prometheus-client>=0.19.0"],
    },
    entry_points={
        "console_scripts": [
            "ultrathink=ultrathink:main",
            "cpp=ultrathink:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="ai llm claude anthropic guardrails orchestration",
)
