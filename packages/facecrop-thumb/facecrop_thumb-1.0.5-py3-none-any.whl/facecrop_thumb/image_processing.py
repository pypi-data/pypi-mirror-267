# image_processing.py
import cv2

def crop_face_thumbnail(image, face_coords, margin=50, target_size=(74, 74)):
    x, y, w, h = face_coords
    x -= margin
    y -= margin
    w += 2 * margin
    h += 2 * margin
    x = max(0, x)
    y = max(0, y)
    w = min(w, image.shape[1])
    h = min(h, image.shape[0])
    aspect_ratio = w / h
    if w > h:
        thumbnail_height = int(target_size[1])
        thumbnail_width = int(thumbnail_height * aspect_ratio)
    else:
        thumbnail_width = int(target_size[0])
        thumbnail_height = int(thumbnail_width / aspect_ratio)
    face_with_margin = image[y:y+h, x:x+w]
    face_thumbnail = cv2.resize(face_with_margin, (thumbnail_width, thumbnail_height), interpolation=cv2.INTER_AREA)
    return face_thumbnail
