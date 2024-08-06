# Calculate elapsed time
elapsedTime = self.timer.get()

# Calculate alpha using sine function and map to range 0.0 to 0.5
alpha = 0.25 * (math.sin(elapsedTime * 2 * math.pi) + 1)  # Sine oscillates between -1 and 1

self.deathWarningOverlay.setDefaultQuadAlpha(alpha)