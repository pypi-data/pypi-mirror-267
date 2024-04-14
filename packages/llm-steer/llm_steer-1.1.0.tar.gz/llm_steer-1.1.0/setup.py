from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='llm_steer',
    version='1.1.0',
    description='Steer LLM outputs towards a certain topic/subject and enhance response capabilities using activation engineering by adding steer vectors',
    author='Mihai Chirculescu',
    author_email='apropodemine@gmail.com',
    py_modules=['llm_steer'],
    url="https://github.com/Mihaiii/llm_steer",
    install_requires=[
        'transformers'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)