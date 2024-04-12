from setuptools import setup, find_packages

setup(
    name='arthoperations',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'arithmetic_operations = arithmetic_operations.__main__:main'
        ]
    },
    install_requires=[],
    author='Your Name',
    author_email='your@email.com',
    description='A Python package for arithmetic operations',
    license='MIT',
    keywords='arithmetic operations',
    url='https://github.com/yourusername/arithmetic_operations'
)
