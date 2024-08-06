import cave
import math

class HealthOrb(cave.Component):
	playerTag = "player"

	def start(self, scene: cave.Scene):
		self.orbMesh = self.entity.getChild("Mesh")
		self.orbMeshTrans = self.orbMesh.getTransform()
		self.orbMeshBody = self.orbMesh.get("Rigid Body")
		self.levitationTimer = cave.SceneTimer()
		self.scene = scene
		self.trans = self.entity.getTransform()

		self.dieTimer = cave.SceneTimer()
		self.dead = False

	def update(self):
		events = cave.getEvents()

		if self.dead:
			elapsedTime = self.dieTimer.get()
			if elapsedTime > 3:
				self.entity.kill()

			# Move up over 3 seconds
			moveAmount = (2 * elapsedTime) / 2
			self.trans.move(0, moveAmount * cave.getDeltaTime(), 0)

			# Scale with oscillation and decay
			scaleDecay = math.exp(-elapsedTime)  # Exponential decay
			scaleOscillation = 1 + 0.5 * cave.math.sin(elapsedTime * 4 * 3.1419)  # Oscillate scale
			scaleAmount = scaleDecay * scaleOscillation  # Combine decay and oscillation
			
			self.trans.setScale(scaleAmount, scaleAmount, scaleAmount)
			return

		val = 0.5 * cave.getDeltaTime()
		
		self.orbMeshTrans.rotate(val, val, val)

		elapsedTime = self.levitationTimer.get()
		levitationHeight = 0.01 * cave.math.sin(elapsedTime * 1 * 3.1419)

		currentPosition = self.orbMeshTrans.getPosition()

		newPosition = cave.Vector3(currentPosition.x, currentPosition.y + levitationHeight, currentPosition.z)
		self.orbMeshTrans.setPosition(newPosition)

		collisionInfos = self.scene.checkContactSphere(self.trans.getPosition(), 1)
		for info in collisionInfos:
			if info.entity is not None and info.entity.hasTag(self.playerTag):
				player = info.entity.getPy("PlayerController")
				if player.curHp < player.health:
					player.receiveHeal(10)
					self.die()
		
	def die(self):
		self.dead = True
		# self.orbMeshBody.disable() # does not exist
		self.dieTimer.reset()


		
	def end(self, scene: cave.Scene):
		pass
	
