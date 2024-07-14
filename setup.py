from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fb_ad_budget_adjuster",
    version="0.1.0",
    author="Ankur Shrivastava",
    author_email="ankshva.yt@gmail.com",
    description="A package to adjust Facebook ad budgets automatically based on specified day of a week and time",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ankshvayt/fb_ad_budget_adjuster",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "facebook-business",
        "pytz",
    ],
)