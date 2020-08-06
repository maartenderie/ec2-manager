import psutil,datetime


HOST = "localhost"
PORT = 25565
MINIMUM_UPTIME_MINUTES = 10
MC_PROCESS_NAME = "java"
EC2_INSTANCE_ID = 'i-0429dce048b91b898'


def get_process(name):
  for process in psutil.process_iter():
    if name == process.name():
      return process
  return None


def get_uptime( process ):
  now = datetime.datetime.now().timestamp()
  return now - process.create_time()


def get_nr_players():
  from mcstatus import MinecraftServer
  server = MinecraftServer(HOST,PORT)
  return server.status().players.online


def shutdown_ec2():
  print("TODO should I stop the MC server?")
  import boto3
  ec2 = boto3.client('ec2')
  ec2.stop_instances(InstanceIds=[EC2_INSTANCE_ID])


def update_last_seen_user():
  my_file = open('last-seen-user.txt', 'w')
  my_file.write( "" + str(int(datetime.datetime.now().timestamp())))
  my_file.close()

def get_last_seen_user():
  my_file = open('last-seen-user.txt','r')
  result = int(my_file.read())
  my_file.close()
  return result


if len(psutil.users()) > 0:
  print("An ssh session is still open, won't shutdown" )
  update_last_seen_user()
  exit(0)

mc_process = get_process(MC_PROCESS_NAME)
#backup_process = get_process('bash')

if None is mc_process:
  print("MC is not running, let's stop")
  shutdown_ec2()

elif get_nr_players() > 0:
  print( "Someone is using the server.")
  update_last_seen_user()

elif get_uptime( mc_process) < MINIMUM_UPTIME_MINUTES*60:
  print(f"Server hasn't been running for {MINIMUM_UPTIME_MINUTES} minutes ({get_uptime(mc_process)})")

elif datetime.datetime.now().timestamp() - get_last_seen_user() < 5*60:
  print("Server has been visited less than 2 minutes ago")

else:
  print( f"Noone is using the server AND more than {MINIMUM_UPTIME_MINUTES} minutes have elapsed: shuting down")
  shutdown_ec2()
