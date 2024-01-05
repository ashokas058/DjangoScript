import os
from CLS_Constants import DJANGO_PORT_CONFIG_DIR, DJANGO_UPLOAD, PORT_POOL, PORT_COMMON, PACKAGES,PYTHON_PACKAGE
from CLS_Constants import SUPERVISOR_CNF, DJANGO_PROJECT_DIR, TEMP_UNZIP,DJANGO_BACKUP,DJANGO_PORT_CONFIG_DIR,DJANGO_LOGGING
from CLS_Constants import TEMPLATE_NGINX, TEMPLATE_SUPERVISOR, TEMPLATE_UWSGI, NGINX_SITEAVAILABLE, NGINX_SITENABLED
from CLS_Constants import DJANGO_USER_GROUP,DJANGO_NGINX_OWNERSHIP,DJANGO_CERT_LOCATION,EXCLUDE_FILES
from CLS_DataBaseManager import PostgresMgmnt
from CLS_DjangoEnv import DjangoEnv
from CLS_Files import FileIO
from CLS_PortManager import PortManager
from CLS_Utils import UtilesDjango
from CLS_Logging import Logger
from os.path import join


class Starter:


    def __init__(self):
       self.log=Logger()
    def updateApiCode(self, sourceFile, destinationPath):
        try:
            if(os.path.isfile(sourceFile) and os.path.isdir(destinationPath)):
                FileIO().unzipFiles(sourceFile,TEMP_UNZIP)
                FileIO().sync_files(TEMP_UNZIP,destinationPath)
                FileIO().deleteDirBash(join(TEMP_UNZIP,"/*"))
                # FileIO().deleteFile(sourceFile)
                self.log.createLog_data(f"completedAPI update :- {destinationPath}",DJANGO_LOGGING)
            else:
                return False
        except Exception as e:
            self.log.createLog_data(f"error in updateApiCode():- {e}",DJANGO_LOGGING)
            print(f"error in updateApiCode():- {e}")
            return False

    def uiSelection(self,directoryPath,excludeFiles):
        if(len(directoryPath)>0):
            list=FileIO().listFilesExcept(directoryPath,excludeFiles)
            index=None
            if(list):
                index=UtilesDjango().terminalUI(list)
                return list[index]
        else:
            print("input Project Name required:- uiApiSelection\n")
            self.log.createLog_data("input Project Name required:- uiApiSelection\n",DJANGO_LOGGING)
            return False

    def reloadSuperVisor(self):
        try:
            if(FileIO().reloadApiService()):
                print(f"updated Supervisor's API Services\n")
            else:
                print("error in supervisor reload")
        except Exception as e:
            print(f"exception in supervisor :- {e}")

    def initBackup(self,apiFolder,dbName):
        if(len(apiFolder)>0 and len(dbName)>0):
            apiPathSplit=apiFolder.split("-")
            project=f"Project-{apiPathSplit[1]}"
            absoluteApiPath=os.path.join(os.path.join(DJANGO_PROJECT_DIR,project),apiFolder)
            PostgresMgmnt().createDbBackup(absoluteApiPath,dbName)
            FileIO().zipFiles(absoluteApiPath,DJANGO_BACKUP)
        else:
            print(f"input apiFolder name and DbName is required :- initBackup ()\n")
            return False

    def createDb(self,dbName):
        if(len(dbName)>0):
            PostgresMgmnt().createDB(dbName)
            return dbName
        else:
            print(f"input DbName required in :- CreateDb()\n")
            return False
    def migrateDb(self,apiFolder,dbName):
        print(f"\nupload zip file to:- {DJANGO_UPLOAD}\n FilesName :- {apiFolder}.sql\n ")
        print(f"WARNING --required files should be uploaded\n")
        if(len(apiFolder)>0 and len(dbName)):
            dbDumpFile=f"{apiFolder}.sql"
            dbDumpAbsolutePath=os.path.join(DJANGO_UPLOAD,dbDumpFile)
            if(os.path.isfile(dbDumpAbsolutePath)):
                PostgresMgmnt.createDB(dbName)
                PostgresMgmnt.restoreDB(dbName,dbDumpAbsolutePath)
            else:
                print(f"No files exist:- {dbDumpAbsolutePath}, please upload")
        else:
            print(f"input apiFolder name and DbName is required :- migrateDb ()\n")
            return False

    def restoreDb(self,dbName,backupFile):
        try:
            if(len(dbName)>0 and os.path.isfile(backupFile)):
                PostgresMgmnt().terminatePgCon(dbName)
                PostgresMgmnt().dropDB(dbName)
                PostgresMgmnt().createDB(dbName)
                PostgresMgmnt().restoreDB(dbName, backupFile)
            else:
                print(f"dnName and backup Files required, missing error:- restoreDb()\n")
                return False
        except Exception as e:
            print(f"error in restoreDB() :- {e}")

    def initProject(self):
        try:
            initPort=PortManager(os.path.join(DJANGO_PORT_CONFIG_DIR,PORT_POOL))
            UtilesDjango().listFormated(FileIO().filterFiles(DJANGO_PROJECT_DIR,"Project-"),"Project")
            projectName=input("Enter the Project Name\n")
            print(f"Current available port from Pool:-{initPort.readNextPort()}\n")
            pPort=int(input("Enter the api port "))
            if not (initPort.isPortInUse(pPort)):
                if(len(projectName) and pPort>=7000):
                    projectOb=FileIO().createProjectDir(projectName)
                    if(projectOb):
                        projectFolder=f"Project-{projectName}"
                        portFilePath=os.path.join(os.path.join(DJANGO_PORT_CONFIG_DIR,projectFolder),PORT_COMMON)
                        initPort.setPortToProject(pPort,portFilePath)
                        initPort.removePort(pPort)
                        return projectFolder
                    else:
                        print(f"Project already exist")
                        return False
                else:
                    print("input required for ProjectName or Port is invalid :- initProject()\n")
                    return False
            print(f"Error:- port is already in use or remove the port {DJANGO_PORT_CONFIG_DIR}/portPool.txt file for getting next unused port\n")
        except Exception as e:
            print(f"error in initProject(){e}")
    def initAPI(self,project):
        try:
            if(len(project)>0):
                UtilesDjango().listFormated(FileIO().listFilesExcept(join(DJANGO_PROJECT_DIR,project),EXCLUDE_FILES),"API under "+project)
                apiName=input("Enter the API name/Valid domain\n")
                if(len(apiName)>0):
                    initPort=PortManager(os.path.join(DJANGO_PORT_CONFIG_DIR,PORT_POOL))
                    portFilePath=os.path.join(join(DJANGO_PORT_CONFIG_DIR,project),PORT_COMMON)
                    port=initPort.getPortFromProject(portFilePath)
                    apiFolder=FileIO().createApiDir(project,apiName,port)
                    if(apiFolder):
                        if not (initPort.isPortInUse(port)):
                            initPort.setPortToProject(port+1,portFilePath)
                            return apiFolder
                    else:
                        print(f"api already exist\n")
                        return False
                else:
                    print("input required for apiName\n")
                    return False
            else:
                print("project input is required in initApi()\n")
                return False
        except Exception as e:
            print(f"Exception in initApi:- {e}")
            return False


    def initDjangoEnv(self):
        for package in PACKAGES:
            print(f"installin linux packages:-{package}")
            DjangoEnv().check_package(package)
        for package in PYTHON_PACKAGE:
            print(f"installin python packages:-{package}")
            DjangoEnv().install_Pythonpackage(package)
        initPort=PortManager(os.path.join(DjangoEnv().initGlobalDir()[1],PORT_POOL))
        initPort.initializePorts(7000,50,1000)

    def initApiConfiguration(self,apiFolder):
        try:
            if(len(apiFolder)>0):
                apiPathSplit=apiFolder.split("-")
                project=f"Project-{apiPathSplit[1]}"
                domain=apiPathSplit[0]
                uwsgiPath=os.path.join(os.path.join(DJANGO_PROJECT_DIR,project),apiFolder)
                supervisorFilePath=FileIO().updateScript(TEMPLATE_SUPERVISOR,SUPERVISOR_CNF,apiFolder,".conf")
                uwsgiScriptpath=FileIO().updateScript(TEMPLATE_UWSGI,uwsgiPath,apiFolder,".sh")
                nginxConfPath=FileIO().updateScript(TEMPLATE_NGINX,NGINX_SITEAVAILABLE,apiFolder,".conf")
                UtilesDjango().nginxSiteLink(nginxConfPath,NGINX_SITENABLED)
                return [supervisorFilePath,uwsgiScriptpath,nginxConfPath,apiFolder]
            else:
                print(f"input is required :- apiFolder name in :- initApiConfiguration()\n")
                return False
        except Exception as e:
            print(f"Exception in initApiConfiguration:- {e}")
            return False

    def installSSL(self,domain):
        if(UtilesDjango().installSSL(domain)):
            if(FileIO().applyOwnerShip(DJANGO_NGINX_OWNERSHIP,DJANGO_CERT_LOCATION)):
                print(f"ownership applied:- {DJANGO_CERT_LOCATION} with {DJANGO_NGINX_OWNERSHIP}")

    def migrateApi(self,apiFolder):
        try:
            if(len(apiFolder)>0):
                uploadStat=1
                apiPathSplit=apiFolder.split("-")
                project=f"Project-{apiPathSplit[1]}"
                api=apiPathSplit[0]
                backendFile=f"{api}.zip"
                distfile=f"{api}-dist.zip"

                backendAbsolutePath=os.path.join(DJANGO_UPLOAD,backendFile)
                distAbsolutePath=os.path.join(DJANGO_UPLOAD,distfile)

                destinationPath=os.path.join(os.path.join(DJANGO_PROJECT_DIR,project),apiFolder)

                print(f"\nupload zip file to:- {DJANGO_UPLOAD}\n FilesName :-\n{api}.zip\n{api}-dist.zip\n ")
                print(f"WARNING --All required files should be uploaded\n")
                while(uploadStat):
                    stat=int(input("\n1)Sync\n ANY key to exit\n"))
                    if(stat):
                        lists=FileIO().filterFiles(DJANGO_UPLOAD,api)
                        if lists:
                                for item in lists:
                                    size=os.path.getsize(os.path.join(DJANGO_UPLOAD,item))/(1024**3)
                                    print(f"{item}-{size}")

                                self.updateApiCode(backendAbsolutePath,destinationPath)
                                self.updateApiCode(distAbsolutePath,destinationPath)
                                if(FileIO().applyOwnerShip(DJANGO_USER_GROUP, destinationPath)):
                                    print(f"ownership applied :-{destinationPath} with {DJANGO_USER_GROUP}")
                        else:
                            print(f"no archieve found")
                    else:
                        uploadStat=0
            else:
                print("input required for apiFolder name:- migrateApi() \n")
                return False
        except Exception as e:
            print(f"Term-UI-zip process failed:- {e}")
            return False








