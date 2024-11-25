import flet as ft
import pandas as pd
import openpyxl


def find_max(arr):
    if arr != []:
        return max(arr)
    else:
        return None

def main(page: ft.Page):
    page.auto_scroll = True
    page.title = "MassSpectroMiner"

    global max_value_flag
    max_value_flag = False

    global file_directory

    global new_df
    new_df = pd.DataFrame()

    selected_files = ft.Text()






    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        global file_directory

        file_directory = " ".join(map(lambda f: f.path, e.files))



        #combine_button.disabled = False
        #combine_button.update()
        selected_files.update()
        button_start.disabled = False
        page.update()



    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    dial = ft.Row(
        [
            ft.ElevatedButton(
                "Выберите файл",
                icon=ft.icons.UPLOAD_FILE,
                on_click=lambda _: pick_files_dialog.pick_files(
                    allow_multiple=True
                ),
            ),
            selected_files,
        ]
    )

    def checkbox_changed(e):
        global max_value_flag
        max_value_flag = not max_value_flag



    div1 = ft.Divider(height=10, color="white")

    tb1 = ft.TextField(label="Числовое значение")
    proc = ft.TextField(label="Процентное отклонение")
    check_max = ft.Checkbox(label="Искать только максимальные значения", on_change=checkbox_changed)

    found_values = ft.Text("Найденные значения:")

    values = [tb1, proc]
    nmb1 = ft.Text(f"{int(len(values)/2)} Значение",  size=20)

    dlg = ft.AlertDialog(
        title=ft.Text("Файл создан!")
    )

    dlg_error = ft.AlertDialog(
        title=ft.Text("Возникла ошибка. Не удается откорректировать файл")
    )

    def button_clicked(e):
        global max_value_flag
        try:
            workbook = openpyxl.load_workbook(file_directory)
            sheets = workbook.sheetnames

            global new_df
            new_df['Выгрузка'] = sheets

            values_dict = {}

            value_find = int(tb1.value)
            percent_put = float(proc.value)/100
            if value_find not in values_dict:
                values_dict[value_find] = percent_put

                #if max_value_flag:
                #    value_find = f'{value_find} MAX'

                new_df[value_find] = ''
                for sheet in sheets:

                    return_list = []
                    df = pd.read_excel(file_directory, sheet_name=sheet, skiprows=range(0,2))
                    query_df = df[(df['m/z'] > value_find - value_find * percent_put) & (
                                df['m/z'] < value_find + value_find * percent_put)]
                    for intens in query_df['Intens.']:
                        return_list.append(intens)

                    # print(return_list)
                    new_df = new_df.astype('object')

                    for c, v in enumerate(new_df['Выгрузка']):
                        if v == sheet:
                            if max_value_flag:
                                new_df[value_find][c] = find_max(return_list)
                            else:
                                new_df[value_find][c] = return_list
                            break
            if max_value_flag:
                value_find =f' {value_find} MAX'
            found_values.value = found_values.value + f' {value_find}'
            button_save.disabled = False
            page.update()
        except Exception as d:
            page.dialog = dlg_error
            dlg_error.title = ft.Text(f'Возникла ошибка {d}')
            #dlg_error.content = f'{d}'
            dlg_error.open = True
            page.update()



    button_start = ft.ElevatedButton(text="Отформатировать столбцы", disabled=True, on_click=button_clicked)

    def button_save_clicked(e):
        try:
            global new_df
            file_name = file_directory.split('.')[0] + ' FORMATTED.' + file_directory.split('.')[1]
            new_df.to_excel(file_name)

            page.dialog = dlg
            dlg.open = True
            page.update()
        except Exception as d:
            page.dialog = dlg_error
            dlg_error.title = ft.Text(f'Возникла ошибка {d}')
            dlg_error.open = True
            page.update()



    button_save = ft.ElevatedButton(text="Выгрузить данные", bgcolor=ft.colors.GREEN_100, disabled=True, on_click=button_save_clicked)



    page.add(ft.Text("Выберите файл Масспектрометрии для переформатирования"))

    page.add(dial,div1,nmb1, tb1, proc,check_max, button_start,div1, found_values, button_save)



ft.app(target=main)