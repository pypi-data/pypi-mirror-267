from setuptools import setup, find_packages

setup(
    name="packaging_demo",
    version="0.0.1",
    author="haddad skander",
    author_email="skander.haddad.perso@gmail.com",
    description="An application that informs you of the time in different locations and timezones",
    long_description="An application that informs you of the time in different locations and timezones",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["click", "pytz"],
    entry_points={"console_scripts": ["packaging_demo = packaging_demo.main:main"]},
)
