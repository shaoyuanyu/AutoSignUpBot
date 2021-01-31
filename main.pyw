#余绍缘
#2021/1/31

from win32gui import GetDesktopWindow, GetWindowDC, DeleteObject
from win32ui import CreateDCFromHandle, CreateBitmap
from win32api import mouse_event, SetCursorPos
from win32con import DESKTOPHORZRES, DESKTOPVERTRES, SRCCOPY, MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP # win常量
# win32库

from cv2 import imread, cvtColor, matchTemplate, minMaxLoc
from cv2 import COLOR_BGR2GRAY, TM_SQDIFF_NORMED
# OpenCV

from numpy import where as np_where
# numpy.where()

from time import sleep
# time.sleep()

from sys import exit
# sys.exit()

import threading
#

#SHOTCUTPATH = "./resourceFiles/screenshot/screenshot.bmp" # 截图保存路径（相对）
#SHOTCUTPATH = "./resourceFiles/screenshot.bmp" # 截图保存路径（相对） # 测试用
SHOTCUTPATH = "C://screenshot.bmp"
STDIMGPATH = "./resourceFiles/standard_img.png" # 匹配模板路径（相对）
running = True

def get_dpi(): # 获取屏幕实际分辨率（此方法可避免因“缩放布局”导致的分辨率误差）和缩放倍率
	from win32gui import GetDC
	from win32print import GetDeviceCaps
	from win32api import GetSystemMetrics
	hDC = GetDC(0)	
	#
	horzes = GetDeviceCaps(hDC, DESKTOPHORZRES)
	# 横向分辨率
	vertres = GetDeviceCaps(hDC, DESKTOPVERTRES)
	# 纵向分辨率
	scaling = horzes/GetSystemMetrics(0)
	# 缩放比例

	return (horzes, vertres), scaling


def screen_shotcut(dpi): # 截图
	hdesktop = GetDesktopWindow()
	# 获取桌面
	width = dpi[0]
	height = dpi[1]
	#print(width, height)
	# 分辨率适应
	desktop_dc = GetWindowDC(hdesktop)
	img_dc = CreateDCFromHandle(desktop_dc)
	# 创建设备描述表
	mem_dc = img_dc.CreateCompatibleDC()
	# 创建一个内存设备描述表
	screenshot = CreateBitmap()
	screenshot.CreateCompatibleBitmap(img_dc, width, height)
	mem_dc.SelectObject(screenshot)
	# 创建位图对象
	mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), SRCCOPY)
	# 截图至内存设备描述表
	screenshot.SaveBitmapFile(mem_dc, SHOTCUTPATH)
	# 将截图保存到文件中
	mem_dc.DeleteDC()
	DeleteObject(screenshot.GetHandle())
	# 内存释放


def math_test():
	THRESHOLDVALUE = 0.02
	# 常量-相似度阈值（在TM_SQDIFF_NORMED模式下，最好为0，最差为1）
	img_rgb = imread(SHOTCUTPATH)
	img_gray = cvtColor(img_rgb, COLOR_BGR2GRAY) # 图片灰度化
	template = imread(STDIMGPATH, 0) # 模板
	width, height = template.shape[::-1]
	# 读入原图和模板
	result = matchTemplate(img_gray, template, TM_SQDIFF_NORMED)
	# 模版匹配
	loc = np_where( result <= THRESHOLDVALUE )
	if loc[0].size>0 and loc[1].size>0: # 匹配成功
		#print(loc)
		#print("ok")
		min_val, max_val, min_loc, max_loc = minMaxLoc(result)
		start_point = min_loc
		end_point = (start_point[0]+width, start_point[1]+height)
		# 识别区域的起始点（左上角）和终止点（右下角）

		"""在屏幕上圈出匹配成功的区域
		import cv2
		cv2.rectangle(img_rgb, start_point, end_point, (7,249,151), 2)   
		cv2.imshow('Detected',img_rgb)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		"""

		#print("start:{}\nend:{}".format(start_point, end_point))
		return list(start_point)
	else:
		#print("404")
		return False

def slide(start_location, scaling):
	LENGTH = int(275/scaling)
	# 常量-滑动长度
	SetCursorPos( start_location )
	# 设置鼠标焦距
	mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
	# 左键按下
	for right_move in range(0, LENGTH):
		loc = ( start_location[0]+right_move, start_location[1] ) 
		SetCursorPos( loc )
		# 设置鼠标焦距
		sleep(0.002)
	# 右移
	mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
	# 左键松开

def main():
	global running
	dpi, scaling = get_dpi()
	while running:
		screen_shotcut(dpi)
		location = math_test()
		# 定位弹窗
		#print(location)
		if location: # 匹配成功（识别到弹窗）
			location[0] = int( (location[0]+35)/scaling ) 
			location[1] = int( (location[1]+123)/scaling ) 
			# 将定位精确到滑块
			slide(location, scaling)
		sleep(5)

def run():
	t=threading.Thread(target=main)
	t.start()

def quit(top):
	global running
	running = False
	top.quit()
	exit()

def ui():
	import tkinter
	top = tkinter.Tk()
	top.title("自动签到 - 余绍缘 - Ca")
	top.geometry('300x100')
	start_button = tkinter.Button(top, text = "开始", command = run)
	exit_button = tkinter.Button(top, text = "结束", command = lambda:quit(top))
	start_button.pack()
	exit_button.pack()
	top.mainloop()

if __name__ == '__main__':
	ui()