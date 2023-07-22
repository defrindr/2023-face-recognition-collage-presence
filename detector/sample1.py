import cv2
import os

def detect_faces_from_camera_and_save_on_enter(face_cascade_path, output_folder):
    # Load the pre-trained Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(face_cascade_path)

    # Initialize camera capture object
    video_capture = cv2.VideoCapture(0)  # 0 means the default camera (you can change it to another index if you have multiple cameras)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_count = 0

    while True:
        # Wait for the "Enter" key to be pressed
        input_key = cv2.waitKey(0) & 0xFF
        if input_key == 13:  # 13 is the ASCII code for "Enter" key
            break

    while True:
        # Read a frame from the camera
        ret, frame = video_capture.read()

        if not ret:
            print("Error: Could not capture frame.")
            break

        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Perform face detection on the grayscale frame
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Save frames with detected faces to the output folder
        for (x, y, w, h) in faces:
            face_roi = frame[y:y + h, x:x + w]
            output_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(output_path, face_roi)
            frame_count += 1

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the frame with detected faces
        cv2.imshow('Face Detection', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release camera capture object
    video_capture.release()

    # Destroy all OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    face_cascade_path = "recognition/haarcascade_frontalface_default.xml"
    output_folder = "recognition/training/dataset/defri/"

    detect_faces_from_camera_and_save_on_enter(face_cascade_path, output_folder)