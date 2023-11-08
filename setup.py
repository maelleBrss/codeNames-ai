from setuptools import setup, find_packages

setup(
    name='codeNames-ai',
    version='1.0.0',
    use_scm_version=True,
    description='CodeNames',
    author='MB',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'typing'
    ]
)