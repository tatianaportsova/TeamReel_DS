"""
[?? To add description ??]
"""


# ----------------------------------------------------------------------------
# Import libraries/modules/functions we will use:

# External (third-party) libraries:
import cv2
import numpy as np
import dlib

# video_filename = 'ALPACAVID-r7tjBJgdj.mp4'


# ----------------------------------------------------------------------------
def get_facial_alignment(video_filename:str):
    vid = cv2.VideoCapture(video_filename)

    if not cap.isOpened():
        print(f"Error: Cannot open video file {video_filename}.")
        exit()

    # Load pre-trained dlib facial landmarks detector from pre-trained model:
    detector = dlib.get_frontal_face_detector()

    # Initialize facial landmarks predictor using the above model:
    predictor = dlib.shape_predictor("./models/dlib_shape_predictor_68_face_landmarks.dat")

    # Get video frames:
    total_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Frame width x height: {frame_width} x {frame_height}")

    # Analyze each frame in the video: get facial landmarks -> determine facial
    # alignment:
    while True:
        returned, frame = vid.read()

        if not returned:
            print("Video stream has ended (cannot receive next frame). Exiting.")
            break

        # # Resize the frame to a smaller size:
        # frame = cv2.resize(frame,
        #                   None,
        #                   fx = 0.80,
        #                   fy = 0.80,
        #                   interpolation = cv2.INTER_AREA)

        # Convert frame to grayscale for optimal processing:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            # The face landmarks code begins from here
            x1 = face.left()
            y1 = face.top()
            w = face.right()
            h = face.bottom()
            # Then we can also do
            # cv2.rectangle function (frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.rectangle(frame, (x1, y1), (w, h), (0, 255, 0), 3)
            cv2.rectangle(frame,
                          (int(0.25*frame_width), int(0.15*frame_height)),
                          (int(frame_width - 0.25*frame_width), int(frame_height - 0.15*frame_height)),
                          (0, 0, 255),
                          3)

            landmarks = predictor(gray, face)
            # We are then accesing the landmark points
            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                cv2.circle(frame, (x, y), 2, (255, 255, 0), -1)

        cv2.imshow("Frame", frame)

        # # Use the 'esc' key to terminate:
        # key = cv2.waitKey(1)
        # if key == 27:
        #     break # press esc the frame is destroyed

        # Use the "q" key as the quit command:
        # waitKey(0 or <= 0): waits for a key event infinitely
        # waitKey(x:int): waits for a key event for x milliseconds (when x > 0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object & close OpenCV windows:
    vid.release()
    cv2.destroyAllWindows()
