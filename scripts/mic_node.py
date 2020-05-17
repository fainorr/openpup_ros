#!/usr/bin/env python

import roslib
import rospy
roslib.load_manifest('openpup_ros')
from std_msgs.msg import *
from sensor_msgs.msg import *
from numpy import *
import time
import os.path as path

from pocketsphinx import *
from sphinxbase import *

import pyaudio

# --------------------
# MICROPHONE READ NODE
# --------------------

# this node reads the mic on the brownlab laptop using the pocketsphinx voice
# recognition library

def microphone():
	pub = rospy.Publisher("/mic_output", String, queue_size=10)
	rospy.init_node('microphone', anonymous=True)
	rate = rospy.Rate(1) # Hz

	MODELDIR = "/home/brownlab/pocketsphinx/model"
	DATADIR = "/home/brownlab/pocketsphinx/test/data"

	config = Decoder.default_config()
	config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
	config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
	config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
	config.set_string('-logfn', '/dev/null')
	decoder = Decoder(config)

	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
	stream.start_stream()

	in_speech_bf = False
	decoder.start_utt()

	while not rospy.is_shutdown():
		buf = stream.read(1024)
		if buf:
			proc = decoder.process_raw(buf, False, False)
			inspeech = decoder.get_in_speech()
			#print inspeech
			if inspeech != in_speech_bf:
				in_speech_bf = decoder.get_in_speech()
				print in_speech_bf
				if not in_speech_bf:
					decoder.end_utt()
					print 'Result:', decoder.hyp().hypstr
					pub.publish(decoder.hyp().hypstr)
					decoder.start_utt()
			else:
				pass
		else:
			continue

		time.sleep(0.0001)

	decoder.end_utt()


if __name__ == '__main__':
	try:
		microphone()
	except rospy.ROSInterruptException:
		pass
