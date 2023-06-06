from car import Car

class Game:
    
    def __init__(self, file_name: str) -> None:
    	self.cars: dict[str, Car]= {}
