from mcstatus import MinecraftServer

# If you know the host and port, you may skip this and use MinecraftServer("example.org", 1234)
server = MinecraftServer.lookup("localhost")

status = server.status()
print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))
