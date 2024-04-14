from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r') as f:
        return f.read()
    

setup(
    name='area_of_a_shape',
    version='0.0.2',
    author='Akim',
    author_email='akimserverov75@gmail.com',
    description='A library that can calculate the area of a circle by radius and a triangle on three sides.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://vk.com/mrrobot1234',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='triangle rectangle',
    project_urls={
        'Profile author': 'https://vk.com/mrrobot1234'
    },
    python_requires='>=3.6'
)
