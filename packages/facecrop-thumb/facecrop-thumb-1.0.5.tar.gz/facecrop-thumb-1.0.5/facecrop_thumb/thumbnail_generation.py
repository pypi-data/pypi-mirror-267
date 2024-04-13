# thumbnail_generation.py
import cv2
import os
from .face_detection import detect_face
from .image_processing import crop_face_thumbnail

def generate_face_thumbnail(input_image_path, output_thumbnail_path, margin=50, detect_face_flag=True):
    image = cv2.imread(input_image_path)
    filename_without_extension = os.path.splitext(os.path.basename(input_image_path))[0]
    output_filename_prefix = f"th-{filename_without_extension}"
    
    if not detect_face_flag:
        aspect_ratio = image.shape[1] / image.shape[0]
        if aspect_ratio > 1:
            new_width = 74
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = 74
            new_width = int(new_height * aspect_ratio)
        image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        output_filename = f"{output_filename_prefix}.jpg"
        output_thumbnail_path = os.path.join(output_thumbnail_path, output_filename)
        cv2.imwrite(output_thumbnail_path, image)
        print(f"Image resized to {new_width}x{new_height} and saved as: {output_thumbnail_path}")
        return
    
    face_coords = detect_face(image)
    
    if face_coords is not None:
        face_thumbnail = crop_face_thumbnail(image, face_coords, margin=margin)
        output_filename = f"{output_filename_prefix}.jpg"
        os.makedirs(output_thumbnail_path, exist_ok=True)
        output_thumbnail_path = os.path.join(output_thumbnail_path, output_filename)
        cv2.imwrite(output_thumbnail_path, face_thumbnail)
        print(f"Face thumbnail saved as: {output_thumbnail_path}")
    else:
        if detect_face_flag:
            aspect_ratio = image.shape[1] / image.shape[0]
            if aspect_ratio > 1:
                new_width = 74
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = 74
                new_width = int(new_height * aspect_ratio)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            output_filename = f"{output_filename_prefix}.jpg"
            output_thumbnail_path = os.path.join(output_thumbnail_path, output_filename)
            cv2.imwrite(output_thumbnail_path, image)
            print(f"Image resized to {new_width}x{new_height} and saved as: {output_thumbnail_path}")
        else:
            print("No face detected in the image.")
