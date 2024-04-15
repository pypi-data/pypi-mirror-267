from setuptools import setup, find_packages

setup(
    name='langchain-tools',
    version='0.1.5',
    author='Langchain Tools Team',
    author_email='cheny@cheny.com',
    description='Simplifying, enhancing, and extending the LangChain library functionality',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MartinChen1973/langchain-tools',
    package_dir={'': 'src'},  # Treats 'src' as the root package directory
    packages=find_packages(where='src'),  # Automatically finds all packages in 'src'
    install_requires=[
        'langchain',  # Main functionality
        'langchain-community',  # Additional community features
        'langchain-openai',  # OpenAI specific features
        # Include other dependencies as necessary
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
    keywords='language processing, AI, natural language understanding, LangChain, LLM',
    project_urls={
        'Bug Tracker': 'https://github.com/MartinChen1973/langchain-tools/issues',
        'Documentation': 'https://MartinChen1973.github.io/langchain-tools/',
        'Source Code': 'https://github.com/MartinChen1973/langchain-tools'
    }
)
