from setuptools import setup, find_packages

setup(
    name='Terminalgemini',  # Name of your package
    version='1.0.1',  # Version of your package
    author='ticklecatisback',  # Your name or your organization's name
    author_email='alesaholder@gmail.com',  # Your email or your organization's contact email
    description='AI chat assistant in your terminal powered by Gemini models.',  # Short description of your package
    long_description=open('README.md').read(),  # Long description read from the README.md file
    long_description_content_type='text/markdown',  # Type of the long description, here markdown
    url='https://github.com/yourusername/TerminalGPT-main',  # Link to your project's GitHub repo
    packages=find_packages(),  # Automatically find all packages and subpackages
    include_package_data=True,  # Include everything in source control
    install_requires=[
        'google-generativeai',
        'tiktoken',
        'colorama',
        'cryptography',
        'click',
        'prompt-toolkit',
        'yaspin',
        'rich',
        'isort',
        'pytest',
        'pylint'
    ],  # List of packages required to run your project, installed by pip install your-package
    entry_points={
        'console_scripts': [
            'terminalgpt=terminalgpt.main:cli'  # Provide a command line script
        ],
    },
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.10',  # Minimum version requirement of Python
)
