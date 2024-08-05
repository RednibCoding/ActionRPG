import cave

class EnemyCombatBehavior(cave.Component):
	def start(self, scene):
		self.character = self.entity.get("Character")
		self.mesh = self.entity.getChild("Mesh").get("Mesh")
		self.hpBar = self.entity.getChild("HpBar")
		self.hpBarTransform= self.hpBar.getTransform()
		self.hpBarBack = self.entity.getChild("HpBarBack")
		self.hpBarBackTransform= self.hpBarBack.getTransform()
		self.animator = self.entity.getChild("Mesh").get("Animation")
		self.death = False
		self.maxHp = 5
		self.hp = self.maxHp
		self.camera = cave.getCurrentScene().getCamera()
		self.deleteTimer = cave.SceneTimer()

	def update(self):
		events = cave.getEvents()
		hpBarPos = self.hpBarTransform.getPosition()
		cameraPos = self.camera.getWorldPosition()
		direction = (cameraPos - hpBarPos).normalized()
		self.hpBarTransform.lookAt(cave.Vector3(direction.x, 0, 0))
		self.hpBarBackTransform.lookAt(cave.Vector3(direction.x, 0, 0))

		self.updateDeath()

	def receiveDamage(self, amount: float):
		self.hp -= amount
		if self.hp < 0: self.hp = 0

		self.updateHpBar()
		
		if self.hp == 0:
			self.die()
		else:
			self.animator.playByName("archer_hit", 0.1, 0, False)

	
	def die(self):
		print("die")
		if not self.death:
			self.animator.playByName("archer_death", 0.1, 0, False)
			self.death = True
			self.deleteTimer.reset()

	def updateDeath(self):
		if self.death:
			elapsedTime = self.deleteTimer.get()
			
			if elapsedTime > 5.0 and elapsedTime <= 8.0:
				# Calculate the alpha value to gradually decrease from 1.0 to 0.0 over 3 seconds (from 5s to 8s)
				alpha = 1.0 - (elapsedTime - 5.0) / 3.0
				self.mesh.tint = cave.Vector4(1.0, 1.0, 1.0, alpha)
			
			if elapsedTime > 8.0:
				self.entity.kill()

	
	def updateHpBar(self):
		newZScale = 0.4 * (self.hp / self.maxHp)
		self.hpBarTransform.setScale(0.05, 0.05, newZScale)

		# hpPercent = (self.hp / self.maxHp) * 100

		if self.hp <= 0:
			self.hpBar.kill()
			self.hpBarBack.kill()

	def updateChaseBehavior(self):
		pass
		
	def end(self, scene):
		pass