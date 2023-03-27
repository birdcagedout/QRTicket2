import re
import os
import cv2
import sys
import time
import flet as ft
import pandas as pd
import datetime as dt
import threading
from pyzbar.pyzbar import *
from dataclasses import dataclass
from typing import List, Set, Dict
from distinctipy import distinctipy as dtp

#######################################################################################################################################################################
# distict color 생성기
# get_colors(N) ==> (R: float, G: float, B: float) ==> '#FFCCAA' 형태로 재포맷
def get_hex_colors(num_of_colors):
	colors = dtp.get_colors(num_of_colors, pastel_factor=0.6)
	hex_colors = []
	for color in colors:
		rgb = (round(color[0] * 255), round(color[1] * 255), round(color[2] * 255))
		hex = '%02X%02X%02X' % rgb
		hex_colors.append('#' + hex)
	return hex_colors


#######################################################################################################################################################################
# <QR Format>
# 식당: NWTAVR-MA-202112-식당이름
# 직원: NWTAVR-MS-202112-4077-01
QR_HEADER = "NWTA(TA|TG|VR|VM)"				# 노원구청 교통행정과 TA(교통행정팀) / TG(운수지도팀) / VR(자동차등록팀) / VM(자동차관리팀) ==> 헤더부분이 내 QR인지 식별자 역할
QR_CLASS_MA = "MA"							# 식당 = Member of Affiliation
QR_CLASS_MS = "MS"							# 직원 = Member of Staff
QR_YEAR = str(dt.date.today().year) if dt.date.today().month != 1 else str(dt.date.today().year-1)																		# 대상년   =========>  실행시 기준(1월이면 이전 년 12월)
QR_MONTH = "12" if dt.date.today().month == 1 else str(dt.date.today().month) if dt.date.today().month == 12 and dt.date.today().day > 15 else str(dt.date.today().month-1)	# 대상월   =========>  실행시 기준 이전 달(12월 말이면 그해 12월)

QR_YYYYMM = QR_YEAR + QR_MONTH				# "202302"
QR_SN = ["0"+str(i) if i < 10 else str(i) for i in range(1, 21)]    # ["01", "02", ... "19", "20"]


#######################################################################################################################################################################
# 교통행정과 모든 팀 포함한 정규식
# NWTA(TA|TG|VR|VM)-MA-202302-[0-9]{4}-[0-9]{2}
MA_pattern = re.compile(QR_HEADER + "-" + QR_CLASS_MA + "-" + QR_YYYYMM + "-" + ".+")							# NWTAVR-MA-202112-노코(NOKO)
MS_pattern = re.compile(QR_HEADER + "-" + QR_CLASS_MS + "-" + QR_YYYYMM + "-" + "[0-9]{4}" + "-" + "[0-9]{2}")	# NWTAVR-MS-202112-4077-01



#######################################################################################################################################################################
# 인풋 아웃풋 폴더 설정
HOME_PATH = "C:/QRticket/"
MOV_PATH = HOME_PATH + QR_YYYYMM + "/"
OUT_PATH = HOME_PATH + QR_YYYYMM + "_Result" + "/"
os.makedirs(OUT_PATH, exist_ok=True)


#######################################################################################################################################################################
# 식당 리스트(19)
#				0				1				2				3			4			5				6			7			8			9			10				11			12			13			14				15				16				17			18			
affil_list = ["노코(NOKO)", "어장촌생선구이", "횡성목장", "전주콩나루", "옛날칼국수", "칠리사이공", "도나한우", "북경(北京)", "명문식당", "일성스시", "새싹비빔밥", "파운드커피", "구내식당", '어돈', '신의주찹쌀순대', '마시차이나', '순두부와빈대떡', '노원437', '명품장어구이']


# 교통행정팀: 직원명단(11, 과장님 포함)
TA_code_list = ["4060",   "4040",   "4038",   "4036",   "4034",   "4062",   "4039",   "4048",   "4037",   "4041",   "4035"  ]
TA_name_list = ["조병주", "정태영", "김주영", "최소영", "김태범", "하정희", "김윤정", "방상호", "손효석", "최민규", "이수지"]

# 운수지도팀: 직원명단(6)
TG_code_list = ["4047",   "4043",   "4045",   "4056",   "4055",   "4044"]
TG_name_list = ["윤정웅", "백주호", "김미섭", "김필상", "김영훈", "심승근"]

