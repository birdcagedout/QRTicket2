import flet as ft

def main(page: ft.Page):
	page.title = "QR식권 처리기"
	page.window_width = 1000
	page.window_height = 1000
	page.window_resizable = False
	page.window_maximizable = False
	page.window_center()
	page.window_visible = True
	
	affil_list = ["노코(NOKO)", "어장촌생선구이", "횡성목장", "전주콩나루", "옛날칼국수", "칠리사이공", "도나한우", "북경(北京)", "명문식당", "일성스시", "새싹비빔밥", "파운드커피", "구내식당"]

	# 2. QR 검증 processing Table
	r2_processing_table = ft.DataTable(
		border=ft.border.all(2, ft.colors.LIGHT_GREEN_300),
		heading_row_height=50,
		data_row_height = 40,
		#column_spacing=10,
		columns=[
			ft.DataColumn(ft.Text("식당 이름", weight=ft.FontWeight.W_800)),
			ft.DataColumn(ft.Text("진행 상황", weight=ft.FontWeight.W_800)),
			ft.DataColumn(ft.Text("처리 결과", weight=ft.FontWeight.W_800)),
		],
		#rows=[
		#	ft.DataRow(
		#		cells=[
					#ft.DataCell(ft.Text("John")),
					#ft.DataCell(ft.Text("Smith")),
		#		],
		#	),
		#	ft.DataRow(
		#		cells=[
					#ft.DataCell(ft.Text("Jack")),
					#ft.DataCell(ft.Text("Brown")),
		#		],
		#	),
		#],
	)

	# 식당 목록 입력
	for name in affil_list:
		r2_processing_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(f"{name}")), ft.DataCell(ft.ProgressBar(width=650, expand=True)), ft.DataCell(ft.Text("성공"))]))


	# 3. 결과 Table
	r3_result_table = ft.DataTable(
		border=ft.border.all(2, ft.colors.LIGHT_BLUE_200),
		columns=[
			ft.DataColumn(ft.Text("First name", weight=ft.FontWeight.BOLD)),
			ft.DataColumn(ft.Text("Last name", weight=ft.FontWeight.BOLD)),
			ft.DataColumn(ft.Text("Age", weight=ft.FontWeight.BOLD), numeric=True),
		],
		rows=[
			ft.DataRow(
				cells=[
					ft.DataCell(ft.Text("John")),
					ft.DataCell(ft.Text("Smith")),
					ft.DataCell(ft.Text("43")),
				],
			),
			ft.DataRow(
				cells=[
					ft.DataCell(ft.Text("Jack")),
					ft.DataCell(ft.Text("Brown")),
					ft.DataCell(ft.Text("19")),
				],
			),
			ft.DataRow(
				cells=[
					ft.DataCell(ft.Text("Alice")),
					ft.DataCell(ft.Text("Wong")),
					ft.DataCell(ft.Text("25")),
				],
			),
		],
	)
	
	page.add(
		r2_processing_table,
		ft.Divider(height=9, thickness=3),
		r3_result_table
	)

	print(page.width, page.height)
	print(r2_processing_table)

ft.app(target=main, view=ft.FLET_APP_HIDDEN)