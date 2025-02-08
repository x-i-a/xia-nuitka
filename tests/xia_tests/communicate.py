from xia_tests.multi import Language


class Communicate(Language):
    @classmethod
    def say_hello(cls):
        print("Hello World")
