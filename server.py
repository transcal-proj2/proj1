from calculator import Calculator
from reader import Reader
from writer import Writer
from flask import Flask

server = Flask(__name__)

@server.route("/result")
def hello():
  reader = Reader()
  result = reader.read('./input.txt')
  calculator = Calculator(result)
  calculatedResult = calculator.getResult()
  Writer(calculatedResult)
  return calculator.getResultAsJSON()


server.run()
