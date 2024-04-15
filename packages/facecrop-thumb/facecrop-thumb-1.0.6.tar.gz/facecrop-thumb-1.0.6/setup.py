from setuptools import setup, find_packages
from facecrop_thumb.version import __version__

setup(
    name='facecrop-thumb',
    version=__version__,
    description='Generate thumbnails of detected faces in images using Python.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url='https://facecrop-thumb.readthedocs.io/en/stable/',
    author='Vaibhav Shukla',
    author_email='shuklavaibhav336@example.com',
    license='MIT',
    project_urls={
        'Documentation': 'https://facecrop-thumb.readthedocs.io/en/stable/',
        'Funding': 'https://www.buymeacoffee.com/mrvaibh',
        'Release Notes': 'https://github.com/mr-vaibh/facecrop-thumb/releases',
        'Source': 'https://github.com/mr-vaibh/facecrop-thumb',
        'Tracker': 'https://github.com/mr-vaibh/facecrop-thumb/issues',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='face detection thumbnail image-processing',
    packages=find_packages(),
    install_requires=[
        'mtcnn>=0.1.1',
        'opencv-python>=4.9.0.80',
    ],
    entry_points={
        'console_scripts': [
            'facecrop-thumb=facecrop_thumb.main:main',
        ],
    },
)
