from os import mkdir
from pathlib import Path
import shutil
import os
import subprocess
path_to_settings = ""
path_to_records = ""
def start():
    path_records_dir = "records"
    os.makedirs(path_records_dir, exist_ok=True)
    #os.chdir("records")
    global path_to_records
    path_to_records = (Path.cwd()/"records").resolve()
    with open ("settings.txt", 'a+') as file:
        global path_to_settings
        path_to_settings = (Path.cwd()/"settings.txt").resolve()

        file.seek(0)  # переместить курсор на элемент 0
        #бляя это пиздец, крч в начале чтения при a+ курсор находится в конце
        # и поэтому, len возвращает то сколько символов перед курсором
        # и каждый раз когда ты проходишся по файлу курсор становится в конец
        if len(file.read().strip()) < 3:# баг
            open_with = input("Enter the path to the .exe file of the program\n"
                          "through which you want to open the file without \"\"\n"
                          "or just press Enter to open with notepad\n"
                          ":    ")
            if len(open_with.strip()) > 0:
                path_to_open = Path(open_with)
                if path_to_open.exists():
                    file.write(f"{path_to_open} \n")
                else:
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
                        "or just press Enter to create .txt\n"
                        ":      ")
    choice_file_name = input("write file name\n"
                             ": ")
    if choice_file_extension == 3:
        mkdir(choice_file_name)
        print(f"dir {choice_file_name} created")
    else:
        dict_creations = {
            "1": choice_file_name + ".txt",
            "2": choice_file_name + ".md",
        }
        if choice_file_extension == "":
            choice_file_extension = str(1)

        #print(dict_creations[choice_file_extension])
        with open(dict_creations[choice_file_extension], 'a+' ) as file:
            with open(path_to_settings, "r+") as settings_file:
                print(1)
                if settings_file.readline().strip() == "notepad.exe":
                    os.startfile(dict_creations[choice_file_extension], 'open')
                else:
                    settings_file.seek(0)
                    print(settings_file.readline().strip())
                    print(2)
                    settings_file.seek(0)
                    subprocess.Popen([settings_file.readline().strip(),dict_creations[choice_file_extension]])

def show(number = None):
    print(path_to_records)
    print(os.getcwd())
    print(os.getcwd() == path_to_records)
    if os.getcwd() != path_to_records:
        print("change to records")
        os.chdir("records")
    else:
        pass
    list_files = []
    path_records = Path(os.getcwd())
    for file in path_records.iterdir():
        list_files.append(file.name)
    counter = 0
    for file in list_files:
        print(f"{counter} - {file}")
        counter += 1
    #os.chdir("records")
    print("show() executed")




    # надо что бы спрашивал у юзера что создать 1)txt.файл 2)md.файл 3)папку
    # и каждому файлу присваивается id (id должен быть програмным
    # а не в риальном названии файла)
    # и что бы это создавалось в той папке в которой находимся
    # если создается файл, то открываеся в редакторе который указан


start()
add_file()
show()
