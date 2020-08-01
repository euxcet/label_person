import cv2
import threading
import numpy as np
import time
import pyaudio
import wave
import os

class AudioRecorder:
	def __init__(self):
		self.FORMAT = pyaudio.paInt16
		self.CHANNELS = 1
		self.SAMPLING_RATE = 32000
		self.CHUNK = 1024
		self.audio = pyaudio.PyAudio()
		self.stream = self.audio.open(
				format = self.FORMAT,
				channels = self.CHANNELS,
				rate = self.SAMPLING_RATE,
				input = True,
				frames_per_buffer = self.CHUNK)

		self.buffer = b''
		self._running = True
	
	def terminate(self):
		self._running = False

	def run(self, path):
		while True:
			data = self.stream.read(self.CHUNK)
			self.buffer += data

			if not self._running:
				wf = wave.open(path, 'wb')
				wf.setnchannels(self.CHANNELS)
				wf.setsampwidth(2)
				wf.setframerate(self.SAMPLING_RATE)
				wf.writeframes(self.buffer)
				wf.close()
				break
		self.stream.stop_stream()
		self.stream.close()
		self.audio.terminate()

class VideoRecorder:
	def __init__(self):
		self._running = True
	
	def terminate(self):
		self._running = False

	def run(self, path):
		cap = cv2.VideoCapture(0)
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		out = cv2.VideoWriter(path, fourcc, 25, (1280, 720))
		while self._running:
			ret, frame = cap.read()
			if ret:
				frame = cv2.flip(frame, 1)
				out.write(frame)
			else:
				break
		cap.release()
		out.release()

if __name__ == '__main__':
	vr = VideoRecorder()
	vrt = threading.Thread(target = vr.run, args=('output.avi',))
	vrt.start()

	ar = AudioRecorder()
	art = threading.Thread(target = ar.run, args=('output.wav',))
	art.start()

	time.sleep(4)

	vr.terminate()
	ar.terminate()

	vrt.join()
	art.join()
