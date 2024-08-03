"""
no changes needed
"""

# Python Stub File for the Cave Engine's RANDOM API
# The code here is available at cave.random. submodule
import cave

def seed(newSeed: int) -> None: ...

def random() -> float: ...						# Returns a random value between [0.0, 1.0]
def randint(a: int, b: int) -> int: ...			# Returns a random int between [a, b]
def uniform(a: float, b: float) -> float: ...	# Returns a random float between [a, b]

# Perlin Noise functions:
def perlin(x: float) -> float: ...	
def perlin(x: float, y: float) -> float: ...	
def perlin(x: float, y: float, z: float) -> float: ...	

def perlin(pos : cave.Vector2) -> float: ...
def perlin(pos : cave.Vector3) -> float: ...