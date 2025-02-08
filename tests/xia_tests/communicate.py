from xia_tests import Language


class Communicate(Language):
    @classmethod
    def say_hello(cls):
        print("Hello World")
