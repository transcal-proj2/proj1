from calculator import Calculator
from reader import Reader
from writer import Writer

reader = Reader()
result = reader.read('./input-test.txt')
calculator = Calculator(result)
calculatedResult = calculator.getResult()

Writer(calculatedResult)