# 등록팀: 직원명단(9 + 1 = 10명)
VR_code_list =  ["4080",    "4076",    "4079",    "4069",    "4078",    "4071",    "4068",    "4075",    "4077",   "4000"]
VR_name_list =  ["정미경",  "정성욱",  "강선임",  "모수지",  "송현우",  "신이은",  "이지은",  "김형수",  "김재형", "한정민" ]

# 자동차관리팀: 직원명단(6)
VM_code_list = ["4052",   "4051",   "4054",   "4053",   "4050",   "4049"]
VM_name_list = ["성금택", "홍종수", "우상민", "홍경옥", "신완택", "배홍길"]


# 통합: 32 + 1 = 33명
code_list = TA_code_list + TG_code_list + VR_code_list + VM_code_list
name_list = TA_name_list + TG_name_list + VR_name_list + VM_name_list


# 직원 color
color_list = get_hex_colors(len(code_list))

name_by_code = {code_list[i] : name_list[i] for i in range(len(code_list))}			# {'4080':'전현호','4076':'정성욱',...,'4077':'김재형'}
color_by_code = {code_list[j] : color_list[j] for j in range(len(code_list))}		# {'4080':'#E32636','4076': '#FFA500',...,'4077':'#119617'}

# 식당 color
MA_color_list = get_hex_colors(len(affil_list))

# print(code_list)
# print(name_list)
# print(color_list)
# ['4060', '4040', '4038', '4036', '4034', '4062', '4039', '4048', '4037', '4041', '4035', '4047', '4043', '4045', '4056', '4055', '4044', '4080', '4076', '4079', '4069', '4078', '4071', '4068', '4075', '4077', '4000', '4052', '4051', '4054', '4053', '4050', '4049']
# ['조병주', '정태영', '김주영', '최소영', '김태범', '하정희', '김윤정', '방상호', '손효석', '최민규', '이수지', '윤정웅', '백주호', '김미섭', '김필상', '김영훈', '심승근', '정미경', '정성욱', '강선임', '모수지', '송현우', '신이은', '이지은', '김형수', '김재형', '한정민', '성금택', '홍종수', '우상민', '홍경옥', '신완택', '배홍길']
# ['#7762B7', '#6CF876', '#FB9B69', '#6ED4FE', '#ED69FD', '#FCFF7A', '#699E61', '#C0C3BB', '#B16862', '#9795F8', '#B7CF62', '#69BCAD', '#F66399', '#FFBAFA', '#A1FECE', '#BD76C0', '#6068FB', '#A49A91', '#646670', '#FCD1A8', '#C1DFFE', '#FE94B9', '#A663FE', '#CAF0A0', '#6296D5', '#66F5BE', '#97DB92', '#DC94F0', '#ADFA66', '#EBC76D', '#60949C', '#67C772', '#96C1E1']




#######################################################################################################################################################################
# 전체 QR 검출된 테이터 저장할 변수
lock = threading.Lock()

# 원래 이걸 사용하려고 했으나 ==> ft.ProgressBar의 값이 0 ~ 1만 있으면 되므로 그냥 list[int]를 사용하기로 했다
# @dataclass
# class ProgressData:
# 	total_frames: int = 0
# 	processed_frames: int = 0
# progress_dict: Dict[str, ProgressData] = {affil_list[k] : ProgressData() for k in range(len(affil_list))}		# typing으로 타입힌트

progress_dict: Dict[str, float] = {affil_list[k] : 0.0 for k in range(len(affil_list))}								# typing으로 타입힌트




# 쓰레드에서 이 변수들에 접근할 때 lock 사용해야 함
# lock.acquire() # 다른 쓰레드의 접근을 금지
# 여기서 공유데이터 쓰기 작업    
# lock.release() # lock 해제






