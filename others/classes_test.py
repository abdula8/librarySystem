

class Calculator:
    def __init__(self, ina, inb):
        self.a = ina
        self.b = inb
    def add(self):
        return self.a + self.b
    def mul(self):
        return self.a*self.b

class Scientific(Calculator):
    def power(self):
        return pow(self.a, self.b)

newCalculation = Calculator(10, 20)
print("a+b: %d" %newCalculation.add())
print("a+b: %d" %newCalculation.mul())


new_power = Scientific(2, 3)
print("a+b: %d" %new_power.add())
print("a+b: %d" %new_power.mul())
print("a+b: %d" %new_power.power())

























