import subprocess


class PortManager:
    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.ports = set()

    def initializePorts(self, startPort, numPorts, increment):
        try:
            self.ports = list(range(startPort, startPort + numPorts * increment, increment))
            with open(self.filepath, 'w') as file:
                for port in self.ports:
                    file.write(f"{port}\n")
            return True
        except Exception as e:
            print(f"An error occurred during port initialization: {e}")

            return False
    def isPortInUse(self,port):
        try:
            subprocess.run(['fuser', str(port)+'/tcp'], check=True)
            print(f'The port {port} is in use.')
            return True
        except subprocess.CalledProcessError as e:
            print(f'The port {port} is not in use.')
            return False
    def getPortFromProject(self, portFilePath):
        try:
            with open(portFilePath, 'r') as file:
                return int(file.read().strip())
        except Exception as e:
            print(f"An error occurred while getting port: {e}")
            return False

    def setPortToProject(self, port, portFilePath):
        try:
            with open(portFilePath, 'w') as file:
                file.write(f"{port}\n")
            return True
        except Exception as e:
            print(f"An error occurred while setting port: {e}")
            return False

    def initializeIncrPorts(self, startPort, numPorts):
        try:
            # Create a set of unique ports
            self.ports = set(range(startPort, startPort + numPorts))

            # Write the ports to the file
            with open(self.filepath, 'w') as file:
                for port in self.ports:
                    file.write(f"{port}\n")
            return True
        except Exception as e:
            print(f"An error occurred during incremental port initialization: {e}")
            return False

    def readAllPorts(self):
        try:
            with open(self.filepath, 'r') as file:
                self.ports = set(map(int, file.read().splitlines()))
        except FileNotFoundError:
            print(f"File not found: {self.filepath}")
            self.ports = set()
        except ValueError:
            print(f"Error reading ports from file: {self.filepath}")
            self.ports = set()

    def readNextPort(self):
        try:
            self.readAllPorts()
            with open(self.filepath, 'r') as file:
                lines = file.readlines()
                if lines:
                    nextPort = int(lines[0].strip())
                    return nextPort
                else:
                    print("No more ports available.")
                    return None
        except Exception as e:
            print(f"An error occurred while reading the next port: {e}")
            return False

    def removePort(self, port):
        try:
            self.readAllPorts()
            self.ports.remove(port)
            with open(self.filepath, 'w') as file:
                for p in self.ports:
                    file.write(f"{p}\n")
            return True
        except Exception as e:
            print(f"exception in removePort:- {e}")
            return False
