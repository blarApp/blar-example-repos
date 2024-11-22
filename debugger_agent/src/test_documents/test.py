class Test:
    def hello(self):
        def hello2():
            self.fibonacci(2)
            print("Hello, world! 2")

        hello2()
        self.hello2()
        a = 1
        print("Hello, world!")

    def factorial(self, n):
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result

    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    def hello2(self):
        print("hc")


test = Test()
test.hello()
