from setuptools import setup

installation_requirements = [

]

setup(
    name="underhill",
    description="You draw far too much attention to yourself, Mr. Underhill.",
    version="0.1",
    url="https://github.com/vagabond-systems/underhill",
    author="(~)",
    package_dir={"": "packages"},
    packages=["underhill"],
    install_requires=installation_requirements
)
