# face_detection.py
from mtcnn import MTCNN

def detect_face(image):
    detector = MTCNN()
    faces = detector.detect_faces(image)
    if faces:
        faces.sort(key=lambda x: x['confidence'], reverse=True)
        return faces[0]['box']
    else:
        return None
