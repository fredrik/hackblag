import time

# decorator for measuring execution time of a function.
def timing(func):
	def wrapper(*arg):
		t0 = time.time()
		r = func(*arg)
		elapsed = time.time() - t0
		print '%s => %0.3f ms' % (func.func_name, elapsed*1000.00)
		return r
	return wrapper

# run the function 100 times, take the average.
def timingx100(func):
	n = 1000
	def avg_wrapper(*arg):
		tot = 0
		emax = 0
		emin = 1000000000000.0
		for i in range(1, n):
			t0 = time.time()
			r = func(*arg)
			elapsed = time.time() - t0
			print '%s%s => %0.3f ms' % (func.func_name, arg, elapsed*1000.00)
			tot += elapsed
			if elapsed > emax:
				emax = elapsed
			if elapsed < emin:
					emin = elapsed
		avg = tot / n
		print 'average> %s => %0.3f ms' % (func.func_name, avg*1000.00)
		print 'min: %0.3f ms  max: %0.3f ms' % (emin*1000.00, emax*1000.00)
		# TODO: stddev, etc
	return avg_wrapper


@timingx100
def a0():
	print 'ok.'

# doing nothing 1024 times.
@timingx100
def a1():
	for i in range(1, 2**10):
		pass

@timingx100
def a2():
	str = ""
	for i in range(1, 2**20):
		str += "x"

@timingx100
def a3():
	s = []
	for i in range(1, 2**20):
		s.append("x")
	str = ''.join(s)

@timingx100
def f(x):
	print "x squared: %s" % x**2


if __name__ == '__main__':
	a0()
	a1()
	a2()
	a3()
	f()