import subprocess
class PostgresMgmnt:
    def __init__(self):
       pass

    def terminatePgCon(self,dbName):
        cmd=f"SELECT pg_terminate_backend (pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '{dbName}';"
        for i in range(5):
            self.executePostgres(cmd)

    def createDB(self,dbName):
        cmd=f"create database {dbName};"
        self.executePostgres(cmd)
    def dropDB(self,dbName):
        cmd =f"drop database {dbName}"
        self.executePostgres(cmd)
    def restoreDB(self,dbName,sourceFile):
        try:
          fullCommand = ["sudo", "-u", "postgres", "psql", "-d", dbName, "-f", sourceFile ]
          subprocess.run(fullCommand, check=True)
        except subprocess.CalledProcessError as e:
          print(f"Error in poastgres: {e}")

    def executePostgres(self,command):
        try:
          fullCommand = ["sudo", "-u", "postgres", "psql", "-c", command]
          subprocess.run(fullCommand, check=True)
        except subprocess.CalledProcessError as e:
          print(f"Error in poastgres: {e}")

    def createDbBackup(self,destinationPath,dbName):
        try:
            fullCommand = ["sudo", "-u", "postgres", "pg_dump", "-d", dbName, "--file", destinationPath]
            subprocess.run(fullCommand, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in poastgres: {e}")


        