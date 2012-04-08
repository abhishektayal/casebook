import Pyro4

name=raw_input("What is your name? ").strip()

greeting_maker=Pyro4.Proxy("PYRONAME:example.greeting")    # use name server object lookup uri shortcut
print greeting_maker.get_fortune(name)