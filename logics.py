from os import mkdir
from pathlib import Path
import shutil
import os
import subprocess
import sys
import webbrowser


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
        with open(dict_creations[choice_file_extension], "w") as file:
            file.write("")
            pass
        with open(path_to_settings, "r+") as file:
            file.seek(0)
            file_for_open = Path(dict_creations[choice_file_extension])
            print(type(file_for_open))
            found_suffix = False
            for line in file:
                if line.strip() == file_for_open.suffix:
                    path_to_open =  file.readline().strip()
                    subprocess.Popen([path_to_open, file_for_open])
                    found_suffix = True
            if not found_suffix:
                file.seek(0)
                subprocess.Popen([file.readline().strip(),
                                dict_creations[choice_file_extension]])

def show(number = None, path_to_dir = None):
    path_to_dir_now = Path(os.getcwd())
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
                                    "Or write |-1| to return\n"
                                    "Or write |-2| to add file\n"
                                    "Or write |-3| to move file\n"
                                    "Or write |-4| to add special_extension\n"
                                    "Or write |-5| ro remove some file\n"
                                    "Or write |-6| to copy file or dir\n"
                                    "Or write |-0| - to close program\n"
                                    
                                    ": ")
            else:
                choice_file = input("\nEnter files number to open him\n"
                                    "Or write |-2| to add file\n"
                                    "Or write |-3| to move file\n"
                                    "Or write |-4| to add special_extension\n"
                                    "Or write |-5| ro remove some file\n"
                                    "Or write |-6| to copy file or dir\n"
                                    "Or write |-0| to close program\n"
                                    ": ")
            number = choice_file
            if number == "-1" and Path.cwd().name != "records":
                while True:
                    os.chdir("..")
                    show(None,Path.cwd())
                    return
            elif number == "-2":
                add_file(Path.cwd())
                show(None,Path.cwd())
            elif number == "-3":
                path_to_movable_file = (
                Path(list_with_files[int(input("write number of movable_file: "))]))
                moving_place = input(
                                    "write number of dir for moving file\n"
                                    "or write |-1| for moving to parent dir: ")
                path_to_moving_place = Path(list_with_files[int(moving_place)])
                if moving_place == "-1":
                    move_file(path_to_movable_file,Path.cwd().parent )
                    print("done")
                else:
                    move_file(path_to_movable_file, path_to_moving_place)
                print("done")
                show(None, Path.cwd())
            elif number == "-0":
                sys.exit()
            elif number == "-4":
                add_special_extension()
                continue
            elif number == "-5":
                number_of_remove_file = input("write number of file to remove: ")
                remove_file(list_with_files[int(number_of_remove_file)])
                continue
            elif number == "-6":
                copy_file_number = input("write number of copying: ")
                place_to_copy = input("write path to copy_place\n"
                                      "or just write Enter to copy in desktop\n"
                                      ": ")
                if place_to_copy == "":
                    copy_file(list_with_files[int(copy_file_number)],str(Path.home()/"Desktop"))
                else:
                    copy_file(list_with_files[int(copy_file_number)], place_to_copy)
                continue
            path_to_file_resolve =(Path(Path.cwd()/list_with_files[int(number)])
                                .resolve())
            if path_to_file_resolve.is_dir():
                os.chdir(path_to_file_resolve)
                show(None, path_to_file_resolve)
                return
            with open (path_to_settings, 'r+') as file:
                file.seek(0)
                file_for_open = Path (list_with_files[int(number)])
                full_path_to_open_file = Path.cwd()/file_for_open
                found_suffix = False
                for line in file:
                    if line.strip() == file_for_open.suffix:
                        path_to_open = Path(file.readline().strip())
                        browsers_list = ["chrome.exe", "msedge.exe", "firefox.exe",
                        "brave.exe", "opera.exe", "opera_gx.exe", "vivaldi.exe",
                        "iexplore.exe", "tor.exe", "waterfox.exe", "palemoon.exe",
                        "maxthon.exe", "midori.exe", "slimjet.exe" ]
                        if path_to_open.name in browsers_list:
                            webbrowser.register(
                                "browser",
                                None,
                                webbrowser.BackgroundBrowser(str(path_to_open))
                            )
                            webbrowser.get("browser").open(f"file:///{full_path_to_open_file}")
                            found_suffix = True
                        else:
                            subprocess.Popen([path_to_open, file_for_open])
                            found_suffix = True
                if not found_suffix:
                    file.seek(0)
                    subprocess.Popen([file.readline().strip(), list_with_files[int(number)]])
            print("show() executed")

def add_special_extension():
    dir_now = Path.cwd()
    os.chdir(path_to_records)
    os.chdir("..")
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
    show(None,dir_now)

def move_file(path_to_movable_file,path_to_moving_place ):
    shutil.move(path_to_movable_file, path_to_moving_place)

def remove_file(path_to_file):
    if Path(path_to_file).is_dir():
        shutil.rmtree(path_to_file)
        print("done")
    if Path(path_to_file).is_file():
        os.remove(path_to_file)
        print("done")
    show(Path.cwd())

def copy_file(copy_file, place_for_copy):
    if Path(copy_file).is_file():
        shutil.copy2(copy_file, place_for_copy)
    elif Path(copy_file).is_dir():
        shutil.copytree(copy_file, place_for_copy, dirs_exist_ok=True)
    show(Path.cwd())
