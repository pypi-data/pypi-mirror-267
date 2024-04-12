from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'A Python package to access Minecraft data'
LONG_DESCRIPTION = (
    'A Python package to access Minecraft data from the ' +
    'PrismarineJs/minecraft-data repository'
)

setup(
    name="minecraft_data_py",
    version=VERSION,
    author="ProfessorQu",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['minecraft', 'data'],
)
