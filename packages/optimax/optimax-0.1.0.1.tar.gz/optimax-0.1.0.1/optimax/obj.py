class Car:
    def _init_(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = 0
    
    def drive(self, distance):
        self.mileage += distance
        print(f"The {self.year} {self.make} {self.model} has now driven {self.mileage} miles.")