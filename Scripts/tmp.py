# Scale with oscillation and decay
			scaleDecay = math.exp(-elapsedTime)  # Exponential decay
			scaleOscillation = 1 + 0.5 * math.sin(elapsedTime * 4 * math.pi)  # Oscillate scale
			scaleAmount = scaleDecay * scaleOscillation  # Combine decay and oscillation
			
			self.trans.setScale(scaleAmount, scaleAmount, scaleAmount)