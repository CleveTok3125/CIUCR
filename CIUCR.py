def fixer(raw):

	# Sao lưu đầu vào
	raw_backup = raw

	#try:	# Xử lí chuỗi

	# Nhập thư viện
	from requests.utils import quote
	import re
	
	def url_check(inp):
		inp = quote(inp)
		if re.search(r'%[0-9]+', inp):
			return False
		else:
			return True

	def cases(inp):	# Danh sách các trường hợp
		return [
		inp.replace(' ', '.'),
		inp.replace('%20', '.'),
		re.sub('(%[0-9]+)(?:[^.]+)(%[0-9]+)', ".", inp), 
		re.sub('(%[0-9]+)(?:[^.]+)(%[0-9]+)', "", inp),
		re.sub('%[0-9]+', "", inp),
		quote(inp)
		]

	# Lấy domain của url
	match1 = re.search(r'(https|http|ssl)(:\/\/)([^\/]+)', raw)
	if match1:
		domain = match1.group(3)
		fixed = domain

		lst0 = cases(domain)
		double_check = True
		lst1 = []

		for i in lst0:
			if url_check(i):
				fixed = i
				double_check = False
				break
			else:
				lst1.append(i)

		if double_check:
			for i in lst1:
				lst2 = cases(i)
				for j in lst2:
					if url_check(j):
						fixed = j
						break

		# Thay thế domain cũ bằng domain mới
		fixed = raw.replace(domain, fixed)

	else:
		assert False, 'Domain in URL could not be found'	# Trả về lỗi nếu không thể lấy domain
	
	return fixed

	#except:	# Nếu xảy ra lỗi, trả về giá trị ban đầu
	#	return raw_backup

# Nhập thư viện
import win32clipboard, time, os, keyboard
from time import gmtime, strftime

# Interface
print('Clipboard Illegal URL Characters Remover\n')
print('Press Enter to start...')
user_input = input('')
if user_input == 'help':
	delay = 1
	input('	help - show help\n	<integer> - setinterval (default: 1)\n	Press ESC to exit\nPress any key to continue...')
elif user_input.isdigit():
	delay = int(user_input)
else:
	delay = 1
os.system('cls')

# Dùng vòng lập để xử lí theo thời gian thực
while True:


	# Mở Clipboard
	win32clipboard.OpenClipboard()

	# Đặt biến
	data1 = win32clipboard.GetClipboardData()
	data2 = fixer(data1)

	# Nếu dữ liệu từ Clipboard khác dữ liệu đã xử lí:
	if data1 != data2:
		
		# Đặt Clipboard là dữ liệu đã xử lí
		win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, data2)

		# Log trên màn hình
		print("["+strftime("%H:%M:%S", gmtime())+"]\nFrom:\n"+data1+"\nTo:\n"+win32clipboard.GetClipboardData())

	# Đóng Clipboard
	win32clipboard.CloseClipboard()

	# Đặt thời gian delay giữa các vòng lặp
	time.sleep(delay)
	
	# Thoát vòng lặp bằng phím tuỳ chỉnh
	if keyboard.is_pressed('esc'):
		break
		
# Kết thúc chương trình
