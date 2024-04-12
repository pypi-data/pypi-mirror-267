from setuptools import setup, find_packages

setup(
    name='daraz-scrapper',
    version='0.1.1',
    author='Anas Khan',
    author_email='anas985822@gmail.com',
    description='A scrapper for Daraz platform',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Anas-art-source/daraz_scrapper',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'numpy',
        'bs4',
        'requests',
        'tqdm',
        'lxml'  # Assuming you are using lxml as parser
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)