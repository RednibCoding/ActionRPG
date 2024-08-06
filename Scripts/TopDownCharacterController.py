import cave

class PlayerController(cave.Component):
	health = 20.0
	runSpeed = 4.0
	hitRecoveryTime = 0.2
	enemyTag = "enemy"

	def start(self, scene):
		self.transform = self.entity.getTransform()
		self.character = self.entity.get("Character")
		self.mesh = self.entity.getChild("Mesh")
		self.meshComponent = self.mesh.get("Mesh")
		self.meshTransform = self.mesh.getTransform()
		self.animator = self.mesh.get("Animation")
		self.currentAnimation = "dwarf_idle"
		self.isShooting = False
		self.camera = scene.getCamera()
		self.mouseRayCast: cave.RayCastOut = None
		self.scene = scene
		self.window = cave.getWindow()
		self.selectionCircle = self.scene.get("SelectionCircle")
		self.isAttacking = False

		self.healthbar = self.entity.getChild("UI").getChild("HealthBar").get("UI Element")
		self.deathWarningOverlay = self.entity.getChild("UI").getChild("DeathWarning").get("UI Element")

		self.idleAnimName:str = self.entity.name.lower().strip() + "_idle"
		self.runAnimName:str = self.entity.name.lower().strip() + "_run"
		self.attack1AnimName:str = self.entity.name.lower().strip() + "_attack1"
		self.powerAnimName:str = self.entity.name.lower().strip() + "_power"
		self.hitAnimName:str = self.entity.name.lower().strip() + "_hit"
		self.deathAnimName:str = self.entity.name.lower().strip() + "_death"

		self.curHp = self.health

		self.recoveryFromHit = False
		self.recoveryFromHitTimer = cave.SceneTimer()

		self.dead = False
		self.dieTimer = cave.SceneTimer()

		self.deathWarningPulseTimer = cave.SceneTimer()

	def update(self):
		events = cave.getEvents()
		self.dt = cave.getDeltaTime()

		self.updateHpBarAndDeathWarning()
		
		if self.dead:
			if self.dieTimer.get() > 0.2:
				self.entity.removeTag("player")
				self.meshComponent.tint = cave.Vector4(1.0, 1.0, 1.0, 1.0)
			return

		if self.recoveryFromHitTimer.get() > self.hitRecoveryTime:
			self.recoveryFromHit = False
			self.meshComponent.tint = cave.Vector4(1.0, 1.0, 1.0, 1.0)
		
		if self.isAttacking:
			self.currentAnimation = self.attack1AnimName
		else:
			self.currentAnimation = self.idleAnimName

		if events.active(cave.event.MOUSE_LEFT):
			self.mouseRayCast = self.castMouseRay()

			
		if self.mouseRayCast is not None:
			selfPos = self.transform.getWorldPosition()
			selfPosVec = cave.Vector3(selfPos.x, 0, selfPos.z)

			isEnemyTarget = False

			if self.mouseRayCast.entity != None and self.mouseRayCast.entity.hasTag(self.enemyTag):
				isEnemyTarget = True
				targetEntityPos = self.mouseRayCast.entity.getTransform().getPosition()
				self.mouseRayCast.position = cave.Vector3(targetEntityPos.x, 0, targetEntityPos.z)

			targetPosVec =  cave.Vector3(self.mouseRayCast.position.x, 0, self.mouseRayCast.position.z) 

			if isEnemyTarget:
				self.selectionCircle.getTransform().setPosition(targetPosVec.x, 0.01, targetPosVec.z)
			else:
				self.selectionCircle.getTransform().setPosition(0, -100, 0)
				
			
			distanceToTarget = (targetPosVec - selfPosVec).length()

			direction = (targetPosVec - selfPosVec).normalized()
			self.meshTransform.lookAtSmooth(-direction, 0.2)

			if distanceToTarget > 1.5: # check if target location has been reached
				self.currentAnimation = self.runAnimName
				self.isAttacking = False
				self.character.setWalkDirection(direction * self.runSpeed * self.dt)
			else:
				self.character.setWalkDirection(0, 0, 0)
				if self.mouseRayCast.entity.hasTag(self.enemyTag):
					self.isAttacking = True
				else:
					self.isAttacking = False
					self.selectionCircle.getTransform().setPosition(0, -100, 0)
					self.mouseRayCast = None

		if events.active(cave.event.KEY_SPACE):
			self.currentAnimation = self.powerAnimName
		
		self.animator.playByName(self.currentAnimation, 0.1, 0, True)
	
	def receiveDamage(self, amount):
		self.curHp -= amount
		if self.curHp < 0: self.curHp = 0

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
			self.dieTimer.reset()
			self.character.disable()

	def updateHpBarAndDeathWarning(self):
		newXScale = 0.07 * (self.curHp / self.health)
		self.healthbar.scale = cave.UIVector(newXScale, 0.0165)

		hpPercent = (self.curHp / self.health) * 100

		self.healthbar.setDefaultQuadColor(cave.Vector3(0.0, 1.0, 0.0))
		self.deathWarningOverlay.setDefaultQuadAlpha(0.0)

		if hpPercent < 50 and hpPercent > 35:
			self.healthbar.setDefaultQuadColor(cave.Vector3(1.0, 1.0, 0.0))
		elif hpPercent < 35:
			self.healthbar.setDefaultQuadColor(cave.Vector3(1.0, 0.0, 0.0))

			# pulsating warning overlay
			elapsedTime = self.deathWarningPulseTimer.get()
			# Calculate alpha using sine function and map to range 0.1 to 0.5
			alpha = 0.1 + 0.2 * (cave.math.sin(elapsedTime * 1 * 3.1419) + 1)
			self.deathWarningOverlay.setDefaultQuadAlpha(alpha)

		if self.curHp <= 0:
			self.healthbar.setDefaultQuadAlpha(0.0)
		else:
			self.healthbar.setDefaultQuadAlpha(0.6)


	def end(self, scene):
		pass

	def castMouseRay(self) -> cave.RayCastOut:
		if self.dead: return
		mousePos = cave.getMousePosition()
		mxn = mousePos.x / self.window.getWindowSize().x
		myn = mousePos.y / self.window.getWindowSize().y
		rayPos = self.camera.getScreenRay(mxn, myn)
		camPos = self.camera.getWorldPosition()
		out = self.scene.rayCast(camPos, camPos + rayPos * 1000)
		
		if not out.hit:
			return None

		return out







































































































































