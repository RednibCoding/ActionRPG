import cave

class EnemyMeleeCombatBehavior(cave.Component):
	health = 5
	sightRadius = 6.0
	runSpeed = 2.0
	hitRecoveryTime = 0.5
	playerTag = "player"

	def start(self, scene):
		self.scene = scene
		self.character = self.entity.get("Character")
		self.meshComponent = self.entity.getChild("Mesh").get("Mesh")
		self.healthbar = self.entity.getChild("HealthBar").get("UI Element")
		self.animator = self.entity.getChild("Mesh").get("Animation")
		self.dead = False
		self.curHp = self.health
		self.camera = cave.getCurrentScene().getCamera()
		self.deleteTimer = cave.SceneTimer()
		self.transform = self.entity.getTransform()
		self.isAttacking = False

		self.idleAnimName:str = self.entity.name.lower().strip() + "_idle"
		self.runAnimName:str = self.entity.name.lower().strip() + "_run"
		self.attackAnimName:str = self.entity.name.lower().strip() + "_attack"
		self.hitAnimName:str = self.entity.name.lower().strip() + "_hit"
		self.deathAnimName:str = self.entity.name.lower().strip() + "_death"

		self.recoveryFromHit = False#
		self.recoveryFromHitTimer = cave.SceneTimer()

		# entities with tag enemy can be attacked by the player
		self.entity.addTag("enemy")

		self.animator.playByName(self.idleAnimName, 0.1, 0, True)

	def update(self):
		events = cave.getEvents()
		self.entity.submitTransformToWorld()
		self.updateDeath()

		if self.recoveryFromHitTimer.get() > self.hitRecoveryTime:
			self.recoveryFromHit = False
			self.meshComponent.tint = cave.Vector4(1.0, 1.0, 1.0, 1.0)

		if not self.recoveryFromHit:
			self.updateChaseBehavior()

	def receiveDamage(self, amount: float):
		self.curHp -= amount
		if self.curHp < 0: self.curHp = 0

		self.updateHpBar()

		self.recoveryFromHit = True
		self.recoveryFromHitTimer.reset()
		self.meshComponent.tint = cave.Vector4(1.0, 0.5, 0.5, 1.0)
		
		if self.curHp == 0:
			self.die()
		else:
			self.animator.playByName(self.hitAnimName, 0.1, 0, False)

	
	def die(self):
		if not self.dead:
			self.animator.playByName(self.deathAnimName, 0.1, 0, False)
			self.dead = True
			self.character.disable()
			self.deleteTimer.reset()

	def updateDeath(self):
		if self.dead:
			elapsedTime = self.deleteTimer.get()
			
			# let sink the corpse into the ground over 11 seconds
			if elapsedTime > 5.0 and elapsedTime <= 11.0:
				pos = self.transform.getPosition()
				self.transform.setPosition(pos.x, pos.y-0.002, pos.z)
			
			if elapsedTime > 11.0:
				self.entity.kill()

	
	def updateHpBar(self):
		newZScale = 0.04 * (self.curHp / self.health)
		self.healthbar.scale = cave.UIVector(newZScale, 0.01)

		# hpPercent = (self.curHp / self.health) * 100

		if self.curHp <= 0:
			self.healthbar.setDefaultQuadAlpha(0.0)

	def updateChaseBehavior(self):
		if self.dead: return
		collisionInfo = self.scene.checkContactSphere(self.transform.getPosition(), self.sightRadius)
		playerInSight = False
		for collision in collisionInfo:
			if collision.entity.hasTag(self.playerTag):
				playerInSight = True
				break
		
		if playerInSight:
			targetPosition = collision.entity.getTransform().getWorldPosition()
			selfPos = self.transform.getWorldPosition()
			direction = (selfPos - targetPosition).normalized()
			self.transform.lookAtSmooth(direction, 0.2)
			
			distanceToTarget = (targetPosition - selfPos).length()

			if distanceToTarget > 1.5:
				# self.character.setWalkDirection(direction * self.runSpeed * cave.getDeltaTime())
				self.transform.move(0, 0, self.runSpeed * cave.getDeltaTime())
				self.animator.playByName(self.runAnimName, 0.1, 0, True)
			else:
				self.animator.playByName(self.attackAnimName, 0.1, 0, True)
				# self.character.setWalkDirection(0, 0, 0)
		else:
			self.animator.playByName(self.idleAnimName, 0.1, 0, True)
			# self.character.setWalkDirection(0, 0, 0)

					
	
		
	def end(self, scene):
		pass