import cv2
import numpy as np 
import datetime
import json

class track_COM():
	"""docstring for track_COM"""
	def __init__(self,Episode_Num,WRITE_FLAG):
		#self.vid = cv2.VideoCapture('testVideo.mp4')
		#self.length = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
		#[self.h,self.w] = [int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))]
		#or
		self.vid = cv2.VideoCapture(1)
		
		self.default()
		self.get_videoName(Episode_Num)
		self.videoWriter_Setup()
		self.get_started(WRITE_FLAG)

	def default(self):

		self.starting_point  = np.array([0,0])
		self.current_point = np.array([0,0])
		self.starting_flag = True
		self.VideoName = "Default"
		self.lower_red = np.array([0,0,150])
		self.upper_red = np.array([100,100,250])
		


	def get_videoName(self,num):

		if num < 10:
			self.VideoName =  'Episode_'+str(0)+str(0)+str(num)
		elif num < 100:
			self.VideoName =  'Episode_'+str(0)+str(num)
		else:
			self.VideoName =  'Episode_'+str(num)
		print 'Video Name Done'
		
	
	def videoWriter_Setup(self):

		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		self.videoDirectory = './EpisodeVideos/'
		name = self.videoDirectory + self.VideoName + '.avi'
		self.out = cv2.VideoWriter(name,fourcc, 20.0, (640,480))

		print 'VideoWriter Setup Done'

	def cal_COM(self,i):
		moment = cv2.moments(i)
		x = int(moment['m10']/moment['m00'])
		y = int(moment['m01']/moment['m00'])
		return (x,y)

	def do_maths(self,cnt):
		l = len(cnt)
		x=self.current_point[0]
		y=self.current_point[1]
		if l>0:
			sumx = 0
			sumy = 0

			for j in xrange(0,l):
				temp = cnt[j]
				[i,j] = self.cal_COM(temp)
				sumx = sumx+i
				sumy = sumy+j
			x = sumx//l
			y = sumy//l
		#print(x,y)
		return (x,y)

	def get_center(self,cnt):
		[a,b ] = self.do_maths(cnt)
		if (self.starting_flag==True ):
			
			if not(a ==0 and b==0):
				self.starting_point = np.array([a,b])
				self.starting_flag = False
			else:
				pass
		else:
			if not(a ==0 and b==0):
				self.current_point = np.array([a,b])

	
	def circle_detect_frame(self):
		self.ret, self.frame = self.vid.read()
		

		redBinary = cv2.inRange(self.frame,self.lower_red,self.upper_red)
		redMask = cv2.bitwise_and(self.frame,self.frame, mask = redBinary)
		redMask_gray = cv2.cvtColor(redMask, cv2.COLOR_BGR2GRAY)

		blurred = cv2.GaussianBlur(redMask_gray, (11, 11), 0)
		mask = cv2.erode(blurred, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		_, contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		
		result = cv2.drawContours(redMask, contours, -1, (255,0,0), 3)
		cv2.imshow('contour', result)
		self.get_center(contours)

	def edit_frame(self):
			timestamp =  datetime.datetime.now()
			font = cv2.FONT_HERSHEY_TRIPLEX
			cv2.putText(self.frame, str(timestamp),(50,460), font, 1,(0,0,0),2,cv2.LINE_AA)
			cv2.putText(self.frame, self.VideoName,(180,40), font, 1,(0,0,0),2,cv2.LINE_AA)
			self.out.write(self.frame)



	def get_started(self,flag):
		#change this for web cam
		#for i in xrange(0,self.length):
		while True:
			self.circle_detect_frame()
			
			if flag == True:
				self.edit_frame()

			cv2.imshow('Original', self.frame)
			
			if ord('q')==cv2.waitKey(10):
				break
		self.vid.release()
		if flag == True:
			self.out.release()

		cv2.destroyAllWindows()

	def reset(self):
		
		self.config  = {'starting_point':self.starting_point.tolist(), 'current_point':self.current_point.tolist(),
		 			'VideoName':self.VideoName,'upper_red':self.upper_red.tolist(),
		 			'lower_red':self.lower_red.tolist()}
		self.save_config()
		self.default()
	

	def save_config(self):
		s = json.dumps(self.config)
  		#print s
  		tempo = open('config.json','w')
  		json.dump(s,tempo)
  		tempo.close()

def unit_direction_vector(start, final):

	direction = np.subtract(final, start)
	unit_vector  = np.true_divide(direction,np.sqrt(np.sum(np.square(direction))))
	return unit_vector


	
if __name__ == '__main__':
	obj = track_COM(999,True)
	print 'current' +str(obj.current_point)
	print 'start'+ str(obj.starting_point)
	print unit_direction_vector(obj.current_point,obj.starting_point)

	#obj.reset()
	#print type(obj.upper_red)