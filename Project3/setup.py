from setuptools import find_packages
from setuptools import setup

def get_requirements(path  : str) -> list:
    """ Get requirements from requirements.txt file
    Args:
        path (str): path to requirements.txt file
    Returns:
        list: list of requirements"""
    with open(path) as f:
        requirements = f.read().splitlines()
    requirements.pop(-1) # remove last element which is the path to the requirements.txt file
    return requirements


NAME : str = "Environment eco saver application"
VERSION : float = '0.0.1'
DESCRIPTION : str = "Energy saving and anomaly detection application for industries"
AUTHOR : str = "Archisman Chakraborti"
AUTHOR_EMAIL : str = "archismanninja@gmail.com"


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    install_requires = get_requirements("requirements_proj3.txt"),
)