from setuptools import setup, find_packages

setup(
    name='QuartzAI',
    version='0.1',
    py_modules=['QuartzAI'],
    entry_points={
        'console_scripts': [
            'QuartzAI = QuartzAI:main',
        ],
    },
    author='pwntrackdev',
    author_email='pwntrackdev@gmail.com',
    description='An AI Coding Friend Package',
    install_requires=[],
)
