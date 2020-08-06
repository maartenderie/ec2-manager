import psutil,datetime


HOST = "localhost"
PORT = 25565
MINIMUM_UPTIME_MINUTES = 10
MC_PROCESS_NAME = "java"
EC2_INSTANCE_ID = 'i-0429dce048b91b898'


def print_processes():
  for process in psutil.process_iter():
    print(process)

print_processes()
