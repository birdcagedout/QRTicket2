import flet as ft
from distinctipy import distinctipy as dc


def main(page: ft.Page):
	page.title = "QR식권 처리기"
	page.window_width = 1930
	page.window_height = 1050
	page.window_resizable = False
	page.window_maximizable = False
	page.window_minimizable = False
	#page.window_maximized = True
	page.theme_mode = ft.ThemeMode.DARK
	page.window_visible = True
	page.window_center()
	page.scroll = ft.ScrollMode.AUTO
	




	affil_list = ["노코(NOKO)", "어장촌생선구이", "횡성목장", "전주콩나루", "옛날칼국수", "칠리사이공", "도나한우", "북경(北京)", "명문식당", "일성스시", "새싹비빔밥", "파운드커피", "구내식당", '어돈', '신의주찹쌀순대', '마시차이나', '순두부와빈대떡', '노원437', '명품장어구이']


	# 교통행정팀: 직원명단(11, 과장님 포함)
	TA_code_list = ["4060",   "4040",   "4038",   "4036",   "4034",   "4062",   "4039",   "4048",   "4037",   "4041",   "4035"  ]
	TA_name_list = ["조병주", "정태영", "김주영", "최소영", "김태범", "하정희", "김윤정", "방상호", "손효석", "최민규", "이수지"]

	# 운수지도팀: 직원명단(6)
	TG_code_list = ["4047",   "4043",   "4045",   "4056",   "4055", "4044"]
	TG_name_list = ["윤정웅", "백주호", "김미섭", "김필상", "김영훈", "심승근"]
	
	# 등록팀: 직원명단(9)
	VR_code_list =  ["4080",    "4076",    "4079",    "4069",    "4078",    "4071",    "4068",    "4075",    "4077"   ]
	VR_name_list =  ["정미경",  "정성욱",  "강선임",  "모수지",  "송현우",  "신이은",  "이지은",  "김형수",  "김재형" ]

	# 자동차관리팀: 직원명단(6)
	VM_code_list = ["4052",   "4051",   "4054",   "4053",   "4050",   "4049"]
	VM_name_list = ["성금택", "홍종수", "우상민", "홍경옥", "신완택", "배홍길"]


	# 통합
	code_list = TA_code_list + TG_code_list + VR_code_list + VM_code_list
	name_list = TA_name_list + TG_name_list + VR_name_list + VM_name_list

	

	# 2. QR 검증 processing Table
	r2_processing_table = ft.DataTable(
		border=ft.border.all(2, ft.colors.LIGHT_GREEN_300),
		#heading_row_height=50,
		#data_row_height = 40,
		#column_spacing=10,

		columns=[
			ft.DataColumn(ft.Text("식당 이름", weight=ft.FontWeight.W_800)),
			ft.DataColumn(ft.Text("진행 상황", weight=ft.FontWeight.W_800)),
			ft.DataColumn(ft.Text("처리 결과", weight=ft.FontWeight.W_800)),
		],
	)

	# 식당 목록 입력
	for name in affil_list:
		r2_processing_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(f"{name}")), ft.DataCell(ft.ProgressBar(width=1580, height=20, color=(0.0, 1.0, 0.0), expand=True)), ft.DataCell(ft.Text("성공"))]))


	# 3. 결과 Table
	r3_result_table = ft.DataTable(
		border=ft.border.all(2, ft.colors.LIGHT_BLUE_200),
		vertical_lines=ft.border.BorderSide(1, ft.colors.BLACK12),
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
	r3_result_table.column_spacing = 12
	r3_result_table.columns.append(ft.DataColumn(ft.Text("식당 이름 ", weight=ft.FontWeight.BOLD)))
	for name in name_list:
		r3_result_table.columns.append(ft.DataColumn(ft.Text(f"{name}")))


	page.add(
		r2_processing_table,
		ft.Divider(height=9, thickness=3),
		r3_result_table
	)

	print(page.width, page.height)
	print(r2_processing_table)

ft.app(target=main, view=ft.FLET_APP_HIDDEN)