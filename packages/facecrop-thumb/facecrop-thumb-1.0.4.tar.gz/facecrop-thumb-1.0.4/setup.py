from setuptools import setup, find_packages

setup(
    name='facecrop-thumb',
    version='1.0.4',
    description='Generate thumbnails of detected faces in images using Python.',
    long_description='FaceCropThumb is a Python package for generating thumbnails of detected faces in images. It utilizes the MTCNN (Multi-Task Cascaded Convolutional Neural Network) for accurate face detection and OpenCV for image processing.',
    url='https://github.com/mr-vaibh/facecrop-thumb',
    author='Vaibhav Shukla',
    author_email='shuklavaibhav336@example.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
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
