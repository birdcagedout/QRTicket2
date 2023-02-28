import flet as ft



VER = "1.0"


WIN_WIDTH = 600
WIN_HEIGHT = 400


def main(page: ft.Page):
	page.title = "QR식권 처리기"
	page.window_width = WIN_WIDTH
	page.window_height = WIN_HEIGHT
	page.window_maximizable = False
	page.window_minimizable = False
	page.window_resizable = False
	page.padding = 15
	page.spacing = 10
	page.theme_mode = ft.ThemeMode.LIGHT
	page.window_center()
	page.window_visible = True
	page.update()
	

	# 파일 다이얼로그 파일선택 결과 ==> ft.FilePickerResultEvent
	# 열기: e.files = 파일(ft.FilePickerFile객체) 리스트
	# 취소: e.files = None
	def pick_files_result(e: ft.FilePickerResultEvent):
		# 취소한 경우
		if e.files == None:
			selected_files.value = "Cancelled!"
		# 정상 선택한 경우
		else:
			#selected_files.value = (", ".join(map(lambda f: f.name, e.files)))
			selected_files.value = list(map(lambda f: f.path, e.files))		
			print(selected_files.value)
			print(len(e.files))
			print(e.files[0].name)
			print(e.files[0].path)
		
		selected_files.update()

	dlg_file_open = ft.FilePicker(on_result=pick_files_result)
	selected_files = ft.Text()

	page.overlay.append(dlg_file_open)

	page.add(
		ft.Row([
				ft.ElevatedButton("파일 열기", icon=ft.icons.UPLOAD_FILE, 
		      					on_click=lambda _: dlg_file_open.pick_files(dialog_title="식권 동영상 파일 열기" , file_type=ft.FilePickerFileType.VIDEO, allow_multiple=True)),
				selected_files,
		])
	)

ft.app(target=main, view=ft.FLET_APP_HIDDEN)