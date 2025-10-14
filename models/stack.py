class Stack:
    def __init__(self, *args):
        self.list = list()
        self.__load(*args)

    def __str__(self):
        return str(self.list)

    def __load(self, *args):
        for arg in args:
            self.list.append(arg)

    def pop(self) -> object:
        return self.list.pop(0)

    def push(self, element: object) -> object:
        self.list.append(element)
        return element

    def peek(self):
        return self.list[-1]
