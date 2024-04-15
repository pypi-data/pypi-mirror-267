# FaceCropThumb

FaceCropThumb is a Python package for generating thumbnails of detected faces in images. It utilizes the MTCNN (Multi-Task Cascaded Convolutional Neural Network) for accurate face detection and OpenCV for image processing.

All documentation is in the “docs” directory and online at https://facecrop-thumb.readthedocs.io/en/stable/. If you’re just getting started, here’s how we recommend you read the docs:

## Features

- Detect faces in images using the MTCNN model
- Crop detected faces with a configurable margin
- Generate square thumbnails of detected faces
- Option to resize the entire image if no face is detected or face detection is skipped
- Command-line utility for easy usage

## Quick Installation

You can install FaceCropThumb via pip:

```pip install facecropthumb```

## Quick Usage

```facecropthumb <image_path> [-d/--dir <output_directory>] [-m/--margin <margin_size>] [-F/--no-face] [-S/--skip-face] [-a/--all]```

- `<image_path>`: Path to the input image file.
- `-d/--dir <output_directory>`: Directory to store the output thumbnail. Default is the current directory.
- `-m/--margin <margin_size>`: Margin around the detected face. Default is 50 pixels.
- `-F/--no-face`: Skip face detection and resize the whole image if no face is detected.
- `-S/--skip-face`: Skip face detection and resize the whole image.
-  `-a/--all`: Process all images in the specified directory. If no directory is provided, it processes images in the current directory.
-  `-v/--version`: Show installed version.
-  `-h/--help`: Show help.

Example:

```facecropthumb input_image.jpg -d output_directory -m 30 -F```

This command will generate a thumbnail of the detected face in `input_image.jpg`, with a margin of 30 pixels, and if no face is detected, it will resize the whole image to a square of 74 x Y pixels (~approx).

## Development Documentation

DISCLAIMER: This documentation is for the contributers of FaceCropThumb, not for general package users.

Firstly install dev dependencies from `requirements.txt` file

### Usage

To run and test the package, use `python -m facecrop-thumb <args>`

### Build Docs

You can see the production build docs in `docs/build/index.html`

Update the documentation at any cost after any change in feature

Run this to watch the `docs/` folder while you're making documentation changes

`watchmedo shell-command --patterns="*.rst;conf.py;_templates/*" --recursive --command='sphinx-build -b html docs docs/_build' docs`

### Release

After a successful change in the package, it's time to publish it officially.

 - Update the version in `facecrop_thumb/version.py`

 - Create a new release on [release page](https://github.com/mr-vaibh/facecrop-thumb/releases/new). (This will automatically trigger GitHub actions to release a new version on PYPI)

That's it, the newer version will be available to everyone.

But if you want to publish a version by yourself, you can use following command:

 - `python setup.py sdist`

 - ` twine upload dist/*`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
