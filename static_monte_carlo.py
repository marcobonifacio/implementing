"""
Chapter 1 of Implementing Models in Quantitative Finance:
Methods and Cases, by G. Fusai and A. Roncoroni
"""

from datetime import datetime
from math import cos, log, pi, sin
from statistics import mean
from typing import Generator, Tuple

# Monte Carlo method
# Steps:
# 1. Fix n "large"
# 2. Generate n samples of x, drawn from X
# 3. Return the sample mean estimation of x

def monte_carlo(
	n: int, x: Generator[float, None, None], *args
) -> float:
	"""
	Simulate a large number of random variables and return the sample mean.
	n: size of samples
	x: generator of random variables
	args: arguments to the generator function

	>>> monte_carlo(1000, uniform_sampling, 100)
	0.49591424044763943
	"""
	gen = x(*args)
	return mean(next(gen) for i in range(n))

# Estimation selection by efficiency rule
# Steps:
# 1. Fix a computational budget T
# 2. Minimize sigma^2*t

def efficiency_rule(
	data: Tuple[Tuple[float]]
) -> Tuple[int | float]:
	"""
	Calculate a minimum for efficiency rule.
	data: a tuple of tuples containing a pair of values: sigma^2 and t for each estimator
	return a tuple containing a positional index and a minimum

	>>> efficiency_rule(((0.12, 1.34), (0.01, 3.46)))
	(1, 0.0346)
	"""
	result = tuple(d[0] * d[1] for d in data)
	return result.index(min(result)), min(result)

# Uniform random variable generator
# Steps:
# 1, Fix integers modulus, multiplier, increment
# 2. Set up a seed between 0 and m - 1
# 3. Run the recursive rule x1 = (a * x + c) % m
# 4. Yield x1 / m beetween 0 and 1

def uniform_sampling(
	x0: int | None = None, a: int = 40_692,
	m: int = 2_147_483_399, c: int = 0
) -> Generator[float, None, None]:
	"""
	Draw a pseudo-random sample from a uniform distribution.
	Pseudo-random series formula:
		x_1 = (a * x_0 + c) % m
	x0: seed number (default: microseconds from datetime.now())
	a: multiplier (default: 40_692)
	m: denominator (default: 2_147_483_399)
	c: increment (default: 0)

	>>> u = uniform_sampling(100)
	>>> next(u)
	0.0018948691300220849
	>>> next(u)
	0.10601463885868205
	"""
	x0 = x0 or datetime.now().microsecond
	assert x0 >= 0 and x0 < m
	def modulus(x: int) -> int:
		return (a * x + c) % m
	while True:
		x0 = modulus(x0)
		yield x0 / m

# Stratified sampling techique
# Steps:
# 1. Fix integers number of bins and number of samples batches
# 2. Cycle over batches and bins, scaling a uniform random variable for bin

def stratified_sampling(
	M: int, k: int, *args
) -> Generator[float, None, None]:
	"""
	Draw pseudo-random uniform samples from stratifying bins.
	M: number of stratifying bins
	k: number of samples batches
	args: arguments for the uniform r.v. generator

	>>> s = stratified_sampling(10, 5, 100)
	>>> next(s)
	0.0001894869130022085
	>>> next(s)
	0.1106014638858682
	"""
	u = uniform_sampling(*args)
	return ((next(u) + i) / M for j in range(k) for i in range(M))

# Transformation methods: inverse transformation
# Steps:
# 1. Simulate a uniform random variable
# 2. Apply the inverse function

def exponential_sampling(
	lambda_: float = 1, *args
) -> Generator[float, None, None]:
	"""
	Draw a pseudo-random sample from an exponential distribution.
	lambda_: parameter of exponential distribution (default: 1)
	args: arguments for the uniform r.v. generator

	>>> e = exponential_sampling(1, 100)
	>>> next(e)
	6.268605503506907
	>>> next(e)
	2.2441780919649372
	"""
	u = uniform_sampling(*args)
	while True:
		yield -(1 / lambda_) * log(next(u)) 

# Transformation methods: multidimensional inverse transformation
# Steps:
# 1. Solve any admissible system of function on uniform variables
# 2. Simulate the uniform variables
# 3. Get the inverse function

# Not yet implemented

# Transformation methods: multivariate direct transformation
# Steps:
# 1. Generate uniform random variables
# 2. Return Box-Laplace transformation

def normal_sampling(
	*args
) -> Generator[Tuple[float], None, None]:
	"""
	Draw a couple of normal distributed samples from an uniform sampling
	args: arguments for the uniform r.v. generator

	>>> n = normal_sampling(100)
	>>> next(n)
	(2.783882890835916, 2.187968705700536)
	>>> next(n)
	(0.14858892424272413, 0.2922135170851708)
	"""
	u = uniform_sampling(*args)
	while True:
		u1 = next(u)
		u2 = next(u)
		yield (
			(-2 * log(u1)) ** .5 * cos(2 * pi * u2),
			(-2 * log(u1)) ** .5 * sin(2 * pi * u2)
		)

# Acceptance-rejection methods
# Steps:
# 1. Select a constant, a density function and a function
# 2. Simulate a uniform random variable
# 3. Simulate a random variable Y according to d.f.
# 4. If U > g(Y), go to step 2
# 5. Return Y

# Not yet implemented

# Hazard rate function method

# Not yet implemented

# Univariate normal distribution
# Steps:
# 1. Generate 12 uniform random variables
# 2. Sum up and differ from 6 to draw a standard normal r.v.

def normal_standard(
	*args
) -> Generator[float, None, None]:
	"""
	Draw a normal standard variable summing up uniform r.v.
	args: arguments for the uniform r.v. generator

	>>> ns = normal_standard(100)
	>>> next(ns)
	-0.7717555971663179
	>>> next(ns)
	0.2917233438413174
	"""
	u = uniform_sampling(*args)
	while True:
		yield sum(next(u) for n in range(12)) - 6


if __name__ == '__main__':
	import doctest
	doctest.testmod()
