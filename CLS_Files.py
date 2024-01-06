from CLS_Constants import DJANGO_PORT_CONFIG_DIR
from CLS_Constants import DJANGO_PROJECT_DIR, DJANGO_UPLOAD, DJANGO_BACKUP,DJANGO_LOGGING
import os
import shutil
import subprocess
import zipfile
import fnmatch
from CLS_Logging import Logger
class FileIO:

    def __init__(self) -> None:
        self.logger=Logger()
    def filterFiles(self,directory, keyword):
        matchingFiles = []
        for filename in os.listdir(directory):
            if fnmatch.fnmatch(filename, f"*{keyword}*"):
                matchingFiles.append(filename)
        return matchingFiles

    def createDir(self,name):
        os.makedirs(name, exist_ok=True)

    def deleteDirBash(self,directoryPath):
        try:
            subprocess.check_call(['rm', '-rf', directoryPath])
            print(f"deleted files under {directoryPath}\n")
            return True
        except Exception as e:
            print(f"deleted files under {e}\n")
            return True
    def deleteFilesDir(self, directory_path):
        try:
            if not os.path.exists(directory_path):
                print(f"The directory '{directory_path}' does not exist.")
                return
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)

                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")

            print(f"All files in '{directory_path}' have been deleted.\n")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.logger.createLog_data(f"An error occurred in deletefileDir(): {e}",DJANGO_LOGGING)

    def deleteFile(self, absoluteFilePath):
        try:
            if os.path.isfile(absoluteFilePath):
                os.remove(absoluteFilePath)
                print(f"Deleted: {absoluteFilePath}")
                self.logger.createLog_data(f"Deleted: {absoluteFilePath}",DJANGO_LOGGING)
            else:
                print(f"files can't be deleted '{absoluteFilePath}.\n")
                self.logger.createLog_data(f"files can't be deleted '{absoluteFilePath}.",DJANGO_LOGGING)

        except Exception as e:
            print(f"An error occurred: {e}")

    def listFilesExcept(self,directoryPath, excluded_files=[]):
        try:
            files = [f for f in os.listdir(directoryPath) if f not in excluded_files]
            return files
        except FileNotFoundError:
            print(f"Directory '{directoryPath}' not found.")
            return []

    def unzipPy(self, zipFilePath, destinationPath):
        try:
            if(os.path.isfile(zipFilePath) and os.path.isdir(destinationPath)):
                with zipfile.ZipFile(zipFilePath, 'r') as zipRef:
                    for file_info in zipRef.infolist():
                        file_info.filename = os.path.basename(file_info.filename)
                        zipRef.extract(file_info, destinationPath)
                    # zipRef.extractall(destinationPath)
                return True
            return False
        except Exception as e:
            print(f"An error occurred during unzip: {e}\n")
            return False

    def unzipFiles(self,zipFilePath, destinationPath):
        try:
            if(os.path.isfile(zipFilePath) and os.path.isdir(destinationPath)):
                subprocess.run(['unzip', '-o', zipFilePath, '-d', destinationPath], check=True)
                print(f'Successfully unzipped {zipFilePath} to {destinationPath}')
                self.logger.createLog_data(f'Successfully unzipped {zipFilePath} to {destinationPath}',DJANGO_LOGGING)
                return True
            return False
        except subprocess.CalledProcessError as e:
            print(f'Error occurred in unzipFiles(): {e}\n')
            self.logger.createLog_data(f'Error occurred in unzipFiles(): {e}',DJANGO_LOGGING)
            return False

    def sync_files(self, source, destination):
        try:
            if(os.path.isdir(source) and os.path.isdir(destination)):
                rsync_command = ['rsync', '-av', source, destination]

                # Run the rsync command
                subprocess.run(rsync_command, check=True)

                print(f"Sync completed successfully: {source} -> {destination}\n")
                self.logger.createLog_data(f"Sync completed successfully: {source} -> {destination}",DJANGO_LOGGING)
                return True

            return False
        except subprocess.CalledProcessError as e:
            print(f"Error syncing files: {e}")
            return False


    def updateScript(self, templatePath, destinationPath, apiFolderName, type):
        try:
            if(os.path.isfile(templatePath) and os.path.isdir(destinationPath)):
                apiDetails = apiFolderName.split("-")
                domain = apiDetails[0]
                project = f"Project-{apiDetails[1]}"
                port = apiDetails[2]
                confScript = f"{apiFolderName}{type}"
                destinationFile = os.path.join(destinationPath, confScript)
                script = None
                with open(templatePath, 'r') as file:
                    script = file.read()
                    script = script.replace('port', port)
                    script = script.replace('apiName', apiFolderName)
                    script = script.replace('projectName', project)
                    script = script.replace('domainName', domain)
                    script = script.replace('scriptName', confScript)
                with open(destinationFile, 'w') as file:
                    file.write(script)
                print(f"Django configuration created:- {destinationFile}\n")
                self.logger.createLog_data(f"Django configuration created:- {destinationFile}",DJANGO_LOGGING)
                return destinationFile
            return False
        except Exception as e:
            print(f"An error occurred Script-replace: {e}")
            self.logger.createLog_data(f"An error occurred Script-replace: {e}\n",DJANGO_LOGGING)
            return  False

    def getExistingProject(self):
        if(os.path.isdir(DJANGO_PROJECT_DIR)):
            return os.listdir(DJANGO_PROJECT_DIR)
        else:
            print(f"Directory not exist, create it:- {DJANGO_PROJECT_DIR}\n ")
            return False


    def getExistingApi(self, projectName):
        return os.listdir(os.path.join(DJANGO_PROJECT_DIR, projectName))

    def listZip(self, files):
        if(files):
            return [file for file in files if file.endswith('.zip')]
        return False

    def listSql(self, files):
        if(files):
            return [file for file in files if file.endswith('.sql')]
        return False

    def createVenv(self,projectLocation):
        try:
            fullCommand = ["sudo", "virtualenv", projectLocation]
            subprocess.run(fullCommand, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error in creating virtual environment: {e}")
            return False



    def listDir(self, location):
        try:
            if(os.path.isdir(location)):
                return os.listdir(location)
            return False
        except Exception as e:
            print(f"An error occurred Script-replace: {e}\n")
            return False

    def createProjectDir(self, projectName):
        try:
            projectFolder = f"Project-{projectName}"
            # Create Project Root Folder
            projectMain = os.path.join(DJANGO_PROJECT_DIR, projectFolder)
            if not os.path.isdir(projectMain):

                os.makedirs(projectMain, exist_ok=True)

                print(f"created new Project Folder:- {projectMain}.")

                # -------------------------------------------------
                # create config folder under /WEBAPP_Config

                projectConfig = os.path.join(DJANGO_PORT_CONFIG_DIR, projectFolder)
                os.makedirs(projectConfig, exist_ok=True)
                print(f"Created Project config folder:- {os.path.join(DJANGO_PORT_CONFIG_DIR, projectFolder)}\n")
                self.createVenv(projectMain)
                print(f"virtual environment created, required a pip install -r req.txt\n")
                self.logger.createLog_data(f"Created Project config folder:- {os.path.join(DJANGO_PORT_CONFIG_DIR, projectFolder)}",DJANGO_LOGGING)
                return projectFolder
            else:
                return False

        except Exception as e:
            print(f"File Project dir creation error at CLS_FILES:-{e}\n")
            self.logger.createLog_data(f"File Project dir creation error at CLS_FILES:-{e}\n",DJANGO_LOGGING)

    def createApiDir(self, projectFolder, apiName, port):
        try:
            projectName = projectFolder.split("-")[1]
            apiFolder = f"{apiName}-{projectName}-{port}"
            apiMain = os.path.join(os.path.join(DJANGO_PROJECT_DIR, projectFolder), apiFolder)
            apiLog=os.path.join(apiMain,"logs")
            if not os.path.isdir(apiMain):
                os.makedirs(apiMain, exist_ok=True)
                print(f"created new API Folder:- {apiMain}.\n")
                self.logger.createLog_data(f"created new API Folder:- {apiMain}.",DJANGO_LOGGING)
                os.makedirs(apiLog, exist_ok=True)
                logFile=os.path.join(apiMain,"uwsgi_supervisor.log")
                self.logger.createLog_data(f"<<<<Log created>>>>>",logFile)
                print(f"logging enabled\n")


                # -------------------------------------------------
                # create backup Folder
                projectBackup = os.path.join(DJANGO_BACKUP, projectFolder)
                os.makedirs(projectBackup, exist_ok=True)
                print(
                    f"created new Backup Folder:-{projectBackup}\n")
                self.logger.createLog_data(f"created new Backup Folder:-{projectBackup}",DJANGO_LOGGING)

                print(f"default upload folder {DJANGO_UPLOAD}")
                self.logger.createLog_data(f"default upload folder {DJANGO_UPLOAD}",DJANGO_LOGGING)
                self.logger.createLog_data(f"created new Backup Folder:-{projectBackup}",DJANGO_LOGGING)
                # create uploadFolder
                # projectUpload = os.path.join(os.path.join(DJANGO_UPLOAD, projectFolder), apiFolder)
                # os.makedirs(projectUpload, exist_ok=True)
                # print(f"created new upload Folder:-{os.path.join(os.path.join(DJANGO_UPLOAD, projectFolder), apiFolder)}")

                return apiFolder
            else:
                return False
        except Exception as e:
            print(f"File Api dir creation error at CLS_FILES:-{e}\n")
            self.logger.createLog_data(f"File Api dir creation error at CLS_FILES:-{e}\n",DJANGO_LOGGING)
            return False


    def zipFilesPy(self,apiFolder,destination):
        try:
            if(os.listdir(apiFolder)):
                shutil.make_archive(destination, 'zip',apiFolder)
                self.logger.createLog_data(f"backup completed, to {destination}",DJANGO_LOGGING)
            else:
                self.logger.createLog_data("Skipping backup, no resource found",DJANGO_LOGGING)
                return "Skipping backup, no resource found"
        except Exception as e:
            self.logger.createLog_data(f"An error occurred while taking backup-{e}",DJANGO_LOGGING)
            print(f"An error occurred while taking backup-{e}\n")



    def zipFiles(self,apiFolder, destination):
        try:
            if(os.listdir(apiFolder)):
                subprocess.run(['zip', '-r', destination, apiFolder], check=True)
                print(f'Successfully zipped {apiFolder} to {destination}\n')
                self.logger.createLog_data(f'Successfully zipped {apiFolder} to {destination}',DJANGO_LOGGING)
        except subprocess.CalledProcessError as e:
            print(f'Error occurred: {e}\n')
            self.logger.createLog_data(f"An error occurred while taking backup-{e}",DJANGO_LOGGING)
            return False

    def applyOwnerShip(self,userGroup,destinationPath):
        try:
            fullCommand = ["sudo", "chown", "-R", userGroup, destinationPath]
            subprocess.run(fullCommand, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error in ownership apply: {e}\n")
            return False


    def reloadApiService(self):
        try:
            fullCommand = ["sudo", "supervisorctl", "reload"]
            subprocess.run(fullCommand, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error in poastgres: {e}")
            return False
