from idlelib.browser import is_browseable_extension
from os import mkdir
from pathlib import Path
import shutil
import os
import subprocess
from tkinter.font import names

path_to_settings = ""
path_to_records = ""

def start():
    path_records_dir = "records"
    os.makedirs(path_records_dir, exist_ok=True)
    global path_to_records
    path_to_records = (Path.cwd()/"records").resolve()
    with open ("settings.txt", 'a+') as file:
        global path_to_settings
        path_to_settings = str((Path.cwd()/"settings.txt").resolve())

        file.seek(0)  # переместить курсор на элемент 0
        #бляя это пиздец, крч в начале чтения при a+ курсор находится в конце
        # и поэтому, len возвращает то сколько символов перед курсором
        # и каждый раз когда ты проходишся по файлу курсор становится в конец
        if len(file.read().strip()) < 3:
            open_with = input("Enter the path to the .exe file of the program\n"
                          "through which you want to open the file without \"\"\n"
                          "or just press Enter to open with notepad\n"
                          ":    ")
            if len(open_with.strip()) > 1:
                path_to_open = Path(open_with)
                if path_to_open.exists():
                    file.write(f"{path_to_open} \n")
                else:
                    file.write("notepad.exe\n")
                    print(path_to_open, "did not found")
            else:
                file.write("notepad.exe\n")
    print("start() executed")

def add_file( directory = None):
    path_to_dir_now = os.getcwd()
    path_to_dir_now_name = os.path.basename(path_to_dir_now)
    if directory is None and path_to_dir_now_name != "records":
        os.chdir("records")
    elif directory is not None:
        os.chdir(directory)
    else:
        pass
    choice_file_extension = input("write:\n"
                        "1 - to create .txt\n\n"
                        "2 - to create .md\n\n"
                        "3 - to create directory\n\n"
                        "or write your extension\n\n"
                        "or just press Enter to create .txt\n"
                        ":      ")
    choice_file_name = input("write file name\n"
                             ": ")
    if choice_file_extension == "3":
        mkdir(choice_file_name)
        print(f"dir {choice_file_name} created")
        return
    else:
        dict_creations = {
            "1": choice_file_name + ".txt",
            "2": choice_file_name + ".md",
        }
        if choice_file_extension == "":
            choice_file_extension = str(1)

        #print(dict_creations[choice_file_extension])
        with open(path_to_settings, "r+") as file:
            pass
            #subprocess.Popen([settings_file.readline().strip(),
                                #dict_creations[choice_file_extension]])

def show(number = None, path_to_dir = None): # потом надо доделать что бы
    path_to_dir_now = Path(os.getcwd())      # при открытие файла прога не закрывалась
    if path_to_dir_now != path_to_records:
        os.chdir(path_to_dir)
    else:
        pass
    list_with_files = []
    path_to_dir_now = Path(os.getcwd())
    for file in path_to_dir_now.iterdir():
        list_with_files.append(file.name)
    counter = 0
    for file in list_with_files:
        print(f"\n{counter} - {file}")
        counter += 1
    if number is None:
        while True:
            choice_file = None
            if Path.cwd().name != "records":
                choice_file = input("\nEnter files number to open him\n"
                                    "Or write |-1| to return"
                                    "Or write |-2| to add file\n"
                                    ": ")
            else:
                choice_file = input("\nEnter files number to open him\n"
                                    "or write |-2| to add file\n"
                                    ": ")
            number = choice_file
            if number == "-1" and Path.cwd().name != "records":
                while True:
                    os.chdir("..")
                    show(None,Path.cwd())
                    return
            elif number == "-2":
                add_file(Path.cwd())
            path_to_file_resolve =(Path(Path.cwd()/list_with_files[int(number)])
                                .resolve())
            if path_to_file_resolve.is_dir():
                os.chdir(path_to_file_resolve)
                show(None, path_to_file_resolve)
                return
            with open (path_to_settings, 'r+') as file:
                file.seek(0)
                file_for_open = Path (list_with_files[int(number)])
                found_suffix = False
                for line in file:
                    if line.strip() == file_for_open.suffix:
                        path_to_open = file.readline().strip()
                        subprocess.Popen([path_to_open, file_for_open])
                        found_suffix = True
                if not found_suffix:
                    file.seek(0)
                    subprocess.Popen([file.readline().strip(), list_with_files[int(number)]])
            print("show() executed")
        # вот здесь надо проверять являются ли настройки специализированными
        # если да то смотреть какое расширение у спициалезированого файла
        # и искать строчку ну допистим с ".md" если найдена то использавать
        # тот путь для редактора что после строки, если не найдена то
        # использавать уневерсальный вариант, тоесть то что на первой строчке

def add_special_extension():
    special_extension = input("Write the extension for which you want"
                              " to assign a special program\n"
                              "for example \".md\" or \".txt\" with out \"\"\n"
                              ":   ")
    path_to_special_extension =input("write path to program.exe\n"
                                 ": ")
    with open("settings.txt", 'a+') as file:
        if Path(path_to_special_extension).exists():
            file.write(special_extension + "\n")
            file.write(path_to_special_extension + "\n")
    print(f"add_special_extension() executed")



    # надо что бы спрашивал у юзера что создать 1)txt.файл 2)md.файл 3)папку
    # и каждому файлу присваивается id (id должен быть програмным
    # а не в риальном названии файла)
    # и что бы это создавалось в той папке в которой находимся
    # если создается файл, то открываеся в редакторе который указан


start()
#add_file()
show(None,path_to_records)
