import logging

class Ademi:

    def __init__(self, name=None):
        if type(name) == str:
            self.name = name
        print(self.name)

if __name__ == "__main__":
    print('Launching Ademi')
    x = Ademi('Hello World app')
    print('Complete!')