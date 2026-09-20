class Car:
    def __init__(self, brand,model):
        self.__brand = brand 
        self.model = model
    def full_name(self):
        return f"{self.brand} {self.model}"
    def get_brand(self):
        return self.__brand
    def fuel_type(self):
        return "petrol or diesel"
    @staticmethod
    def get_found():
        return "lite hi h yrr zindagi badi h"
class ElectricCar(Car):
    def __init__(self, brand, model, battery_size):
        super().__init__(brand,model)
        self.battery_size = battery_size 
    def fuel_type(self):
        return 'electricity'

        
    
    
        
my_car = Car("Toyota", "Camry")
#print(my_car.brand)
print(my_car.model)  
#print(my_car.full_name()) 
my_electric_car = ElectricCar("Tesla", "Model 3", "77 KWh")     
zinvan = ElectricCar("Tesla", "Modfweel 3", "7e7 KWh")
#print(my_electric_car.__brand)
print(my_electric_car.model)
print(my_electric_car.battery_size)
print(my_electric_car.get_brand())
print(my_electric_car.fuel_type())
print(my_car.fuel_type())
print(zinvan.get_found())
print(my_car.get_found())