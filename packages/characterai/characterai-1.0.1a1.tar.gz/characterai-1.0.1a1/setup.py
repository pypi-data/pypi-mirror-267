from setuptools import setup, find_packages

with open('requirements.txt', encoding='utf-8') as r:
    requires = [i.strip() for i in r]

with open('README.rst', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='characterai',
    version='1.0.1-a1',
    description='An unofficial API for Character AI for Python',
    keywords="characterai ai wrapper api library",
    long_description=readme,
    long_description_content_type='text/x-rst',
    url='https://github.com/kramcat/characterai',
    author='kramcat',
    license='MIT',
    install_requires=requires,
    packages=find_packages(exclude=['docs*', 'examples*']),
    project_urls={
        'Community': 'https://discord.gg/ZHJe3tXQkf',
        'Source': 'https://github.com/kramcat/characterai',
        'Documentation': 'https://docs.kram.cat',
    },
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],
)
