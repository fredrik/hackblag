# Starting small

Lately I have been micro benchmarking my Python code to get a feel for how it
performs and behaves. This post will introduce a few benchmarking primitives
that I will build upon in later benchmark studies.

# Decorators

Python has got something called decorators. A decorator takes a functions as its
arguments and constructs a function, called wrapper below, that is executed in
place of the original function.

You attach a decorator to a function like so:

<pre>
def some_decorator(func):
	def wrapper(*arg):
		print 'executing %s.' % func.func_name
		func(*arg)
	return wrapper

@some_decorator
def f(x):
	print "x squared: %s" % x**2
</pre>

The wrapper function is responsible for calling f(). Seeing how we want to
benchmark some function f(), that might just turn out to be very useful!

# Timing a function

Imagine we wish to time f() to see how quick it is. Something like this would do
the job:

<pre>
# measure the execution time of a function.
def timing(func):
	def wrapper(*arg):
		t0 = time.time()
		r = func(*arg)
		elapsed = time.time() - t0
		print '%s => %0.3f ms' % (func.func_name, elapsed*1000.00)
		return r
	return wrapper
</pre>

What, for example, is the cost of printing a string to standard out?

<pre>
@timing
def a():
	print 'ok.'
</pre>	

Around 0.086 ms it turns out. Running the same benchmark a few more times gives
me executions times between 0.085 and 0.125 ms. Is this evidence that printing a
string will always cost us a tenth of a millisecond?

# Timing a function's average execution time.

Running the same function many times is likely to give us a more accurate
picture of how it performs. Assuming that the function yields no side effects,
the runs are guaranteed to be identical.

Here is a decorator that will run 'func' a hundred times and draw an average:

<pre>
# run the function 100 times, take the average.
def timingx100(func):
	n = 100
	def avg_wrapper(*arg):
		tot = 0
		for i in range(1, n):
			t0 = time.time()
			r = func(*arg)
			elapsed = time.time() - t0
			print '%s%s => %0.3f ms' % (func.func_name, arg, elapsed*1000.00)
			tot += elapsed
		avg = tot / n
		print 'average> %s => %0.3f ms' % (func.func_name, avg*1000.00)
	return avg_wrapper

@timingx100
def a():
	print 'ok.'
</pre>

The measurements:
<pre>
a() => 0.092 ms
a() => 0.040 ms
a() => 0.040 ms
a() => 0.038 ms
a() => 0.039 ms
a() => 0.039 ms
a() => 0.155 ms
a() => 0.073 ms
a() => 0.039 ms
a() => 0.039 ms
a() => 0.039 ms
[..]
average> a => 0.045 ms
</pre>

The first thing to notice is that first execution takes twice as long as do most
of the following. Running the same test repeatedly shows that this behaviour is
consistent; this is likely a pattern that we will see for most of what we
measure. "The process is not stable."

Also, while the average falls somewhere near 0.040 ms and most measures lie just
below that average, a few outliers fall far off at between 0.100 and 0.200 ms.
What causes these outliers? I don't know, but they occur frequently enough in
repeated tests that I draw the conclusion that they are not freak incidents.

The 'correct' number of times to run measurements differs between functions. Zed
Shaw has written [more about
this](http://www.zedshaw.com/essays/programmer_stats.html). I did confirm my
assumption that the deviation between runs would become smaller as the number of
measurements per run increased. At 100 000 runs, the average execution time
settled at around 0.100 ms - which is very close to the naive one-run
measurement we had from the beginning!

# Summary

This post has introduced a simple decorator-based timing mechanism. We have also
seen that running benchmarks a large number of times is a good thing.
