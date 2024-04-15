import time
from typing import Callable
from functools import wraps

def CallableTimer(roundoff: int=5) -> Callable:
	def timetracker(callable: Callable) -> Callable:
		@wraps(callable)
		def wrapper(*args, **kwargs):
			start = time.time()
			result = callable(*args, **kwargs)
			took = round((time.time() - start), roundoff)
			print(f"{callable.__name__} took {took} seconds to run")
			return result
		return wrapper
	return timetracker