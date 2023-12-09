import cv2
import os
import numpy as np
from App.Core.config import Config

current_directory = os.getcwd() + "/facerec"


def train_lbph_face_recognizer(data_dir, training_file, force=False):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    labels = []
    label_to_name = {}
    print(os.listdir(f"{current_directory}/{data_dir}"))
    for label, name in enumerate(os.listdir(f"{current_directory}/{data_dir}")):
        if name == '.DS_Store':
            continue
        label_to_name[label] = name
        person_dir = os.path.join(data_dir, name)
        for filename in os.listdir(f"{current_directory}/{person_dir}"):
            if filename == '.DS_Store':
                continue
            image_path = os.path.join(person_dir, filename)
            image = cv2.imread(
                f"{current_directory}/{image_path}", cv2.IMREAD_GRAYSCALE)
            faces.append(image)
            labels.append(label)
            pass
        pass
    pass

    if (force or os.path.exists(f"{current_directory}/{training_file}") == False):
        face_recognizer.train(faces, np.array(labels))
        face_recognizer.save(f"{current_directory}/{training_file}")
    else:
        face_recognizer.read(f"{current_directory}/{training_file}")
    pass

    return face_recognizer, label_to_name


def training_data(temp_video_path, name):
    base_folder = "training/faces"
    folder = f"training/faces/{name}"
    training_file = "trained_face_recognizer.yml"
    # Process the video and save face images with labels
    video_capture = cv2.VideoCapture(temp_video_path)
    face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')

    if os.path.exists(f"{current_directory}/{training_file}") == True:
        confidence, user_id = predict_face(temp_video_path)
        print(confidence, user_id)

        config= Config()
        if confidence > config.MINIMUM_CONFIDENCE_TRAINING:
            if user_id == name:
                print("Deteksi ulang")
            elif user_id == 0:
                print("Deteksi ulang")
            else:
                return False
        pass

    face_counter = 0
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Convert frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(
            gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_image = frame[y:y+h, x:x+w]

            # Save face image with label to 'faces' directory
            cv2.imwrite(
                f'{current_directory}/{folder}/{face_counter}.jpg', face_image)
            face_counter += 1

    video_capture.release()
    print("uwuwu")
    train_lbph_face_recognizer(
        base_folder,
        training_file,
        True
    )

    return True


def predict_face(video):
    folder = "training/faces"
    face_recognizer, labels = train_lbph_face_recognizer(
        folder,
        "trained_face_recognizer.yml"
    )

    # Process the video and save face images with labels
    video_capture = cv2.VideoCapture(video)
    face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')

    highest_confidence = 0
    highest_confidence_id = ''
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Convert frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(
            gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_roi = gray_frame[y:y + h, x:x + w]
            id, confidence = face_recognizer.predict(face_roi)
            confidence = round(100 - confidence)

            if confidence > highest_confidence:
                highest_confidence = confidence
                highest_confidence_id = labels.get(id, 0)

    video_capture.release()

    return highest_confidence, highest_confidence_id

# if __name__ == "__main__":
#     training_data_dir = "recognition/training/dataset"
#     test_image_path = "recognition/training/dani.jpg"
#     face_cascade_path = "recognition/haarcascade_frontalface_default.xml"

#     face_recognizer, label_to_name = train_lbph_face_recognizer(
#         training_data_dir, "trained_face_recognizer.yml")
#     student_names = [name for _, name in sorted(label_to_name.items())]

#     is_student_present(face_recognizer, label_to_name,
#                        test_image_path, face_cascade_path)
