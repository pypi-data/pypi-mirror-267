# main.py
import argparse
import os
from .version import __version__

def main():
    parser = argparse.ArgumentParser(description="Generate a thumbnail of the detected face in an image.")
    parser.add_argument("image_path", help="Path to the input image file")
    parser.add_argument("-d", "--dir", help="Directory to store the output thumbnail", default="")
    parser.add_argument("-m", "--margin", help="Margin around the detected face (default: 50)", type=int, default=50)
    parser.add_argument("-F", "--no-face", help="Skip face detection and resize the whole image if no face is detected", action="store_true")
    parser.add_argument("-S", "--skip-face", help="Skip face detection and resize the whole image", action="store_true")
    parser.add_argument("-v", "--version", action="version", version=f"facecrop-thumb {__version__}")
    parser.add_argument("-a", "--all", help="Process all images in the specified directory", action="store_true")
    args = parser.parse_args()

    from .thumbnail_generation import generate_face_thumbnail

    output_directory = os.path.join(os.getcwd(), args.dir)
    if args.all:
        input_directory = args.image_path or "."
        for file_name in os.listdir(input_directory):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(input_directory, file_name)
                generate_face_thumbnail(file_path, output_directory, margin=args.margin, detect_face_flag=not args.skip_face)
    else:
        if not args.image_path:
            parser.error("You must provide an image path or use the -a/--all option to process all images in a directory.")
        generate_face_thumbnail(args.image_path, output_directory, margin=args.margin, detect_face_flag=not args.skip_face)

if __name__ == "__main__":
    main()
