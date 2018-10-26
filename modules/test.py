import grid
import cozmo

class Test:
    def __init__(self):
        self.grid = grid.Grid()

    def main(self):
        self.grid.printGrid()

if __name__ == "__main__":
    objName = Test()
    objName.main() 