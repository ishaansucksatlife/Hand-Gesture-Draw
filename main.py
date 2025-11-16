import cv2,numpy as np,mediapipe as mp,math
from collections import deque
import time,os
from datetime import datetime
import traceback
class PerfectHandWhiteboard:
	def __init__(self):
		self.mp_hands=mp.solutions.hands;self.mp_draw=mp.solutions.drawing_utils;self.hands=self.mp_hands.Hands(static_image_mode=False,max_num_hands=2,min_detection_confidence=.7,min_tracking_confidence=.7,model_complexity=1);self.colors=[(0,255,0),(255,0,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255),(255,255,255),(128,128,128),(0,165,255),(128,0,128),(128,128,0),(0,128,128),(203,192,255),(42,42,165),(0,0,0),(130,0,75)];self.color_names=['GREEN','BLUE','RED','CYAN','MAGENTA','YELLOW','WHITE','GRAY','ORANGE','PURPLE','TEAL','OLIVE','PINK','BROWN','BLACK','INDIGO'];self.current_color_index=0;self.color=self.colors[self.current_color_index];self.brush_sizes=[3,6,9,12,15,20];self.current_brush_size=2;self.brush_thickness=self.brush_sizes[self.current_brush_size];self.eraser_sizes=[15,25,35,50];self.current_eraser_size=1;self.eraser_thickness=self.eraser_sizes[self.current_eraser_size];self.drawing_tools=['brush','spray','fill'];self.current_tool=0;self.spray_density=20;self.spray_radius=15;self.canvas_width=1920;self.canvas_height=1080;self.canvas=np.ones((self.canvas_height,self.canvas_width,3),dtype=np.uint8)*255;self.cam_width=1280;self.cam_height=720;self.history=deque(maxlen=20);self.redo_stack=deque(maxlen=20);self.left_hand={'drawing':False,'tool_active':False,'prev_point':None,'current_point':None,'points_buffer':deque(maxlen=5),'active':False,'tool_change_triggered':False,'brush_change_triggered':False,'brush_change_start_time':0,'brush_change_held':False,'stable_points':deque(maxlen=8),'last_active_time':0,'velocity':(0,0),'acceleration':(0,0),'gesture_confidence':0,'smooth_position':None,'last_gesture':'none','gesture_start_time':0,'gesture_cooldown':0};self.right_hand={'drawing':False,'erasing':False,'prev_point':None,'current_point':None,'points_buffer':deque(maxlen=5),'active':False,'color_change_triggered':False,'stable_points':deque(maxlen=8),'last_active_time':0,'velocity':(0,0),'acceleration':(0,0),'gesture_confidence':0,'smooth_position':None,'last_gesture':'none','gesture_start_time':0,'gesture_cooldown':0};self.gesture_cooldowns={'color_change':0,'brush_change':0,'tool_change':0,'drawing':0,'erasing':0};self.fps=0;self.frame_times=deque(maxlen=60);self.performance_stats={'min_fps':float('inf'),'max_fps':0,'avg_fps':0};self.hand_timeout_threshold=3.
		try:self.cap=cv2.VideoCapture(0);self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,self.cam_width);self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,self.cam_height);self.cap.set(cv2.CAP_PROP_FPS,60)
		except:raise RuntimeError('Could not open camera.')
		os.makedirs('saved_drawings',exist_ok=True)
	def update_performance_metrics(self):
		current_time=time.time();self.frame_times.append(current_time)
		if len(self.frame_times)>1:
			time_diff=self.frame_times[-1]-self.frame_times[0]
			if time_diff>0:
				self.fps=len(self.frame_times)/time_diff;self.performance_stats['min_fps']=min(self.performance_stats['min_fps'],self.fps);self.performance_stats['max_fps']=max(self.performance_stats['max_fps'],self.fps)
				if self.performance_stats['avg_fps']==0:self.performance_stats['avg_fps']=self.fps
				else:self.performance_stats['avg_fps']=.95*self.performance_stats['avg_fps']+.05*self.fps
	def check_hand_timeouts(self):
		current_time=time.time()
		for hand in[self.left_hand,self.right_hand]:
			if hand['active']and current_time-hand['last_active_time']>self.hand_timeout_threshold:hand['active']=False;hand['prev_point']=None;hand['points_buffer'].clear();hand['drawing']=False;hand['erasing']=False;hand['tool_active']=False
	def get_landmark_coords(self,hand_landmarks,landmark_index):
		try:h,w,c=self.frame.shape;landmark=hand_landmarks.landmark[landmark_index];x=landmark.x*w;y=landmark.y*h;return x,y
		except:return
	def map_to_canvas(self,camera_point):
		if camera_point is None:return
		scale_x=self.canvas_width/self.cam_width;scale_y=self.canvas_height/self.cam_height;scale=min(scale_x,scale_y);offset_x=(self.canvas_width-self.cam_width*scale)/2;offset_y=(self.canvas_height-self.cam_height*scale)/2;canvas_x=int(camera_point[0]*scale+offset_x);canvas_y=int(camera_point[1]*scale+offset_y);canvas_x=max(0,min(canvas_x,self.canvas_width-1));canvas_y=max(0,min(canvas_y,self.canvas_height-1));return canvas_x,canvas_y
	def calculate_distance(self,point1,point2):
		if point1 is None or point2 is None:return float('inf')
		dx=point2[0]-point1[0];dy=point2[1]-point1[1];return math.sqrt(dx*dx+dy*dy)
	def calculate_hand_metrics(self,hand_landmarks,hand):
		try:
			wrist=self.get_landmark_coords(hand_landmarks,self.mp_hands.HandLandmark.WRIST)
			if wrist is None:return 0,0,0
			wrist_canvas=self.map_to_canvas(wrist);hand['stable_points'].append(wrist_canvas);thumb_tip=self.get_landmark_coords(hand_landmarks,self.mp_hands.HandLandmark.THUMB_TIP);pinky_tip=self.get_landmark_coords(hand_landmarks,self.mp_hands.HandLandmark.PINKY_TIP)
			if thumb_tip and pinky_tip:hand_size=self.calculate_distance(thumb_tip,pinky_tip)
			else:hand_size=100
			if len(hand['stable_points'])>=5:recent_points=list(hand['stable_points'])[-5:];avg_x=sum(p[0]for p in recent_points)/len(recent_points);avg_y=sum(p[1]for p in recent_points)/len(recent_points);stability=sum((p[0]-avg_x)**2+(p[1]-avg_y)**2 for p in recent_points)/len(recent_points)
			else:stability=100
			if hand['smooth_position']and len(hand['stable_points'])>=2:
				current_pos=wrist_canvas;last_pos=hand['smooth_position'];dt=1./max(self.fps,30);vx=(current_pos[0]-last_pos[0])/dt;vy=(current_pos[1]-last_pos[1])/dt;hand['velocity']=vx,vy
				if hand['velocity'][0]!=0 or hand['velocity'][1]!=0:ax=vx/dt;ay=vy/dt;hand['acceleration']=ax,ay
			hand['smooth_position']=wrist_canvas;return hand_size,stability,self.calculate_gesture_confidence(hand)
		except:return 100,100,.1
	def calculate_gesture_confidence(self,hand):
		try:velocity_magnitude=math.sqrt(hand['velocity'][0]**2+hand['velocity'][1]**2);acceleration_magnitude=math.sqrt(hand['acceleration'][0]**2+hand['acceleration'][1]**2);speed_confidence=max(0,1-velocity_magnitude/500);accel_confidence=max(0,1-acceleration_magnitude/1000);return(speed_confidence+accel_confidence)/2
		except:return .1
	def is_advanced_pinch_gesture(self,hand_landmarks,finger_tip_index,hand):
		try:
			thumb_tip=self.get_landmark_coords(hand_landmarks,self.mp_hands.HandLandmark.THUMB_TIP);finger_tip=self.get_landmark_coords(hand_landmarks,finger_tip_index)
			if thumb_tip is None or finger_tip is None:return False,None,None,0
			distance=self.calculate_distance(thumb_tip,finger_tip);hand_size,stability,confidence=self.calculate_hand_metrics(hand_landmarks,hand);base_threshold=50;dynamic_threshold=base_threshold*(.8+.4*confidence);other_fingers_too_close=False;other_finger_indices=[self.mp_hands.HandLandmark.INDEX_FINGER_TIP,self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,self.mp_hands.HandLandmark.RING_FINGER_TIP,self.mp_hands.HandLandmark.PINKY_TIP];other_finger_indices=[idx for idx in other_finger_indices if idx!=finger_tip_index]
			for other_finger_index in other_finger_indices:
				other_finger_tip=self.get_landmark_coords(hand_landmarks,other_finger_index)
				if other_finger_tip:
					other_distance=self.calculate_distance(thumb_tip,other_finger_tip)
					if other_distance<dynamic_threshold*1.2:other_fingers_too_close=True;confidence*=.3;break
			wrist=self.get_landmark_coords(hand_landmarks,self.mp_hands.HandLandmark.WRIST)
			if wrist:thumb_to_wrist=self.calculate_distance(thumb_tip,wrist);finger_to_wrist=self.calculate_distance(finger_tip,wrist);extension_ratio=min(thumb_to_wrist,finger_to_wrist)/max(thumb_to_wrist,finger_to_wrist);extension_confidence=min(1.,extension_ratio*2);confidence=(confidence+extension_confidence)/2
			is_pinching=distance<dynamic_threshold and confidence>.4 and not other_fingers_too_close;return is_pinching,thumb_tip,finger_tip,confidence
		except:return False,None,None,0
	def is_index_thumb_pinch(self,hand_landmarks,hand):return self.is_advanced_pinch_gesture(hand_landmarks,self.mp_hands.HandLandmark.INDEX_FINGER_TIP,hand)
	def is_middle_thumb_pinch(self,hand_landmarks,hand):return self.is_advanced_pinch_gesture(hand_landmarks,self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,hand)
	def is_ring_thumb_pinch(self,hand_landmarks,hand):return self.is_advanced_pinch_gesture(hand_landmarks,self.mp_hands.HandLandmark.RING_FINGER_TIP,hand)
	def is_pinky_thumb_pinch(self,hand_landmarks,hand):return self.is_advanced_pinch_gesture(hand_landmarks,self.mp_hands.HandLandmark.PINKY_TIP,hand)
	def get_pinch_center(self,thumb_tip,finger_tip):
		if thumb_tip is None or finger_tip is None:return
		return(thumb_tip[0]+finger_tip[0])/2,(thumb_tip[1]+finger_tip[1])/2
	def advanced_smooth_point(self,new_point,hand):
		if new_point is None:return hand['points_buffer'][-1]if hand['points_buffer']else None
		canvas_point=self.map_to_canvas(new_point)
		if canvas_point is None:return
		if hand['points_buffer']and hand['velocity']!=(0,0):last_point=hand['points_buffer'][-1];predicted_x=last_point[0]+hand['velocity'][0]*.1;predicted_y=last_point[1]+hand['velocity'][1]*.1;predicted_point=predicted_x,predicted_y;confidence=hand.get('gesture_confidence',.5);blend_factor=.3*confidence;canvas_point=canvas_point[0]*(1-blend_factor)+predicted_point[0]*blend_factor,canvas_point[1]*(1-blend_factor)+predicted_point[1]*blend_factor
		hand['points_buffer'].append(canvas_point)
		if len(hand['points_buffer'])==1:return canvas_point
		weights=[];confidence=hand.get('gesture_confidence',.5)
		for i in range(len(hand['points_buffer'])):base_weight=.5**(len(hand['points_buffer'])-i-1);confidence_weight=base_weight*(.5+.5*confidence);weights.append(confidence_weight)
		total_weight=sum(weights);avg_x=sum(p[0]*w for(p,w)in zip(hand['points_buffer'],weights))/total_weight;avg_y=sum(p[1]*w for(p,w)in zip(hand['points_buffer'],weights))/total_weight;return avg_x,avg_y
	def use_brush_tool(self,position,hand):
		if position is None:return
		int_position=int(position[0]),int(position[1]);hand['current_point']=int_position
		if hand['prev_point']is not None:cv2.line(self.canvas,hand['prev_point'],int_position,self.color,self.brush_thickness,lineType=cv2.LINE_AA);cv2.circle(self.canvas,int_position,max(1,self.brush_thickness//2),self.color,-1,lineType=cv2.LINE_AA)
		hand['prev_point']=int_position
	def use_spray_tool(self,position,hand):
		if position is None:return
		int_position=int(position[0]),int(position[1])
		for _ in range(self.spray_density):angle=np.random.random()*2*math.pi;radius=np.random.random()*self.spray_radius;dx=radius*math.cos(angle);dy=radius*math.sin(angle);spray_point=int(int_position[0]+dx),int(int_position[1]+dy);dot_size=max(1,np.random.randint(1,3));cv2.circle(self.canvas,spray_point,dot_size,self.color,-1)
	def use_fill_tool(self,position):
		if position is None:return
		int_position=int(position[0]),int(position[1]);self.save_state();temp_canvas=self.canvas.copy();h,w=temp_canvas.shape[:2];mask=np.zeros((h+2,w+2),np.uint8);fill_color=self.color;lo_diff=20,20,20;up_diff=20,20,20;seed_point=int_position[0],int_position[1]
		if 0<=seed_point[0]<w and 0<=seed_point[1]<h:
			seed_color=temp_canvas[seed_point[1],seed_point[0]]
			if np.array_equal(seed_color,fill_color):return
			flags=65284|cv2.FLOODFILL_FIXED_RANGE
			try:cv2.floodFill(temp_canvas,mask,seed_point,fill_color,loDiff=lo_diff,upDiff=up_diff,flags=flags);self.canvas=temp_canvas
			except Exception as e:pass
	def save_state(self):
		try:
			if self.canvas is not None:self.history.append(self.canvas.copy());self.redo_stack.clear()
		except:pass
	def undo(self):
		try:
			if self.history:self.redo_stack.append(self.canvas.copy());self.canvas=self.history.pop()
		except:pass
	def redo(self):
		try:
			if self.redo_stack:self.history.append(self.canvas.copy());self.canvas=self.redo_stack.pop()
		except:pass
	def process_left_hand_tools(self,hand_landmarks):
		hand=self.left_hand;hand['active']=True;hand['last_active_time']=time.time();hand['tool_active']=False;hand_size,stability,confidence=self.calculate_hand_metrics(hand_landmarks,hand);hand['gesture_confidence']=confidence;is_brush_gesture,thumb_brush,index_tip,brush_conf=self.is_index_thumb_pinch(hand_landmarks,hand);is_spray_gesture,thumb_spray,middle_tip,spray_conf=self.is_middle_thumb_pinch(hand_landmarks,hand);is_brush_change_gesture,thumb_brush_change,ring_tip,brush_change_conf=self.is_ring_thumb_pinch(hand_landmarks,hand);is_fill_gesture,thumb_fill,pinky_tip,fill_conf=self.is_pinky_thumb_pinch(hand_landmarks,hand);active_gestures=[]
		if is_brush_gesture and brush_conf>.5:active_gestures.append(('brush',brush_conf))
		if is_spray_gesture and spray_conf>.5:active_gestures.append(('spray',spray_conf))
		if is_brush_change_gesture and brush_change_conf>.5:active_gestures.append(('brush_change',brush_change_conf))
		if is_fill_gesture and fill_conf>.5:active_gestures.append(('fill',fill_conf))
		if len(active_gestures)==1:
			tool_name,tool_confidence=active_gestures[0];current_time=time.time()
			if hand['gesture_cooldown']>0:return'none',None
			if tool_confidence>.6 and hand['last_gesture']!=tool_name:
				if tool_name=='brush':self.current_tool=0
				elif tool_name=='spray':self.current_tool=1
				elif tool_name=='fill':self.current_tool=2
				hand['last_gesture']=tool_name;hand['gesture_start_time']=current_time;hand['gesture_cooldown']=15;return f"tool_{tool_name}",None
		if is_brush_change_gesture and brush_change_conf>.6:
			current_time=time.time()
			if not hand['brush_change_held']:hand['brush_change_start_time']=current_time;hand['brush_change_held']=True
			hold_duration=current_time-hand['brush_change_start_time']
			if thumb_brush_change and ring_tip:
				pinch_center=self.get_pinch_center(thumb_brush_change,ring_tip);canvas_center=self.map_to_canvas(pinch_center)
				if canvas_center:
					center_x,center_y=canvas_center;progress=min(hold_duration/1.,1.);radius=25;confidence_color=0,int(255*brush_change_conf),255;cv2.circle(self.display_frame,(center_x,center_y),radius,confidence_color,2);angle=int(360*progress);cv2.ellipse(self.display_frame,(center_x,center_y),(radius,radius),0,0,angle,confidence_color,4)
					if hold_duration<1.:remaining=1.-hold_duration;cv2.putText(self.display_frame,f"{remaining:.1f}s",(center_x-15,center_y+5),cv2.FONT_HERSHEY_SIMPLEX,.6,confidence_color,2)
					else:cv2.putText(self.display_frame,'CHANGE!',(center_x-30,center_y+5),cv2.FONT_HERSHEY_SIMPLEX,.6,(0,255,0),2)
			if hold_duration>=1. and not hand['brush_change_triggered']and self.gesture_cooldowns['brush_change']==0:self.current_brush_size=(self.current_brush_size+1)%len(self.brush_sizes);self.brush_thickness=self.brush_sizes[self.current_brush_size];self.gesture_cooldowns['brush_change']=25;hand['brush_change_triggered']=True;hand['prev_point']=None;hand['points_buffer'].clear();return'brush_change',None
		else:hand['brush_change_held']=False;hand['brush_change_triggered']=False
		if hand['gesture_cooldown']>0:hand['gesture_cooldown']-=1
		return'none',None
	def process_right_hand_gestures(self,hand_landmarks):
		hand=self.right_hand;hand['active']=True;hand['last_active_time']=time.time();hand['drawing']=False;hand['erasing']=False;hand_size,stability,confidence=self.calculate_hand_metrics(hand_landmarks,hand);hand['gesture_confidence']=confidence;is_draw_pinch,thumb_tip_draw,index_tip,draw_confidence=self.is_index_thumb_pinch(hand_landmarks,hand);is_erase_pinch,thumb_tip_erase,middle_tip,erase_confidence=self.is_middle_thumb_pinch(hand_landmarks,hand);is_color_change_pinch,thumb_tip_color,pinky_tip,color_confidence=self.is_pinky_thumb_pinch(hand_landmarks,hand);active_gestures=[]
		if is_draw_pinch and draw_confidence>.5:active_gestures.append(('drawing',draw_confidence))
		if is_erase_pinch and erase_confidence>.5:active_gestures.append(('erasing',erase_confidence))
		if is_color_change_pinch and color_confidence>.6:active_gestures.append(('color_change',color_confidence))
		if len(active_gestures)>1:active_gestures.sort(key=lambda x:x[1],reverse=True);active_gestures=[active_gestures[0]]
		if is_color_change_pinch and color_confidence>.6 and('color_change',color_confidence)in active_gestures:
			if not hand['color_change_triggered']and self.gesture_cooldowns['color_change']==0:self.current_color_index=(self.current_color_index+1)%len(self.colors);self.color=self.colors[self.current_color_index];self.gesture_cooldowns['color_change']=20;hand['color_change_triggered']=True;hand['prev_point']=None;hand['points_buffer'].clear();return'color_change',None
		else:hand['color_change_triggered']=False
		if is_draw_pinch and not is_erase_pinch and draw_confidence>.5 and('drawing',draw_confidence)in active_gestures:
			hand['drawing']=True;pinch_center=self.get_pinch_center(thumb_tip_draw,index_tip)
			if pinch_center:
				smooth_point=self.advanced_smooth_point(pinch_center,hand)
				if hand['prev_point']is None and self.current_tool in[0,1]:self.save_state()
				if self.current_tool==0:self.use_brush_tool(smooth_point,hand)
				elif self.current_tool==1:self.use_spray_tool(smooth_point,hand)
				elif self.current_tool==2:self.use_fill_tool(smooth_point);hand['prev_point']=None;return'fill',smooth_point
				return'drawing',smooth_point
		elif is_erase_pinch and not is_draw_pinch and erase_confidence>.5 and('erasing',erase_confidence)in active_gestures:
			hand['erasing']=True;pinch_center=self.get_pinch_center(thumb_tip_erase,middle_tip)
			if pinch_center:
				smooth_point=self.advanced_smooth_point(pinch_center,hand)
				if hand['prev_point']is None:self.save_state()
				int_position=int(smooth_point[0]),int(smooth_point[1]);hand['current_point']=int_position
				if hand['prev_point']is not None:cv2.line(self.canvas,hand['prev_point'],int_position,(255,255,255),self.eraser_thickness,lineType=cv2.LINE_AA)
				hand['prev_point']=int_position;return'erasing',smooth_point
		hand['prev_point']=None;hand['points_buffer'].clear();return'none',None
	def draw_interface(self,frame):
		panel_width,panel_height=550,300;cv2.rectangle(frame,(10,10),(panel_width,panel_height),(40,40,60),-1);cv2.rectangle(frame,(10,10),(panel_width,panel_height),(200,200,200),2);cv2.putText(frame,'Hand Gesture WHITEBOARD',(20,35),cv2.FONT_HERSHEY_SIMPLEX,.7,(255,255,255),2);fps_color=(0,255,0)if self.fps>30 else(0,255,255)if self.fps>15 else(0,100,255);cv2.putText(frame,f"FPS: {self.fps:.1f}",(panel_width-100,35),cv2.FONT_HERSHEY_SIMPLEX,.5,fps_color,1);cv2.putText(frame,f"Avg: {self.performance_stats['avg_fps']:.1f}",(panel_width-100,55),cv2.FONT_HERSHEY_SIMPLEX,.4,(200,200,200),1);current_tool=self.drawing_tools[self.current_tool].upper();color_name=self.color_names[self.current_color_index];cv2.putText(frame,f"Tool: {current_tool}",(20,65),cv2.FONT_HERSHEY_SIMPLEX,.6,(255,255,255),2);cv2.putText(frame,f"Color: {color_name}",(20,95),cv2.FONT_HERSHEY_SIMPLEX,.6,self.color,2);cv2.circle(frame,(500,90),18,self.color,-1);cv2.circle(frame,(500,90),18,(255,255,255),2);cv2.putText(frame,f"Brush: {self.brush_thickness}px",(20,125),cv2.FONT_HERSHEY_SIMPLEX,.5,(200,200,200),1);cv2.putText(frame,f"Eraser: {self.eraser_thickness}px",(150,125),cv2.FONT_HERSHEY_SIMPLEX,.5,(200,200,200),1);left_confidence=self.left_hand.get('gesture_confidence',0);right_confidence=self.right_hand.get('gesture_confidence',0);left_timeout=time.time()-self.left_hand['last_active_time']>self.hand_timeout_threshold;right_timeout=time.time()-self.right_hand['last_active_time']>self.hand_timeout_threshold;left_status=f"Left: ACTIVE"if not left_timeout else'Left: READY';right_status=f"Right: ACTIVE"if not right_timeout else'Right: READY';left_color=(0,255,0)if not left_timeout else(100,100,100);right_color=(0,255,0)if not right_timeout else(100,100,100);cv2.putText(frame,left_status,(20,155),cv2.FONT_HERSHEY_SIMPLEX,.5,left_color,1);cv2.putText(frame,right_status,(20,175),cv2.FONT_HERSHEY_SIMPLEX,.5,right_color,1);instructions=['LEFT: Index=Brush Middle=Spray Ring=BrushSize Pinky=Fill','RIGHT: Index=Draw Middle=Erase Pinky=Color','Keys: Z=Undo Y=Redo C=Clear S=Save T=Tool Q=Quit','+/- = Brush Size  [/] = Eraser Size']
		for(i,instruction)in enumerate(instructions):cv2.putText(frame,instruction,(20,200+i*20),cv2.FONT_HERSHEY_SIMPLEX,.4,(200,200,200),1)
	def draw_advanced_gesture_feedback(self,hand_landmarks,gesture,position,hand_type):
		hand=self.left_hand if hand_type=='left'else self.right_hand;confidence=hand.get('gesture_confidence',.5)
		if hand_type=='left':base_color=255,200,0
		else:base_color=200,255,0
		confidence_color=int(base_color[0]*confidence),int(base_color[1]*confidence),int(base_color[2]);wrist=self.get_landmark_coords(hand_landmarks,self.mp_hands.HandLandmark.WRIST)
		if wrist:
			wrist_canvas=self.map_to_canvas(wrist)
			if wrist_canvas:
				wrist_int=int(wrist_canvas[0]),int(wrist_canvas[1]);label='LEFT HAND (TOOLS)'if hand_type=='left'else'RIGHT HAND (DRAWING)';label_color=(255,150,150)if hand_type=='left'else(150,150,255);cv2.putText(self.display_frame,label,(wrist_int[0]-60,wrist_int[1]-20),cv2.FONT_HERSHEY_SIMPLEX,.7,label_color,2)
				if hand_type=='left':tool_info=f"Tool: {self.drawing_tools[self.current_tool].upper()}";cv2.putText(self.display_frame,tool_info,(wrist_int[0]-30,wrist_int[1]-45),cv2.FONT_HERSHEY_SIMPLEX,.6,(255,255,0),2)
				else:stability_info=f"Conf: {confidence:.2f}";cv2.putText(self.display_frame,stability_info,(wrist_int[0]-25,wrist_int[1]-45),cv2.FONT_HERSHEY_SIMPLEX,.5,confidence_color,2)
				vx,vy=hand['velocity'];speed=math.sqrt(vx**2+vy**2)
				if speed>10:arrow_end=int(wrist_canvas[0]+vx*.1),int(wrist_canvas[1]+vy*.1);cv2.arrowedLine(self.display_frame,wrist_int,arrow_end,(0,255,255),2)
		if gesture=='drawing'and position:
			pos_int=int(position[0]),int(position[1])
			if self.current_tool==0:cv2.circle(self.display_frame,pos_int,self.brush_thickness//2+2,(255,255,255),2);cv2.circle(self.display_frame,pos_int,self.brush_thickness//2,self.color,-1)
			elif self.current_tool==1:cv2.circle(self.display_frame,pos_int,self.spray_radius,(255,255,255),2);cv2.circle(self.display_frame,pos_int,3,self.color,-1)
			elif self.current_tool==2:cv2.circle(self.display_frame,pos_int,8,(255,255,255),2);cv2.circle(self.display_frame,pos_int,6,(255,0,255),-1)
		elif gesture=='erasing'and position:pos_int=int(position[0]),int(position[1]);cv2.circle(self.display_frame,pos_int,self.eraser_thickness//2+2,(255,255,255),2);cv2.circle(self.display_frame,pos_int,self.eraser_thickness//2,(255,0,0),-1)
	def run(self):
		cv2.namedWindow('Hand Gesture WHITEBOARD',cv2.WINDOW_NORMAL);cv2.setWindowProperty('Hand Gesture WHITEBOARD',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN);print('Starting Hand Gesture Whiteboard...')
		try:
			while True:
				ret,self.frame=self.cap.read()
				if not ret:break
				self.frame=cv2.flip(self.frame,1);self.left_hand['active']=False;self.right_hand['active']=False;self.update_performance_metrics();self.check_hand_timeouts();rgb_frame=cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB);results=self.hands.process(rgb_frame);self.display_frame=self.canvas.copy();left_gesture='none';right_gesture='none'
				if results.multi_hand_landmarks:
					for(hand_index,hand_landmarks)in enumerate(results.multi_hand_landmarks):
						hand_label='Right'
						if results.multi_handedness:hand_label=results.multi_handedness[hand_index].classification[0].label
						self.mp_draw.draw_landmarks(self.display_frame,hand_landmarks,self.mp_hands.HAND_CONNECTIONS,self.mp_draw.DrawingSpec(color=(0,255,0),thickness=2,circle_radius=3),self.mp_draw.DrawingSpec(color=(255,0,0),thickness=2))
						if hand_label=='Left':gesture,position=self.process_left_hand_tools(hand_landmarks);left_gesture=gesture
						else:gesture,position=self.process_right_hand_gestures(hand_landmarks);right_gesture=gesture
						self.draw_advanced_gesture_feedback(hand_landmarks,gesture,position,hand_label.lower())
				for gesture in self.gesture_cooldowns:
					if self.gesture_cooldowns[gesture]>0:self.gesture_cooldowns[gesture]-=1
				self.draw_interface(self.display_frame);cv2.imshow('Hand Gesture Whiteboard',self.display_frame);key=cv2.waitKey(1)&255
				if key==ord('q'):break
				elif key==ord('c'):self.save_state();self.canvas=np.ones((self.canvas_height,self.canvas_width,3),dtype=np.uint8)*255;print('Canvas cleared')
				elif key==ord('s'):timestamp=datetime.now().strftime('%Y%m%d_%H%M%S');filename=f"saved_drawings/drawing_{timestamp}.png";cv2.imwrite(filename,self.canvas);print(f"Drawing saved as {filename}")
				elif key==ord('z'):self.undo()
				elif key==ord('y'):self.redo()
				elif key==ord('t'):self.current_tool=(self.current_tool+1)%len(self.drawing_tools);print(f"Tool changed to: {self.drawing_tools[self.current_tool]}")
				elif key==ord('+')or key==ord('='):self.current_brush_size=min(self.current_brush_size+1,len(self.brush_sizes)-1);self.brush_thickness=self.brush_sizes[self.current_brush_size];print(f"Brush size: {self.brush_thickness}px")
				elif key==ord('-'):self.current_brush_size=max(self.current_brush_size-1,0);self.brush_thickness=self.brush_sizes[self.current_brush_size];print(f"Brush size: {self.brush_thickness}px")
				elif key==ord(']'):self.current_eraser_size=min(self.current_eraser_size+1,len(self.eraser_sizes)-1);self.eraser_thickness=self.eraser_sizes[self.current_eraser_size];print(f"Eraser size: {self.eraser_thickness}px")
				elif key==ord('['):self.current_eraser_size=max(self.current_eraser_size-1,0);self.eraser_thickness=self.eraser_sizes[self.current_eraser_size];print(f"Eraser size: {self.eraser_thickness}px")
		except Exception as e:print(f"Error in main loop: {e}");traceback.print_exc()
		finally:self.cap.release();cv2.destroyAllWindows();print('Hand Gesture Whiteboard closed')
if __name__=='__main__':
	try:app=PerfectHandWhiteboard();app.run()
	except Exception as e:print(f"Failed to start application: {e}");traceback.print_exc()