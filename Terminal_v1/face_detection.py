import cv2
import mediapipe as mp

class FaceDetector:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection()
    
    def detect_faces(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(image_rgb)
        face_list = []
        if results.detections:
            for detection in results.detections:
                bbox_cords = self.mp_drawing._normalized_to_pixel_coordinates(
                    detection.location_data.relative_bounding_box, 
                    image.shape[1], 
                    image.shape[0]
                )
                face_list.append(bbox_cords)
        return face_list