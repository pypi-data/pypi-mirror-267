from setuptools import setup, find_packages

setup(
    name='IbbUploader',
    version='0.0.1',
    author='dlrodev92',
    author_email='dlrdev92@gmail.com',
    description='A Python library for uploading images to ImgBB via their API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dlrodev92/ibb_uploader_python',
    packages=find_packages(),
    install_requires=[
        'requests', 
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/dlrodev92/ibb_uploader_python/issues',
        'Source': 'https://github.com/dlrodev92/ibb_uploader_python',
    },
)