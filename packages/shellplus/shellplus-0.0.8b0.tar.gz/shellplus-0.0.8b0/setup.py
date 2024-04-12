from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='shellplus',
    version='0.0.8b0',
    packages=find_packages(),
    install_requires=[
        'rich',  # Add any other dependencies here
    ],
    setup_requires=['wheel'],  # Add 'wheel' to setup_requires
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Programming Language :: Python :: 3.12',
    ],
    # Add the long_description field
    long_description=long_description,
    long_description_content_type='text/markdown',  # Assuming it's a Markdown file
    license='Unlicense',
)
