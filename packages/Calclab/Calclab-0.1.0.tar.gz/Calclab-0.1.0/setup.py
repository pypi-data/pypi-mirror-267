from setuptools import setup, find_packages

setup(
    name='Calclab',
    version='0.1.0',
    author='Aaroh Charne',
    author_email='aaroh.charne@gmail.com',
    description='Description of your library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/aa425/Calclab.git',
    packages=find_packages(),
    python_requires='>=3.7',  # Specify the minimum Python version required
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
