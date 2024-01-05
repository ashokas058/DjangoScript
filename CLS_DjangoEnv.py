import subprocess
import os
from CLS_Constants import DJANGO_PORT_CONFIG_DIR,DJANGO_PROJECT_DIR,TEMP_UNZIP,DJANGO_BACKUP,DJANGO_UPLOAD,DJANGO_USER_GROUP
from CLS_Constants import DJANGO_OWNER
from CLS_Files import FileIO
class DjangoEnv:

 
    def __init__(self) :
        pass

    def check_package(self,package_name):
        try:
            subprocess.check_output(['dpkg', '-s', package_name])
            print(f"{package_name} is installed.")
        except subprocess.CalledProcessError:
            print(f"{package_name} is not installed.")
            self.install_package(package_name)

    def install_package(self,package_name):
        try:
            subprocess.check_call(['sudo', 'apt-get', 'install', '-y', package_name])
            print(f"{package_name} has been installed successfully.")
        except subprocess.CalledProcessError:
            print(f"Error installing {package_name}.")

    def install_Pythonpackage(self,package_name):
        try:
            subprocess.check_call(['pip3', 'install', package_name])
            print(f"Successfully installed {package_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package_name}: {e}")

    def initGlobalDir(self):
        try:
            os.makedirs(DJANGO_PROJECT_DIR,exist_ok=True)
            os.makedirs(DJANGO_PORT_CONFIG_DIR,exist_ok=True)
            os.makedirs(TEMP_UNZIP,exist_ok=True)
            os.makedirs(DJANGO_UPLOAD,exist_ok=True)
            os.makedirs(DJANGO_BACKUP,exist_ok=True)
            FileIO().applyOwnerShip(DJANGO_USER_GROUP, DJANGO_OWNER)
            return [DJANGO_PROJECT_DIR,DJANGO_PORT_CONFIG_DIR]
        except Exception as e:
            print(f"Exception at CLS_DjangoENV :- {e}\n")
            print((f"run it as sudo user\n"))

    