# openpup_ros
During the 2019-2020 school year, the locomotion sub-team of Lafayette's openDog senior design created this ROS package for prototyping walking gaits on the **openPup** platform.  This repository contains all files related to servo control, sensor processing, and walking finite state machines.  Included below are descriptions of each node and the launch files for running tests on openPup.

To utilize this package, first log into the openPup's raspberry pi.  With a micro-usb plugged into the USB port on the pi, use the Terminal application and run "ssh pi@raspberrypi.local", and then enter the password "rosbots!" when prompted.  From here, launch files are run by "roslaunch openpup_ros <file_name>.launch".


## LAUNCH:

1. **openpup_wii.launch**: this file launches the joystick node to read the wii remote's input.

    - This remote must first be connected via bluetooth.  Once on the pi, press the red button on the back of the wii remote and run "sudo bluetoothctl" to see all the bluetooth devices available.  Find the wii remote in the list, copy its 12-digit identifier, and type "exit" to return to the pi.  Finally, run "connect <identifier>" to connect to the remote.  Once this is achieved, the run the launch file

2. **openpup_mic.launch** and **openpup_mic_laptop.launch**: this pair of launch files (one for launching on the laptop with microphone and one for launching on the pi) controls the pup using voice commands.

3. **openpup_autonomous.launch**: using the ultrasonic sensor, this launch file controls the pup for basic autonomous obstacle avoidance based on a series of timers.  An overview of the FSM is illustrated in the [**openpup ultrasonic FSM**](https://github.com/fainorr/openpup_ros/tree/master/images/ultrasonic_FSM.pdf).


## SCRIPTS:

**controlling openPup**

1. **servo_control_node.py**: this node, when receiving state machine instructions in the form of an "action" and a "direction", controls the servos on the pup by calling two classes of functions:

    - **inverse_kinematics.py**: this class of functions converts the FSM instructions into joint angles by first defining the x, y, and z positions of the feet based on the action and current time and then finding the joint angles using the IK equations.

    - **servo_angles.py**: after the node fins the IK angles, it passes them to this function which converts them to servo "angles", or pulses to send to the servo control board.  This function is what actually moves the legs.


**using sensors**

2. **mic_node.py**: this node reads the mic on the brownlab laptop using the pocketsphinx voice recognition library and publishes the result as a string to the topic /mic_output.

3. **ultrasonic_node.py**: this node reads the ultrasonic signal and calculates the distance based on the time between sending and receiving a pulse. It publishes a float, /sonar_dist.


**finite state machines**

4. **openpup_FSM.py**: this FSM does not utilize sensors at all; it simply uses a sequence of timers to cycle through various movements to test the inverse kinematics and servo controller.

5. **openpup_wii_FSM.py**: to control the pup with a wii remote, this FSM subscribes to the /joy topic and sets the action based on a user's input.

6. **openpup_voice_FSM.py**: this FSM subscribes to the microphone to make the pup swivel, stop, and lay down on voice command.

7. **openpup_ultra_FSM.py**: this FSM is a basic obstacle avoidance controller using the ultrasonic sensor.
