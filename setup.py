from setuptools import setup, find_packages

setup(
    name="realtor-buddy",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "langchain>=0.1.0",
        "langchain-community>=0.0.10",
        "langchain-openai>=0.0.5",
        "pymysql>=1.1.0",
        "sqlalchemy>=2.0.25",
        "python-dotenv>=1.0.0",
        "click>=8.1.7",
        "rich>=13.7.0",
        "tabulate>=0.9.0",
        "pandas>=2.1.4",
        "numpy>=1.26.2",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "realtor-buddy=realtor_buddy.cli.main:main",
        ],
    },
    python_requires=">=3.8",
    author="Nuno Antunes",
    description="Croatian Real Estate Property Search using LangChain",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)