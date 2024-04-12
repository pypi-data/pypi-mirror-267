from setuptools import setup, find_packages

setup(
    name="polytrend",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "matplotlib==3.8.3",
        "numpy==1.21.5",
        "pandas==2.2.2",
        "scikit_learn==1.4.1.post1",
    ],
)
