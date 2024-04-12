from setuptools import setup, find_packages

setup(
    name='QuartzFramework',
    version='0.2',
    py_modules=['QuartzFramework'],
    entry_points={
        'console_scripts': [
            'QuartzFramework = QuartzFramework:main',
        ],
    },
    author='QuartzSec',
    author_email='ydku@quartz.ai',
    description='An Exploitation Framework',
    install_requires=[],
)
