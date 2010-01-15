def some_decorator(func):
	def wrapper(*arg):
		print 'executing %s.' % func.func_name
		func(*arg)
	return wrapper

@some_decorator
def f(x):
	y = x ** 2
	print "x squared: %s" % y

if __name__ == "__main__":
	f(4)
