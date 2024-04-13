from setuptools import setup, find_packages

setup(
    name='git_root_to_syspath',
    version='0.1',
    packages=find_packages(),
    description='Inserts the nearest git repository root into sys.path.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ivo Marvan',
    author_email='ivo@marvan.cz',
    url='https://gitlab.com/ivo-marvan/git_root_to_syspath',
    install_requires=[
        # List your dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
