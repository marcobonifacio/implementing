from datetime import datetime
from typing import Generator

def uniform(
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

def stratified_sampling(
	M: int, k: int
) -> Generator[float, None, None]:
	"""
	Draw pseudo-random uniform samples from stratifying bins.
	M: number of stratifying bins
	k: number of samples batches
	"""
	u = uniform()
	return ((next(u) + i) / M for j in range(k) for i in range(M))
