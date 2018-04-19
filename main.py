from calculator import Calculator
from reader import Reader
from writer import Writer

reader = Reader()
result = reader.read('./entradarelatorio.txt')
calculator = Calculator(result)
calculatedResult = calculator.getResult()
Writer(calculatedResult)