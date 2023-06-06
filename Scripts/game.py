from car import Car

class Game:
    
    def __init__(self, file_name: str) -> None:
    	self.cars: dict[str, Car]= {}
    	self.load_cars(file_name)
    	
    def load_cars(file_name: str) -> None:
    	# Append self.cars with all cars in filename csv
    	pass
