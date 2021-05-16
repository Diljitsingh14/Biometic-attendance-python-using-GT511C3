from fps import *

def Enroll():
    # Enroll test
	# find open enroll id
	enrollid = 0
	usedid = True
	while(usedid):
		usedid = fps.CheckEnrolled(enrollid)
		if(usedid):
			enrollid += 1
	fps.EnrollStart(enrollid)
	#enroll
	print("Press finger to Enroll #")
	print(enrollid)
	while(fps.IsPressFinger() == False):
		delay(.1)
	bret = fps.CaptureFinger(True)
	iret = 0
	if(bret != False):
		print("Remove finger")
		fps.Enroll1() 
		while(fps.IsPressFinger() == True):
			delay(.1)
		print("Press same finger again")
		while(fps.IsPressFinger() == False):
			delay(.1)
		bret = fps.CaptureFinger(True)
		if(bret != False):
			print("Remove finger")
			fps.Enroll2()
			while(fps.IsPressFinger() == True):
				delay(.1)
			print("Press same finger yet again")
			while(fps.IsPressFinger() == False):
				delay(.1)
			bret = fps.CaptureFinger(True)
			if(bret != False):
				print("Remove finger")
				iret = fps.Enroll3()
				if(iret == 0):
					print("Enrolling Successful")
				else:
					print("Enrolling Failed with error code:")
					print(iret)
			else:
				print("Failed to capture third finger")
		else:
			print("Failed to capture second finger");
	else:
		print("Failed to capture first finger")
		
def find_finger():
	if(fps.IsPressFinger()):
		fps.CaptureFinger(False)
		fpid = fps.Identify1_N()
		if (fpid <200): #<- change id value depending model you are using
		    #if the fingerprint matches, provide the matching template ID
			print("Verified ID:{}".format(fpid))
			return fpid
		else:
		  #if unable to recognize
			print("Finger not found")
			return False
	else:
		print("Please press finger")
		return False

#Enroll()
class FP_sensor(FPS_GT511C3):
	def __init__(self,Debug = True):
		#super.UseSerialDebug = Debug
		super(FP_sensor,self).__init__(Debug)
		super(FP_sensor,self).SetLED()
		print("sensor open")
	
	def Off_led(self):
		super(FP_sensor,self).SetLED(on=False)

	def Enroll(self):
		# Enroll test
		# find open enroll id
		enrollid = 0
		usedid = True
		while(usedid):
			usedid = super(FP_sensor,self).CheckEnrolled(enrollid)
			if(usedid):
				enrollid += 1
		super(FP_sensor,self).EnrollStart(enrollid)
		#enroll
		print("Press finger to Enroll #")
		print(enrollid)
		while(super(FP_sensor,self).IsPressFinger() == False):
			delay(.1)
		bret = super(FP_sensor,self).CaptureFinger(True)
		iret = 0
		if(bret != False):
			print("Remove finger")
			super(FP_sensor,self).Enroll1() 
			while(super(FP_sensor,self).IsPressFinger() == True):
				delay(.1)
			print("Press same finger again")
			while(super(FP_sensor,self).IsPressFinger() == False):
				delay(.1)
			bret = super(FP_sensor,self).CaptureFinger(True)
			if(bret != False):
				print("Remove finger")
				super(FP_sensor,self).Enroll2()
				while(super(FP_sensor,self).IsPressFinger() == True):
					delay(.1)
				print("Press same finger yet again")
				while(super(FP_sensor,self).IsPressFinger() == False):
					delay(.1)
				bret = super(FP_sensor,self).CaptureFinger(True)
				if(bret != False):
					print("Remove finger")
					iret = super(FP_sensor,self).Enroll3()
					if(iret == 0):
						print("Enrolling Successful")
					else:
						print("Enrolling Failed with error code:")
						print(iret)
				else:
					print("Failed to capture third finger")
			else:
				print("Failed to capture second finger");
		else:
			print("Failed to capture first finger")
		
	def find_finger(self):
		retry = 0
		while(True):
			if(super(FP_sensor,self).IsPressFinger()):
				super(FP_sensor,self).CaptureFinger(False)
				fpid = super(FP_sensor,self).Identify1_N()
				if (fpid <200): #<- change id value depending model you are using
					#if the fingerprint matches, provide the matching template ID
					print("Verified ID: {}".format(fpid))
					return int(fpid)
				else:
				#if unable to recognize
					print("Finger not found")
					retry += 1;
			else:
				print("Please press finger")
			if retry >= 5:
				break
			delay(.1)

	def __del__(self):
		self.Off_led()
		super(FP_sensor,self).Close()

DEVICE_NAME = "/dev/ttyAMA0"
fps = FP_sensor(Debug = False)
#delay(1)
#fps.Enroll()
print(fps.GetEnrollCount())
#a = fps.find_finger()
#if(a < 200):
#	print("welcome")
#else:
#	print("failed")



