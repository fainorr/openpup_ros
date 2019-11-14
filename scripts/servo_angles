
# SERVO CONTROL NODE


class servo_angles():




# NEEDS UPDATING TO ROS




sangf1 = zeros(len(t))
sangt1 = zeros(len(t))
sangs1 = zeros(len(t))

sangf2 = zeros(len(t))
sangt2 = zeros(len(t))
sangs2 = zeros(len(t))

sangf3 = zeros(len(t))
sangt3 = zeros(len(t))
sangs3 = zeros(len(t))

sangf4 = zeros(len(t))
sangt4 = zeros(len(t))
sangs4 = zeros(len(t))


def set_servo_pulse(channel, pulse):
	pulse_length = 1000000
	pulse_length //=60
	print('{0}us per bit' .format (pulse_length))
	pulse *= 1000
	pulse //= pulse_length
	pwm.set_pwm(channel, 0, pulse)
	pwm.set_pwm_freq(100)



#tibia and femur angles in radians
for i in range(0,len(t)):
	angs1[i], angf1[i], angt1[i] = getServoAng(x1[i], y1[i], z1[i], ls, lf, lt, 1)
	angs2[i], angf2[i], angt2[i] = getServoAng(x2[i], y2[i], z2[i], ls, lf, lt, 2)
	angs3[i], angf3[i], angt3[i] = getServoAng(x3[i], y3[i], z3[i], ls, lf, lt, 3)
	angs4[i], angf4[i], angt4[i] = getServoAng(x4[i], y4[i], z4[i], ls, lf, lt, 4)

	if angf1[i] > 0: angf1[i] = angf1[i] - 2*pi
	if angf3[i] > 0: angf3[i] = angf3[i] - 2*pi

	print(str(angt1[i])+", "+ str(angf1[i])+", "+str(angt2[i])+", "+str(angf2[i])+", "+str(angt3[i])+", "+str(angf3[i])+", "+str(angt4[i])+", "+str(angf4[i]))


#converting the radians to servo angles

	sangf1[i]=(840*angf1[i])/(pi/2)
	sangt1[i]=(800*angt1[i])/(pi/2)
	sangs1[i]=(760*angs1[i])/(pi/2)

	sangf2[i]=(780*angf2[i])/(pi/2)
	sangt2[i]=(760*angt2[i])/(pi/2)
	sangs2[i]=(760*angs2[i])/(pi/2)

	sangf3[i]=(800*angf3[i])/(pi/2)
	sangt3[i]=(760*angt3[i])/(pi/2)
	sangs3[i]=(760*angs3[i])/(pi/2)

	sangf4[i]=(800*angf4[i])/(pi/2)
	sangt4[i]=(760*angt4[i])/(pi/2)
	sangs4[i]=(760*angs4[i])/(pi/2)


#angle offset values
tib1_offset = 1800
fem1_offset = 1720
sh1_offset = 2000

tib2_offset = 300
fem2_offset = 400
sh2_offset = 500

tib3_offset = 1800
fem3_offset = 1800
sh3_offset = 2000

tib4_offset = 300
fem4_offset = 420
sh4_offset = 500


#sending the servo angles to indivial servos

i=0

while True:

	i = i+1
	i_c = i%len(sangt1)

	# check zeros

	if (zero == 1):
		pwm.set_pwm(0, 0, tib2_offset+760)
		pwm.set_pwm(1, 0, fem2_offset+780)
		#pwm.set_pwm(2, 0, sh2_offset)

		pwm.set_pwm(3, 0, tib1_offset-800)
		pwm.set_pwm(4, 0, fem1_offset-840)
		#pwm.set_pwm(5, 0, sh1_offset)

		time.sleep(0.01)

		pwm.set_pwm(8, 0, fem3_offset-800)
		pwm.set_pwm(9, 0, tib3_offset-760)
 		#pwm.set_pwm(10, 0, sh3_offset)

		pwm.set_pwm(12, 0, fem4_offset+800)
		pwm.set_pwm(7, 0, tib4_offset+760)
		pwm.set_pwm(13, 0, sh4_offset)


	# control servos

	else:
		pwm.set_pwm(0, 0, tib2_offset + int(sangt2[i_c]))		#port 0: right front tibia
		pwm.set_pwm(1, 0, fem2_offset + int(sangf2[i_c]))		#port 1: right front femur
		pwm.set_pwm(2, 0, sh2_offset - int(sangs2[i_c]))		#port 2: right front hip

		pwm.set_pwm(3, 0, tib1_offset + int(sangt1[i_c]))		#port 3: left front tibia
		pwm.set_pwm(4, 0, fem1_offset + int(sangf1[i_c]))		#port 4: left front femur
		pwm.set_pwm(5, 0, sh1_offset - int(sangs1[i_c]))		#port 5: left front hip

		time.sleep(0.01)

		pwm.set_pwm(8, 0, fem3_offset + int(sangf3[i_c]))		#port 8: left back femur
		pwm.set_pwm(9, 0, tib3_offset + int(sangt3[i_c]))		#port 9: left back tibia
		pwm.set_pwm(10, 0, sh3_offset - int(sangs3[i_c]))		#port 10: left back hip


		pwm.set_pwm(12, 0, fem4_offset + int(sangf4[i_c]))		#port 6: right back femur
		pwm.set_pwm(7, 0, tib4_offset + int(sangt4[i_c]))		#port 7: right back tibia
		pwm.set_pwm(13, 0, sh4_offset - int(sangs4[i_c]))		#port 11: right back hip


	print(str(time.time())+", "+str(int(sangt1[i%len(sangt1)]))+", "+ str(int(sangf1[i%len(sangf1)]))+", "+ str(int(sangs1[i%len(sangs1)])))


