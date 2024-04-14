from setuptools import setup, find_packages
setup(
    name="Myexperiment",
    version="1.0.0",
    packages=find_packages(),
    package_data={
        "Mycontent": [r"C:\Users\吴秋宏\Desktop\实验项目\Mycontent\My.py", r"C:\Users\吴秋宏\Desktop\实验项目\Mycontent\*"]
    },
    long_description=open("README.txt", encoding="utf-8").read(),
    long_description_content_type="text/markdown"
)