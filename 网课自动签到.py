import os
def unzip(zip_name, file_folder_path):
	if os.path.isdir(file_folder_path):
		pass
	else:
		import zipfile
		zip_file = zipfile.ZipFile(zip_name)
		os.mkdir(file_folder_path)
		i = 1
		for name in zip_file.namelist():
			print( "[{}/{}][unzip]{}...".format(i, len(zip_file.namelist()), name) )
			zip_file.extract(name, file_folder_path)
			i += 1
		zip_file.close()

def init():
	print("正在初始化...\n")
	#
	print("(1/3)加载资源文件...")
	unzip("./resources.zip", "./AutoSignUp")
	print("Finished!\n")
	#
	print("(2/3)加载AI组件...")
	unzip("./AutoSignUp/Lib/site-packages/cv2.zip", "./AutoSignUp/Lib/site-packages/cv2")
	print("Finished!\n")
	#
	print("(3/3)加载运算组件...")
	unzip("./AutoSignUp/Lib/site-packages/numpy.zip", "./AutoSignUp/Lib/site-packages/numpy")
	print("Finished!\n")
	#

def show():
	print("======================================Ca钙帮===========================================")
	print("本软件由昆山中学余绍缘开发，测试阶段，如遇问题请加QQ2264558384，对代码的交流也可以来找我，虽然不一定有空回复...")
	print("由于人工智障比较智障，在未进入无线宝课堂时也可能会错误地识别，造成鼠标乱动...所以请在进入网课前打开本软件，退出网课后关闭本软件...")
	print("其实上述问题换个方法就好了...但是懒")
	input("所以...按下你的回车键，开始吧（勿关闭本窗口，可以最小化）")

def main():
	init()
	show()
	os.system("AutoSignUp\\python.exe AutoSignUp\\main.pyw")

if __name__ == '__main__':
	main()