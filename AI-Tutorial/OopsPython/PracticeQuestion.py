class ComplexNumber:
    def __init__(self, real, imaginary):
        self.real = real 
        self.imaginary = imaginary
        
    def __add__(self, other):
    
        other.real = other.real
        other.imaginary = other.imaginary
        return ComplexNumber(self.real + other.real, self.imaginary + other.imaginary)
    def __str__(self):
        return f"{self.real} + {self.imaginary}i"
c1 = ComplexNumber(2, 3)
c2 = ComplexNumber(4, 5)
c3 = c1 + c2
print(c3)