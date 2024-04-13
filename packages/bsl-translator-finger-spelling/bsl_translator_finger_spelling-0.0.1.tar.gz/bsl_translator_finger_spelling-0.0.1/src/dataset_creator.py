# dataset_creator.py

import pickle
import mediapipe as mp
import cv2
import os

# Load the mediapipe utils
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Load the model
hand = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)


def create_dataset_from(data_path, output_path=None):
    # Create empty lists to store the data
    data = []  # List inside a list -> data [[], [], [], ... ]
    labels = []

    # Run through all the images in the directories inside ./data
    for dir_ in os.listdir(data_path):
        for filename in os.listdir(os.path.join(data_path, dir_)):

            temp = []

            # Normalize the data so that the model learns from the relative position of the landmarks rather than the
            # position of the landmarks in an image
            norm_x = []
            norm_y = []

            # Load the image
            image = cv2.imread(os.path.join(data_path, dir_, filename))
            # image = cv2.flip(image, 1)

            # Transform the image into RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Run the mediapipe hand model
            results = hand.process(image_rgb)

            # Check for the end of the list
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    if len(results.multi_handedness) == 2:
                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y

                            norm_x.append(x)
                            norm_y.append(y)

                # Iterate through all the landmarks found
                for hand_landmarks in results.multi_hand_landmarks:
                    if len(results.multi_handedness) == 2:
                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y

                            # Normalization -> we store the difference in position (relative position) rather than the actual
                            # position
                            x = x - min(norm_x)
                            y = y - min(norm_y)

                            # Store the position of the landmarks in the data list
                            temp.append(x)
                            temp.append(y)

                if len(results.multi_handedness) == 2:
                    data.append(temp)
                    labels.append(dir_)

    for i in range(len(data)):
        if len(data[i]) != 84:
            print(len(data[i]))
            print(labels[i])
            print(i)

    output = os.path.join(output_path, "data.pickle")
    f = open(output, 'wb')
    pickle.dump({'data': data, 'labels': labels}, f)
    f.close()