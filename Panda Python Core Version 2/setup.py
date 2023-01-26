from setuptools import setup, find_packages

setup(
    name='PandaPythonCore',
    version='0.0.1',
    author='Joshua Filer',
    author_email='joshuafiler.jf@gmail.com',
    url='https://github.com/Closeplanet2/PandaPythonCore',
    description='Python helpers for my project',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4==4.11.1',
        'Pillow== 9.2.0',
    ],
)