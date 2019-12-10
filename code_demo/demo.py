class Demo:
    @staticmethod
    def addition(a, b):
        addition = a + b
        if b == 0:
            print('b is zero')
        if b > 0:
            print('b is an positive integer')
        else:
            print('b is a negative integer')
        return addition

    @staticmethod
    def subtraction(a, b):
        subtraction = a - b
        if b == 0:
            print('b is zero')
        if b > 0:
            print('b is an positive integer')
        else:
            print('b is a negative integer')
        return subtraction
