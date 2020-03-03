#!/usr/bin/env python

# MICROPHONE READ NODE

import roslib
import rospy
roslib.load_manifest('openpup_ros')
from std_msgs.msg import *
from sensor_msgs.msg import *
from numpy import *
import time

from pocketsphinx import *
from sphinxbase import *

def microphone():
    pub = rospy.Publisher("/output", String, queue_size=10)
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

    stream = open(path.join(DATADIR, 'goforward.raw'), 'rb')
    #stream = open('10001-90210-01803.wav', 'rb')

    in_speech_bf = False
    decoder.start_utt()

    while not rospy.is_shutdown():

        buf = stream.read(1024)
        if buf:
            decoder.process_raw(buf, False, False)
            if decoder.get_in_speech() != in_speech_bf:
                in_speech_bf = decoder.get_in_speech()
                if not in_speech_bf:
                    decoder.end_utt()
                    print 'Result:', decoder.hyp().hypstr
                    decoder.start_utt()
        else:
            break

        pub.publish(decoder.hyp().hypstr)
        rate.sleep()

    decoder.end_utt()

if __name__ == '__main__':
	try:
        microphone()
    except rospy.ROSInterruptException:
        pass
