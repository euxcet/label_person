import sys
import cv2
import os
import tqdm
import argparse
sys.path.append('D:/openpose/build/python/openpose/Release')
import pyopenpose as op
from utils import *
from database import Mongo


class OpenposeExtractor:
    def __init__(self):
        self.db = Mongo()
        self.db.clear()
        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        params = dict()
        params["model_folder"] = "models/"
        params["face"] = False
        params["hand"] = False
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(params)
        self.opWrapper.start()



    def getFaceRectangle(self, pose, height, width):
        minRec = (10000, 10000)
        maxRec = (0, 0)
        nose = pose[0][0]
        REar = pose[0][17]
        LEar = pose[0][18]
        RShoulder = pose[0][2]
        LShoulder = pose[0][5]
        RShoulderSym = RShoulder
        LShoulderSym = LShoulder

        if nose[0] > 1.0:
            if REar[0] > 1.0 and (LEar[0] < 1.0 or distance(REar, nose) > distance(LEar, nose)):
                RShoulderSym = symmetry(RShoulder, REar, nose)
                LShoulderSym = symmetry(LShoulder, REar, nose)
            elif LEar[0] > 1.0:
                RShoulderSym = symmetry(RShoulder, LEar, nose)
                LShoulderSym = symmetry(LShoulder, LEar, nose)

        minRec = minPoint(minRec, nose)
        minRec = minPoint(minRec, REar)
        minRec = minPoint(minRec, LEar)
        minRec = minPoint(minRec, RShoulder)
        minRec = minPoint(minRec, LShoulder)
        minRec = minPoint(minRec, RShoulderSym)
        minRec = minPoint(minRec, LShoulderSym)

        maxRec = maxPoint(maxRec, nose)
        maxRec = maxPoint(maxRec, REar)
        maxRec = maxPoint(maxRec, LEar)
        maxRec = maxPoint(maxRec, RShoulder)
        maxRec = maxPoint(maxRec, LShoulder)
        maxRec = maxPoint(maxRec, RShoulderSym)
        maxRec = maxPoint(maxRec, LShoulderSym)

        dlt = ((maxRec[0] - minRec[0]) / 4, (maxRec[1] - minRec[1]) / 4)
        minRec = (max(int(minRec[0] - dlt[0]), 0), max(int(minRec[1] - dlt[1]), 0))
        maxRec = (min(int(maxRec[0] + dlt[0]), width - 1), min(int(maxRec[1] + dlt[1]), height - 1))

        return minRec, maxRec


    def extract(self, video_path, output_path, frame_folder, face_folder):
        capture = cv2.VideoCapture(video_path)
        if not capture.isOpened():
            print("Failed to load video", video_path)
            return
        fps = capture.get(cv2.CAP_PROP_FPS)
        frame_count = capture.get(cv2.CAP_PROP_FRAME_COUNT)
        frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        datum = op.Datum()

        head_points = [0, 1, 2, 5, 15, 16, 17, 18]


        print("video path:", video_path)
        print("output path:", output_path)
        print("frame folder:", frame_folder)
        print("face folder:", face_folder)
        print("fps:", fps)
        print("frame count:", frame_count)
        print("width:", frame_width)
        print("height:", frame_height, flush=True)


        with tqdm.tqdm(total=frame_count) as bar:
            count = 0
            while True:
                ret, frame = capture.read()
                if ret:
                    count += 1
                    bar.update(1)
                    datum.cvInputData = frame
                    self.opWrapper.emplaceAndPop([datum])
                    if datum.poseKeypoints.shape != ():
                        minRec, maxRec = self.getFaceRectangle(datum.poseKeypoints, frame.shape[0], frame.shape[1])
                        face = frame[minRec[0]:maxRec[0], minRec[1]:maxRec[1]]
                        if maxRec[0] != 0 and maxRec[1] != 0:
                            if count % 10 == 0:
                                figure_path = os.path.join(frame_folder, str(count) + '.png')
                                face_path = os.path.join(face_folder, str(count) + '.png')
                                cv2.imwrite(face_path, frame[minRec[1]:maxRec[1] + 1, minRec[0]:maxRec[0] + 1])
                                cv2.rectangle(frame, minRec, maxRec, (0, 255, 0), 2)
                                cv2.imwrite(figure_path, frame)
                                self.db.insert_figure(figure_path, face_path, 0, frame_width, frame_height, (minRec[0] + maxRec[0]) // 2, (minRec[1] + maxRec[1]) // 2)
                            else:
                                cv2.rectangle(frame, minRec, maxRec, (0, 255, 0), 2)

                    out.write(frame)
                    cv2.waitKey(10)
                else:
                    break
            bar.close()

    def extractFolder(self, folder, save_folder):
        makedirs(save_folder)

        for home, dirs, files in os.walk(folder):
            save_home = save_folder + home[len(folder):]
            makedirs(save_home)
            for f in files:
                if os.path.splitext(f)[-1] in ['.avi', '.mp4']:
                    path = os.path.join(home, f)
                    if self.db.search_video(path) is not None:
                        continue

                    folder = os.path.join(save_home, os.path.splitext(f)[0])
                    video_folder = os.path.join(folder, 'video')
                    frame_folder = os.path.join(folder, 'frame')
                    face_folder = os.path.join(folder, 'face')
                    makedirs(folder)
                    makedirs(video_folder)
                    makedirs(frame_folder)
                    makedirs(face_folder)
                    output_path = os.path.join(video_folder, 'video.avi')

                    path = os.path.join(os.getcwd(), path)
                    output_path = os.path.join(os.getcwd(), output_path)
                    frame_folder = os.path.join(os.getcwd(), frame_folder)
                    face_folder = os.path.join(os.getcwd(), face_folder)

                    self.extract(path, output_path, frame_folder, face_folder)
                    self.db.insert_video(path, output_path, frame_folder, face_folder)

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc != 3:
        print('usage: python openpose_extractor.py [source folder] [output folder]')
    else:
        for i in sys.argv:
            print(i)
        extractor = OpenposeExtractor()
        extractor.extractFolder(sys.argv[1], sys.argv[2])
