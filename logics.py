from pathlib import Path
import shutil
import os

def start ():
    path_records_dir = "records"
    os.makedirs(path_records_dir, exist_ok=True)
    with open ("settings.txt", 'a+') as file:
        if file.read().splitlines() != "":
            open_with = input("Enter the path to the .exe file of the program\n"
                          " through which you want to open the file without \"\"\n"
                          "ot just press Enter to open with notepad\n"
                          ":    ")
            if len(open_with) > 0:
                path_to_open = Path(open_with)
                if path_to_open.exists():
                    file.write(f"start \"\" \"{path_to_open}\" \n")
                else:
                    print(path_to_open, "did not found")
            else:
                file.write("start notepad.exe \n") 
            print("done")


def create_file(path):
    pass


start()
