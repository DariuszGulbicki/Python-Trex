from binder import Binder

class ConsoleBinder(Binder):

    def send(self, scopes):
        for scope in scopes:
            print(scope["name"] + ": " + scope["value"])