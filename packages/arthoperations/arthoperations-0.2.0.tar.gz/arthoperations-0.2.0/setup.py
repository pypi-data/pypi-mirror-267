from setuptools import setup, find_packages

setup(
    name='arthoperations',
    version='0.2.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'arithmetic_operations = arithmetic_operations.__main__:main'
        ]
    },
    install_requires=[],
    author='stealth22',
    author_email='your@email.com',
    description='A Python package for arithmetic operations',
    license='MIT',
    keywords='arithmetic operations'
)
