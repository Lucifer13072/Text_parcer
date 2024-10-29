import flet as ft
import json

def main(page: ft.Page):

    def dark():
        page.theme_mode = ft.ThemeMode.DARK
        theme_b.bgcolor=ft.colors.BLACK
        theme_b.color=ft.colors.WHITE
        theme_b.icon = ft.icons.DARK_MODE
        page.update()
        parametrs["theme"] = True
        with open("settings.json", "w", encoding="utf-8") as file:
            json.dump(parametrs, file)


    def light():
        page.theme_mode = ft.ThemeMode.LIGHT
        theme_b.bgcolor=ft.colors.WHITE
        theme_b.color=ft.colors.BLACK
        theme_b.icon = ft.icons.LIGHT_MODE
        page.update()
        parametrs["theme"] = False
        with open("settings.json", "w", encoding="utf-8") as file:
            json.dump(parametrs, file)

    def fsc(e):
        if fullscreen_b.data == True:
            page.window_maximized = True
            fullscreen_b.data == False
            page.update()
        else:
            page.window.width = 900
            page.window.height = 500
            fullscreen_b.data == True
            page.update()

    def save_setting(e):
        parametrs["key"] = key_task.value
        with open("settings.json", "w", encoding="utf-8") as file:
            json.dump(parametrs, file)
        settings_modal.open = False
        page.update()  
    

    with open("settings.json", "r", encoding="utf-8") as file:
            settings_par = json.load(file)

    parametrs = settings_par

    page.title = "Parcer"
    page.window.height = 900
    page.window.width = 500
    page.window.title_bar_hidden = True
    page.window.title_bar_buttons_hidden = True

    def theme_replace(e):
        if theme_b.data == True: #Dark
            theme_b.data = False
            dark()
            parametrs["theme"] = True
        else: #Light 
            theme_b.data = True
            light()
            parametrs["theme"] = False
        page.update()
    
    def minm(e):
        page.window_minimized = True
        page.update()

    #buttons
    theme_b = ft.IconButton(icon=ft.icons.DARK_MODE, on_click=theme_replace) 
    fullscreen_b = ft.IconButton(ft.icons.FULLSCREEN, on_click=fsc, data=True)
    settings_b = ft.IconButton(ft.icons.SETTINGS, on_click=lambda e: page.open(settings_modal))
    model_button_main_dl = ft.TextButton(text="Сохранить", on_click=save_setting)

    #tasks
    key_task = ft.TextField(max_lines=1, shift_enter=True, expand=True, value=settings_par["key"])

    #text
    key_text = ft.Text(value="API gigachat:")

    settings_modal = ft.AlertDialog(
        modal=True,
        content=ft.Column(
                [ft.Row([key_text, key_task])],
                spacing=10,
                height=200,),
        actions=[
            ft.IconButton(ft.icons.HELP, on_click=help),
            model_button_main_dl
        ],
        actions_alignment=ft.MainAxisAlignment.START
    )

    page.add(
        ft.Row(controls=[ft.WindowDragArea(
            ft.Text("Парсер данных", weight=800), expand=True),
            settings_b,
            theme_b,
            ft.IconButton(ft.icons.MINIMIZE, on_click=minm),
            fullscreen_b,
            ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close())]),
    )

    if settings_par["theme"] == True:
        dark()
        theme_b.data = False
    else:
        light()
        theme_b.data = True

ft.app(main)