#!/usr/bin/python3
from CLS_Starter import Starter
import sys
from os.path import join
import  os
from CLS_Constants import DJANGO_UPLOAD,EXCLUDE_FILES,DJANGO_PROJECT_DIR
from CLS_Utils import UtilesDjango

try:
    if(sys.argv[1]=="init"):
        Starter().initDjangoEnv()
    elif(sys.argv[1]=="start"):
        exit_lp=1
        while(exit_lp):
            try:
                stat=int(input(f"1)create Project\n  2) Add API to Project\n  3)Update API\n4)Create DB\n5)Restore DB\n6) Install SSL\n7)Reload Supervisor0)Exit\n"))
                if(stat==1):
                    currentProject=Starter().initProject()
                    if(currentProject):
                        if(input("Setup API now? Y/N\n").lower()=='y'):
                            apiDataArray=Starter().initApiConfiguration(Starter().initAPI(currentProject))
                            if(input("Import Backend and Frontend Files Y/N ?\n").lower()=='y'):
                                if(Starter().migrateApi(apiDataArray[-1])):
                                    if(input("Create DB and restore DB now Y/N ?\n").lower()=='y'):
                                        Starter().migrateDb(apiDataArray[-1],input("\nEnter the Database name\n"))
                    UtilesDjango().clear()
                elif(stat==2):
                    projectName=Starter().uiSelection(DJANGO_PROJECT_DIR,EXCLUDE_FILES)
                    apiDataArray=Starter().initApiConfiguration(Starter().initAPI(projectName))
                    if(apiDataArray):
                        if(input("Import Backend and Frontend Files Y/N ?\n").lower()=='Y'):
                            if(Starter().migrateApi(apiDataArray[-1])):
                                if(input("restore DB now Y/N ?\n").lower()=='y'):
                                    Starter().migrateDb(apiDataArray[-1],input("\nEnter the Database name\n"))
                            if(input("Do you want to install SSL now Y/N ?\n").lower()=='Y'):
                                Starter().installSSL(input("Enter the domain\n"))
                    UtilesDjango().clear()
                elif(stat==3):
                    pName=Starter().uiSelection(DJANGO_PROJECT_DIR,EXCLUDE_FILES)
                    Starter().migrateApi(Starter().uiSelection(join(DJANGO_PROJECT_DIR,pName),EXCLUDE_FILES))
                    UtilesDjango().clear()
                elif(stat==4):
                    if(Starter().createDb(input("input DB name\n"))):
                        print(f"created DB\n")
                    UtilesDjango().clear()
                elif(stat==5):
                    pName=Starter().uiSelection(DJANGO_PROJECT_DIR,EXCLUDE_FILES)
                    apiFolder=Starter().uiSelection(join(DJANGO_PROJECT_DIR,pName),EXCLUDE_FILES)
                    if(apiFolder):
                        dump=f"{apiFolder}.sql"
                        print(f"backup Files required to be uploaded to /upload\n fileName:- {dump}\n")

                        Starter().restoreDb(input("enter DB name"),os.path.join(DJANGO_UPLOAD,dump))
                    # UtilesDjango().clear()
                elif(stat==6):
                    if(Starter().installSSL(input("Enter the Domain\n"))):
                        print(f"done\n")
                    UtilesDjango().clear()
                elif(stat==7):
                    Starter().reloadSuperVisor()
                    UtilesDjango().clear()
                else:
                    exit_lp=0
            except Exception as e:
                print(f"invalid input, please try again\n")
                UtilesDjango().clear()


    elif(sys.argv[1]=="postgres"):
        if(sys.arg[2]):
            if(sys.argv[3]):
                Starter().restoreDb(sys.argv[2],sys[3])
            else:
                print("require- DB backup file path\n")
                print("cmd:- ScriptName postgres dbname /backup.sql\n")
        else:
            print("require Db name\n")
            print("cmd:- ScriptName postgres dbname /backup.sql\n")

    elif(sys.argv[1]=="api"):
        if(sys.arg[2]):
            if(sys.argv[3]):
                Starter().updateApiCode(sys.argv[2],sys[3])
            else:
                print("require destination absolute path\n")
                print(" cmd:- scriptName src/file.zip /destination-path\n")
        else:
            print("require zip file path\n")
            print(" cmd:- scriptName src/file.zip /destination-path\n")
    else:
        print("invalid input")
except Exception as e:
    print(f"Available commands\n")
    print(f"init - Install Django environment/reset current PortPool\n")
    print(f"start - Set up new Project or add API to Project\n")

    print(f"{e}\n")