from datetime import datetime
from typing import Generator

import numpy as np

# Uniform random variable generator
# Steps:
# 1, Fix integers modulus, multiplier, increment
# 2. Set up a seed between 0 and m - 1
# 3. Run the recursive rule x1 = (a * x + c) % m
# 4. Yield x1 / m beetween 0 and 1

def uniform_sampling(
	x0: int = datetime.now().microsecond, a: int = 40_692,
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
	"""
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
	M: int, k: int
) -> Generator[float, None, None]:
	"""
	Draw pseudo-random uniform samples from stratifying bins.
	M: number of stratifying bins
	k: number of samples batches
	"""
	u = uniform_sampling()
	return ((next(u) + i) / M for j in range(k) for i in range(M))

# Transformation methods: inverse transformation
# Steps:
# 1. Simulate a uniform random variable
# 2. Apply tje inverse function

def exponential_sampling(
	lambda_: float = 1
) -> Generator[float, None, None]:
	"""
	Draw a pseudo-random sample from an exponential distribution.
	lambda_: parameter of exponential distribution (default: 1)
	"""
	u = uniform_sampling()
	while True:
		yield -(1 / lambda_) * np.log(next(u)) 