#######################################################################################################################################################################
# 동영상 파일 하나씩 QR검출 돌릴 쓰레드
class QRDetectorThread(threading.Thread):
	
	# 초기화
	def __init__(self, movie=None, threadID=None):
		super(QRDetectorThread, self).__init__(daemon=True)
		
		# 동영상 파일 정보
		self.movie = movie											# 입력 MOV 파일
		self.threadID = threadID									# 쓰레드 ID
		self.width = int(movie.get(cv2.CAP_PROP_FRAME_WIDTH))		# 이번 MOV 파일의 width
		self.height = int(movie.get(cv2.CAP_PROP_FRAME_HEIGHT))		# 이번 MOV 파일의 height
		self.frame_count = int(movie.get(cv2.CAP_PROP_FRAME_COUNT))	# 이번 MOV 파일의 frame 총수
		self.fps = movie.get(cv2.CAP_PROP_FPS)						# 이번 MOV 파일의 frame rate
		
		# QR 내용 정보
		# self.detected_MA_set = set()  # 식당QR (중복없음)
		self.final_MA_name = ""			# 최종 식당 이름
		self.detected_MS_set = set()    # 직원QR (중복없음)
		self.final_MS_dict = {}			# 최종 직원 명단 : {"전현호": [1, 4, 5], "정성욱": [2, 10], "박선녕": [],  "신상용": [],  ..., "김재형": [4, 12]}

		# DIVX 코덱으로 avi 파일 생성
		self.fourcc = cv2.VideoWriter_fourcc(*'DIVX')
		self.out = cv2.VideoWriter(f"{OUT_PATH}QR_result_{threadID}.avi", self.fourcc, self.fps, (self.width, self.height))
	
	# 쓰레드 실행
	def run(self):

		# 진행상황 변수 update용 global 선언 
		global progress_dict
		
		# frame 1개씩 읽기
		for frame_index in range(self.frame_count):

			# frame 읽어오지 못한 경우(success = False) ==> 다음 frame으로
			success, frame = self.movie.read()
			if success == False:
				continue

			# frame 1개에서 여러개의 QR 찾기
			QRs_in_frame = decode(frame, symbols=[ZBarSymbol.QRCODE])    # list
			num_of_QR = len(QRs_in_frame)
			# print(f"[전처리 전] 발견된 QR개수: {num_of_QR}")


			# 만약 하나도 발견되지 않았다면 다음 frame
			if num_of_QR == 0:
				# print("QR code not detected")
				continue


			# frame 1개에서 발견한 여러개 QR 중 1개 = eachQR
			for eachQR in QRs_in_frame:

				# QR 형식검증 : MS/MA패턴
				eachQR_data = eachQR.data.decode('utf-8')
				match_result_MA = MA_pattern.match(eachQR_data)
				match_result_MS = MS_pattern.match(eachQR_data)
				
				# QR이 가맹점도 직원도 아닌 경우 ==> 삭제 후 다음 eachQR
				if (match_result_MA is None) and (match_result_MS is None):
					QRs_in_frame.remove(eachQR)    # remove: list에서 index 가장 앞쪽 값 1개만 삭제
					continue
				
				# 식당QR인 경우
				if match_result_MA is not None:
					# self.detected_MA_set.add(match_result_MA.group())
					_header, _ms, _yyyymm, affil_name = eachQR.data.decode('utf-8').split('-')
					color_selected = (0, 0, 255)    # 식당QR은 빨간색
					
					# 최초 검출된 경우
					if self.final_MA_name == "":
						self.final_MA_name = affil_name				
				
				# 직원QR인 경우
				if match_result_MS is not None:
					self.detected_MS_set.add(match_result_MS.group())
					_header, _ms, _yyyymm, code, _sn = eachQR.data.decode('utf-8').split('-')
					color_hex_selected = color_by_code[code]
					color_selected = tuple(int(color_hex_selected[i:i+2], 16) for i in (5, 3, 1))	# HEX 문자열 -> BGR tuple값
				

				# QR 테두리 선그리기 : QR 1개당 polygon 점의 개수(보통 4각형=4개)
				points = len(eachQR.polygon)

				# QR 1개당 경계선 그리기
				for point in range(points):
					next_point = (point+1) % points
					cv2.line(frame, tuple(eachQR.polygon[point]), tuple(eachQR.polygon[next_point]), color_selected, 5)    # (B,G,R), 굵기

				# ========== [안쪽 for loop 내부] frame 1개 중 QR 1개 처리 끝 ==========

			if self.final_MA_name != "":
				lock.acquire() # 다른 쓰레드의 접근 금지
				progress_dict[self.final_MA_name] = (frame_index + 1) / self.frame_count
				lock.release() # lock 해제
			# ========== [안쪽 for loop 종료] frame 1개 중 QR 전체 처리 끝 ==========
			# num_of_QR_preprocessed = len(QRs_in_frame)
			# print("Frame  #{:3}/{:3} 처리 끝    ====>    전처리 전: {:2} \t 전처리 후: {:2}".format(frame_index+1, frame_count, num_of_QR, num_of_QR_preprocessed))

			# frame 1개 처리 끝 ==> 저장
			self.out.write(frame)

		self.out.release()	# 결과 파일 처리 끝
		self.movie.release()	# MOV 파일 읽기 끝
		# ========== [바깥 for loop 종료] MOV 파일의 모든 frame 처리 끝 ==========
		
		
		# ========== 검출된 QR자료 정리 시작 ==========
		# MA_list = list(self.detected_MA_set)
		# MA_list = sorted(MA_list)
		MS_list = list(self.detected_MS_set)
		MS_list = sorted(MS_list)
		
		# 가맹점 QR이 1개도 없으면 오류, 1개뿐이면 최종 저장
		# if len(MA_list) != 1:
		# 	print("[오류] QR 검출된 가맹점이 없거나, 2개 이상입니다.")
		# 	sys.exit(0)
		# else:
		# 	self.final_MA_name = MA_list[0].split('-')[3]		# ['NWTAVR-MA-202112-새싹비빔밥']
		

		# 직원 QR은 하나도 없을 수도 있음 ==> 알림만 표시 (데이터 형태는 유지)
		# if len(MS_list) == 0:
		# 	print(f"[알림] 현재 쓰레드({self.threadID})에서 검출된 직원 QR이 없습니다.")

		# 직원 순서대로 final_MS_dict 초기화 : python 3.7부터 dict = ordered
		for _code in code_list:
			self.final_MS_dict[name_by_code[_code]] = []

		# QR 있는 직원만 final_MS_dict에 SN 채워넣기
		for eachStaff in MS_list:
			_header, _ms, _yyyymm, code, sn = eachStaff.split("-")
			self.final_MS_dict[name_by_code[code]].append(sn)
			
		
		print(f"[쓰레드 종료] ID: {self.threadID:>2}")
		#============================ 쓰레드 run() 처리 끝 ======================================





