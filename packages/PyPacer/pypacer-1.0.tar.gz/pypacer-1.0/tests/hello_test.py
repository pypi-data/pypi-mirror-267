from PyPacer import CallableTimer

@CallableTimer
def hello() -> None:
	print("Hi, mom!")

if __name__ == "__main__":
	hello()
