def fixer(inp):

	# Sao lưu đầu vào
	raw_backup = inp

	try:	# Xử lí chuỗi

		# Nhập thư viện
		from requests.utils import quote
		import re
		
		# Chia dòng
		inp = inp.splitlines()
		# Tạo danh sách đầu ra
		otp = []

		# Xử lí danh sách đầu vào
		for raw in inp:

			# Lấy domain của url
			match1 = re.search(r'(https|http|ssl)(:\/\/)([^\/]+)', raw)
			if match1:
			    domain = match1.group(3)
			else:
			    assert False, 'Domain in URL could not be found'	# Trả về lỗi nếu không thể lấy domain

			# Kiểm tra url đã encode hay chưa
			match2 = re.search(r'%[0-9]+', raw)
			if match2:
				fixed = re.sub('%[0-9]+', "", domain)	# Nếu có, loại bỏ trực tiếp %<number>
			else:
				encoded = quote(domain, safe=':/?&=')	# Nếu không, encode và loại bỏ %<number>
				fixed = re.sub('%[0-9]+', "", encoded)

			# Thay dấu khoảng cách bằng dấu chấm nếu sau khi xử lí không có dấu ngăn cách giữa domain và top-level domain
			fixed = re.sub(' +', ".", fixed)
			
			# Thay thế domain cũ bằng domain mới
			fixed = raw.replace(domain, fixed)

			# Thêm mục vào danh sách đầu ra
			otp.append(fixed)

		# Nối các dòng
		otp = '\n'.join(otp)

		# Trả về kết quả
		return otp

	except:	# Nếu xảy ra lỗi, trả về giá trị ban đầu
		return raw_backup

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

	# Thoát vòng lặp bằng phím tuỳ chỉnh
	# Đặt thời gian delay giữa các vòng lặp
	time.sleep(delay)

	if keyboard.is_pressed('esc'):
		break
		
# Kết thúc chương trình
