from setuptools import setup, find_packages

setup(
    name='psd2fabric',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        "psd_tools==1.9.28"
    ],
    entry_points={
        'console_scripts': [
            'psd2fabric = cli:main'
        ]
    }
)
