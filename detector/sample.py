import cv2
import os
import numpy as np

current_directory = os.getcwd()


def train_lbph_face_recognizer(data_dir, training_file, force=False):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    labels = []
    label_to_name = {}

    for label, name in enumerate(os.listdir(data_dir)):
        if name == '.DS_Store':
            continue
        label_to_name[label] = name
        person_dir = os.path.join(data_dir, name)
        for filename in os.listdir(person_dir):
            if filename == '.DS_Store':
                continue
            image_path = os.path.join(person_dir, filename)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            faces.append(image)
            labels.append(label)
            pass
        pass
    pass

    if (force or os.path.exists(training_file) == False):
        face_recognizer.train(faces, np.array(labels))
        face_recognizer.save(training_file)
    else:
        face_recognizer.read(training_file)
    pass
    # Save the training result to a YAML file

    return face_recognizer, label_to_name


def is_student_present(face_recognizer, student_names, test_image_path, face_cascade_path, confidence_threshold=70):
    full_path = f"{current_directory}/{test_image_path}"
    test_image = cv2.imread(full_path)

    gray_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(face_cascade_path)

    faces = face_cascade.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=7, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face_roi = gray_image[y:y + h, x:x + w]

        label, confidence = face_recognizer.predict(face_roi)

        if confidence > confidence_threshold:
            student_name = student_names[label]
            print(f"{student_name} is present. (Confidence: {confidence:.2f})")
        else:
            print("Unknown person (not a student) detected.")


if __name__ == "__main__":
    training_data_dir = "recognition/training/dataset"
    test_image_path = "recognition/training/dani.jpg"
    face_cascade_path = "recognition/haarcascade_frontalface_default.xml"

    face_recognizer, label_to_name = train_lbph_face_recognizer(
        training_data_dir, "trained_face_recognizer.yml")
    student_names = [name for _, name in sorted(label_to_name.items())]

    is_student_present(face_recognizer, label_to_name,
                       test_image_path, face_cascade_path)
