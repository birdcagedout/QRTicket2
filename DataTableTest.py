import re
import time
from datetime import *
import flet as ft
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
QR_YEAR = str(date.today().year) if date.today().month != 1 else str(date.today().year-1)																		# 대상년   =========>  실행시 기준(1월이면 이전 년 12월)
QR_MONTH = "12" if date.today().month == 1 else str(date.today().month) if date.today().month == 12 and date.today().day > 15 else str(date.today().month-1)	# 대상월   =========>  실행시 기준 이전 달(12월 말이면 그해 12월)

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



def main(page: ft.Page):
	page.title = "QR식권 처리기"
	page.window_width = 1938
	page.window_height = 1050
	page.window_resizable = False
	page.window_maximizable = False
	page.window_minimizable = False
	#page.window_maximized = True
	page.theme_mode = ft.ThemeMode.DARK
	page.window_visible = True
	page.window_center()
	page.scroll = ft.ScrollMode.AUTO
	# print(page.width, page.height)
	

	# 식당 리스트(19)
	affil_list = ["노코(NOKO)", "어장촌생선구이", "횡성목장", "전주콩나루", "옛날칼국수", "칠리사이공", "도나한우", "북경(北京)", "명문식당", "일성스시", "새싹비빔밥", "파운드커피", "구내식당", '어돈', '신의주찹쌀순대', '마시차이나', '순두부와빈대떡', '노원437', '명품장어구이']


	# 교통행정팀: 직원명단(11, 과장님 포함)
	TA_code_list = ["4060",   "4040",   "4038",   "4036",   "4034",   "4062",   "4039",   "4048",   "4037",   "4041",   "4035"  ]
	TA_name_list = ["조병주", "정태영", "김주영", "최소영", "김태범", "하정희", "김윤정", "방상호", "손효석", "최민규", "이수지"]

	# 운수지도팀: 직원명단(6)
	TG_code_list = ["4047",   "4043",   "4045",   "4056",   "4055", "4044"]
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
	MA_color_list = get_hex_colors(len(affil_list))

	
	
	# 파일 다이얼로그 파일선택 결과 ==> ft.FilePickerResultEvent
	# 열기: e.files = 파일(ft.FilePickerFile객체) 리스트
	# 취소: e.files = None
	def pick_files_result(e: ft.FilePickerResultEvent):
		# 취소한 경우
		if e.files == None:
			pass
		# 정상 선택한 경우
		else:
			selected_files.value = list(map(lambda f: f.path, e.files))		# ['C:\\Dev\\QRticket\\202301\\IMG_7158.MOV', ... 'C:\\Dev\\QRticket\\202301\\IMG_7160.MOV']

	
	
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


	
	page.add(
		r2_processing_table,
		ft.Divider(height=9, thickness=3),
		r3_result_table,
		selected_files		# 맨 마지막에 넣어야 공백 없음
	)

	# 다이얼로그 띄우기
	dlg_file_open.pick_files(dialog_title="식권 동영상 파일 열기" , file_type=ft.FilePickerFileType.VIDEO, allow_multiple=True)

	for i in range(len(affil_list)):
		print(r2_processing_table.rows[i].cells[1].content.value)
		time.sleep(1)
		r2_processing_table.rows[i].cells[1].content.value += 0.1
		page.update()



ft.app(target=main, view=ft.FLET_APP_HIDDEN)