#######################################################################################################################################################################
# QR검출 진행상황 관리 쓰레드
class QRProgressThread(ft.UserControl):
	def __init__(self, progressbar_list, page: ft.Page):
		super().__init__()

		self.progressbars: List[ft.ProgressBar] = progressbar_list
		self.page: ft.Page = page
		self.done: Dict[str, bool] = {}
		self.running = False

	def did_mount(self):
		self.thread = threading.Thread(target=self.update_timer, args=(), daemon=True)
		self.thread.start()
		self.running = True

	def will_unmount(self):
		self.running = False

	def update_timer(self):
		while self.running == True:
			names = list(progress_dict.keys())
			for i in range(len(names)):
				name = names[i]
				self.progressbars[affil_list.index(name)].value = progress_dict[name]
				print(f"{name}: {progress_dict[name]}")
				self.page.update()

				if progress_dict[name] == 1:
					self.done[name] = True
			
			time.sleep(0.2)

			total = 0
			for j in self.done.values():
				if j == True:
					total += 1
			if total == len(progress_dict):
				break

	def build(self):
		return ft.Container()		# 더미 Control 하나 던져준다








#######################################################################################################################################################################
# main()
def main(page: ft.Page):
	page.title = f"QR식권 처리기: {QR_YEAR}년 {QR_MONTH}월"
	page.window_width = 1938
	page.window_height = 1050
	page.window_resizable = False
	page.window_maximizable = False
	page.window_minimizable = False
	page.theme_mode = ft.ThemeMode.DARK
	page.window_visible = True
	page.window_center()
	page.scroll = ft.ScrollMode.AUTO
	
	QR_workers = []
	QR_manager = None
	

	
	
	# 파일 다이얼로그 파일선택 결과 ==> ft.FilePickerResultEvent
	# 열기: e.files = 파일(ft.FilePickerFile객체) 리스트
	# 취소: e.files = None
	def pick_files_result(e: ft.FilePickerResultEvent):
		# 취소한 경우
		if e.files == None:
			pass
		# 정상 선택한 경우
		else:
			# 동영상 파일 리스트
			selected_files.value = list(map(lambda f: f.path, e.files))		# ['C:\\Dev\\QRticket\\202301\\IMG_7158.MOV', ... 'C:\\Dev\\QRticket\\202301\\IMG_7160.MOV']
			num_of_thread = len(selected_files.value)
			mov = [cv2.VideoCapture(selected_files.value[i]) for i in range(num_of_thread)]    # 동영상 파일 입력 ==> cap 리스트에 저장

			# QR 처리 쓰레드(process_thread) 실행
			# 쓰레드 생성 + 시작
			for i in range(num_of_thread):
				QR_workers.append(QRDetectorThread(mov[i], i))
				QR_workers[i].start()

			# 진행상황 관리 쓰레드(manager_thread) 실행
			progressbar_list = [r2_processing_table.rows[i].cells[1].content for i in range(len(affil_list))]
			QR_manager = QRProgressThread(progressbar_list, page)
			page.add(QR_manager)

			# 결과 datatable 표시

			# 엑셀파일 저장



	
	
	# 파일 열기 다이얼로그
	dlg_file_open = ft.FilePicker(on_result=pick_files_result)
	page.overlay.append(dlg_file_open)

	# 식권 동영상 파일 리스트(selected_files.value)
	selected_files = ft.Text()




	# 2. QR 검출 processing Table
	r2_processing_table = ft.DataTable(
		border=ft.border.all(2, ft.colors.LIGHT_GREEN_300),
		vertical_lines=ft.border.BorderSide(1, ft.colors.WHITE12),
		#heading_row_height=50,
		#data_row_height = 40,
		#heading_row_color=ft.colors.LIGHT_GREEN_400,
		#heading_text_style=ft.TextStyle(size=17, color=ft.colors.LIGHT_BLUE_900),
		column_spacing=30,

		columns=[
			ft.DataColumn(ft.Text("식당 이름", weight=ft.FontWeight.W_800)),
			ft.DataColumn(ft.Text("진행 상황", weight=ft.FontWeight.W_800)),
			ft.DataColumn(ft.Text("처리 결과", weight=ft.FontWeight.W_800)),
		],
	)

	# 식당 목록 입력
	for i, name in enumerate(affil_list):
		r2_processing_table.rows.append(
			ft.DataRow(cells=[
				ft.DataCell(ft.Text(f"{name}")), 
				ft.DataCell(ft.ProgressBar(width=1625, height=20, color=MA_color_list[i], value=0)), 
				ft.DataCell(ft.Text("성공"))
			])
		)
		
	

	# 3. QR 처리 결과 Table
	r3_result_table = ft.DataTable(
		border=ft.border.all(2, ft.colors.LIGHT_BLUE_200),
		vertical_lines=ft.border.BorderSide(1, ft.colors.WHITE12),
		#columns=[],
		#rows=[
		#	ft.DataRow(
		#		cells=[
		#			ft.DataCell(ft.Text("John")),
		#			ft.DataCell(ft.Text("Smith")),
		#			ft.DataCell(ft.Text("43")),
		#		],
		#	),
		#	ft.DataRow(
		#		cells=[
		#			ft.DataCell(ft.Text("Jack")),
		#			ft.DataCell(ft.Text("Brown")),
		#			ft.DataCell(ft.Text("19")),
		#		],
		#	),
		#	ft.DataRow(
		#		cells=[
		#			ft.DataCell(ft.Text("Alice")),
		#			ft.DataCell(ft.Text("Wong")),
		#			ft.DataCell(ft.Text("25")),
		#		],
		#	),
		#],
	)
	
	# 결과 Table 채우기
	# columns = 직원 명단
	r3_result_table.column_spacing = 10.2
	r3_result_table.columns.append(ft.DataColumn(ft.Text("   식당 이름         ", weight=ft.FontWeight.BOLD)))
	for name in name_list:
		r3_result_table.columns.append(ft.DataColumn(ft.Text(f"{name}", size=13)))
	r3_result_table.columns.append(ft.DataColumn(ft.Text("        합계   ")))         


	
	# 위젯 붙이기
	page.add(
		r2_processing_table,
		ft.Divider(height=9, thickness=3),
		r3_result_table,
		selected_files		# 맨 마지막에 넣어야 공백 없음
	)

	# 다이얼로그 띄우기
	dlg_file_open.pick_files(dialog_title="식권 동영상 파일 열기" , file_type=ft.FilePickerFileType.VIDEO, allow_multiple=True)

	
	
	for i in range(len(affil_list)):
		# print(r2_processing_table.rows[i].cells[1].content.value)
		# time.sleep(1)
		# r2_processing_table.rows[i].cells[1].content.value += 0.1
		# page.update()
		print(r2_processing_table.rows[i].cells[0].content.value)



ft.app(target=main, view=ft.FLET_APP_HIDDEN)