from setuptools import setup, find_packages
setup(
    name="Myexperiment",
    version="1.0.1",
    packages=find_packages(),
    package_data={
        "Mycontent": [r"Mycontent/My.py", r"Mycontent/*"]
    },
    long_description=open("README.txt", encoding="utf-8").read(),
    long_description_content_type="text/markdown"
)