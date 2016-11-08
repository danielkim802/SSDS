# class _fun(object):
# 	def __init__(self, f):
# 		self.funct = f

# 	def __call__(self, *args):
# 		return self.funct(*args)

# 	def __rrshift__(self, x):
# 		return self.funct(x)

# def __rrshift__(y, x):
# 	return y(x)

# l = lambda x: x+1

# incrall = _fun(lambda x: lambda y: map(lambda z: z+y, x))
# filtints = _fun(lambda x: filter(lambda y: type(y) == int, x))
# print [1, 2.0, 3, 4.0, 5, 6.0] >> incrall(1) >> filtints

class Operator(object):
	def __init__(self, funct):
		self.function = funct

	def __rrshift__(self, other):
		return Operator(lambda x: self.function(other, x))

	def __rshift__(self, other):
		return self.function(other)

	def __ror__(self, other):
		return Operator(lambda x: self.function(other, x))

	def __or__(self, other):
		return self.function(other)

	def __radd__(self, other):
		return Operator(lambda x: self.function(other, x))

	def __add__(self, other):
		return self.function(other)

	def __rmul__(self, other):
		return Operator(lambda x: self.function(other, x))

	def __mul__(self, other):
		return self.function(other)

	def __gt__(self, other):
		return self.function(other)

