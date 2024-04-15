import shutil
import os
import glob
from setuptools import setup, find_packages
from subprocess import call

# Function to clean up build directories
def remove_build_dirs():
    directories = ['dist', 'build', '*.egg-info']
    for directory in directories:
        if os.path.isdir(directory):  # Checks if it's a directory
            shutil.rmtree(directory)
        elif glob.glob(directory):  # This is for wildcard like '*.egg-info'
            for dir in glob.glob(directory):
                shutil.rmtree(dir)

# Setup configuration
def setup_package():
    setup(
        name='langchain-tools',
        version='0.1.6',
        author='Langchain Tools Team',
        author_email='cheny@cheny.com',
        description='Simplifying, enhancing, and extending the LangChain library functionality',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        url='https://github.com/MartinChen1973/langchain-tools',
        packages=find_packages(),
        install_requires=[
            'langchain', 
            'langchain-community', 
            'langchain-openai'
        ],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10'
        ],
        python_requires='>=3.7',
        keywords='language processing, AI, natural language understanding, LangChain, LLM'
    )

# Main execution logic
if __name__ == "__main__":
    remove_build_dirs()  # Clean old build files
    setup_package()  # Setup package

    # Optional: Automatically upload to PyPI
    # call(['twine', 'upload', 'dist/*'])
