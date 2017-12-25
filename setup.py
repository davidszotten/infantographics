from setuptools import find_packages, setup


setup(
    name='infantographics',
    version='0.1',
    description='utilities for generating graphs with data about our baby',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'jinja2',
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'infantographics=infantographics.cli:main',
        ],
    },
)
