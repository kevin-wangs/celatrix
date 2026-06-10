from setuptools import setup, find_packages

setup(
    name="celatrix",
    version="0.1.0",
    description="Celatrix — part of the Optrix ecosystem by Apex Ridge Technologies, Inc.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Kevin Wangs",
    author_email="kevin@apexridgetech.com",
    url="https://github.com/kevin-wangs/celatrix",
    project_urls={
        "Company": "https://apexridgetech.com",
        "Documentation": "https://github.com/kevin-wangs/celatrix/tree/main/docs",
        "Issues": "https://github.com/kevin-wangs/celatrix/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=["numpy>=1.24"],
    extras_require={
        "dev": ["pytest>=7", "pytest-cov", "ruff"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
