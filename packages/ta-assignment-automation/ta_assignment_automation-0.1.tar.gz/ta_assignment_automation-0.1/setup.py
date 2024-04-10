from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='ta_assignment_automation',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas"
    ],
    description='Assign TAs to Classes using a global optimization algorithm',
    long_description_content_type="text/markdown",
    long_description=long_description,
    license="MIT",
    author='Ashwin Pillai',
    author_email='ashwinkumarpillai1729@gmail.com',
    url='https://github.com/AshwinkumarPillai/TA_assignment_automation',
)
