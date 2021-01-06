import face_recognition
import cv2
import numpy as np
import os
import sys
import subprocess
import argparse
from utils import col, removeExtension


def parse_args():
    parser = argparse.ArgumentParser(
        description="Highlight recognized faces in videos")
    parser.add_argument("files", metavar="filepath", type=str,
                        nargs="+", help="file path of videos to process")
    parser.add_argument("-a", "--accuracy", dest="accuracy", type=float,
                        help="the factor the video will get scaled down by before processing (faster; noninversive)")
    arguments = vars(parser.parse_args())
    return arguments


def main(options):
    if options.get("accuracy", None) != None:
        ACCURACY = options["accuracy"]
    else:
        ACCURACY = 0.25

    print("using accuracy of " + str(ACCURACY))

    for video in options.get("files", []):
        FILE_PATH = options.get("files", [])[options.get("files").index(video)]
        FILE_NAME = removeExtension(FILE_PATH).replace("videos/", "")
        NEW_FILE_PATH = "videos/" + FILE_NAME + "-rec.mp4"

        # extracting audio as mp3
        os.system("ffmpeg -i " + FILE_PATH + " -loglevel warning temp/" +
                  FILE_NAME + ".mp3")

        # getting framerate of video
        cmd = ['ffprobe', '-v', '0', '-of', 'csv=p=0', '-select_streams',
               'v:0', '-show_entries', 'stream=r_frame_rate', FILE_PATH]
        FRAME_RATE = subprocess.Popen(
            cmd, stdout=subprocess.PIPE).communicate()[0]
        FRAME_RATE = str(FRAME_RATE).replace("b", "").replace(
            "\n", "").replace("\\n", "").replace("'", "")
        frame_rate_divisors = FRAME_RATE.split("/")
        FRAME_RATE = float(
            int(frame_rate_divisors[0]) / int(frame_rate_divisors[1]))

        video_capture = cv2.VideoCapture(FILE_PATH)

        known_face_encodings = []
        known_face_names = []

        for i in os.listdir("faces"):
            if i == ".DS_Store":
                continue
            f = face_recognition.load_image_file("faces/" + str(i))
            try:
                encoding = face_recognition.face_encodings(f)[0]
            except IndexError:
                print("no encoding available for " + str(i))
                continue
            known_face_encodings.append(encoding)
            known_face_names.append(str(i))

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        cc = cv2.VideoWriter_fourcc(*"MP4V")
        writer = cv2.VideoWriter(NEW_FILE_PATH, cc, FRAME_RATE, (1920, 1080))

        try:
            while True:
                # Grab a single frame of video
                ret, frame = video_capture.read()

                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(
                    frame, (0, 0), fx=ACCURACY, fy=ACCURACY)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Only process every other frame of video to save time
                if process_this_frame:
                    # Find all the faces and face encodings in the current frame of video
                    face_locations = face_recognition.face_locations(
                        rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(
                        rgb_small_frame, face_locations)

                    face_names = []
                    for face_encoding in face_encodings:
                        # See if the face is a match for the known face(s)
                        matches = face_recognition.compare_faces(
                            known_face_encodings, face_encoding)
                        name = "Unknown"

                        # # If a match was found in known_face_encodings, just use the first one.
                        # if True in matches:
                        #     first_match_index = matches.index(True)
                        #     name = known_face_names[first_match_index]

                        # Or instead, use the known face with the smallest distance to the new face
                        face_distances = face_recognition.face_distance(
                            known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]

                        face_names.append(name)

                process_this_frame = not process_this_frame

                # Display the results
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= int(1 / ACCURACY)
                    right *= int(1 / ACCURACY)
                    bottom *= int(1 / ACCURACY)
                    left *= int(1 / ACCURACY)

                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top),
                                  (right, bottom), (0, 0, 255), 2)

                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35),
                                  (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6),
                                font, 1.0, (255, 255, 255), 1)

                # Display the resulting image
                cv2.imshow('Video', frame)
                writer.write(frame)

                # Hit 'q' on the keyboard to quit!
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as e:
            print(col.FAIL + "Error: " + col.ENDC + str(e))
        finally:
            writer.release()
            video_capture.release()
            cv2.destroyAllWindows()

        # write extracted mp3 from temp/ to FILE_PATH
        os.system(
            f"ffmpeg -i {NEW_FILE_PATH} -i temp/{FILE_NAME}.mp3 -loglevel warning -y {removeExtension(NEW_FILE_PATH)}-with_audio.mp4")
        os.remove("temp/" + str(FILE_NAME) + ".mp3")
        os.remove(NEW_FILE_PATH)


if __name__ == "__main__":
    main(parse_args())
