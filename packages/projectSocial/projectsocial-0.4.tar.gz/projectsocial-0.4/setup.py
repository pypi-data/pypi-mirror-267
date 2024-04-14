from setuptools import setup, find_packages

setup(
    name='projectSocial',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    entry_points={
        'console_scripts': [
            'projectSocial = projectSocial.scraper:main'
        ]
    }
)
