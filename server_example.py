import Pyro4

class GreetingMaker(object):
    def get_fortune(self, name):
        return "Hello, {0}. Here is your fortune message:\n" \
               "Behold the warranty -- the bold print giveth and the fine print taketh away.".format(name)

greeting_maker=GreetingMaker()
Pyro4.config.HOST="10.0.2.6"
daemon=Pyro4.Daemon()                 # make a Pyro daemon
ns=Pyro4.locateNS()                   # find the name server
uri=daemon.register(greeting_maker)   # register the greeting object as a Pyro object
ns.register("example.greeting", uri)  # register the object with a name in the name server

print "Ready."
daemon.requestLoop()                  # start the event loop of the server to wait for calls