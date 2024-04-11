from setuptools import setup, find_packages

setup(
    name='daraz_scrapper',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
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
    entry_points={
        'console_scripts': [
            # If you have a script meant to be executed directly, you can list it here.
            # 'daraz-scrapper = daraz_scrapper.scrapper:main_function',
        ],
    },
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