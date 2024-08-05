import cave

class Player(cave.Component):
	def start(self, scene):
		self.runSpeed = 4
		self.transform = self.entity.getTransform()
		self.character = self.entity.get("Character")
		self.mesh = self.entity.getChild("Mesh")
		self.meshTransform = self.mesh.getTransform()
		self.animator = self.mesh.get("Animation")
		self.currentAnimation = "dwarf_idle"
		self.isShooting = False
		self.camera = scene.getCamera()
		self.mouseRayCast: cave.RayCastOut = None
		self.scene = scene
		self.window = cave.getWindow()
		self.indicator = self.scene.get("Indicator")
		self.isAttacking = False
		self.attackArea = self.entity.getChild("AttackArea")
		self.attackAreaBody = self.attackArea.get("Rigid Body")

	def update(self):
		events = cave.getEvents()
		self.dt = cave.getDeltaTime()
		
		# we need to call this to update the position of the rigid body of the attack collision area
		self.attackArea.submitTransformToWorld()
		
		if self.isAttacking:
			self.currentAnimation = "dwarf_attack1"
		else:
			self.currentAnimation = "dwarf_idle"

		if events.active(cave.event.MOUSE_LEFT):
			self.mouseRayCast = self.castMouseRay()

		if events.released(cave.event.MOUSE_LEFT):
			# self.mouseRayCast = None
			# self.isAttacking = False
			pass
			
		if self.mouseRayCast is not None:
			selfPos = self.transform.getWorldPosition()
			selfPosVec = cave.Vector3(selfPos.x, 0, selfPos.z)

			targetPosition =  cave.Vector3(self.mouseRayCast.position.x, 0, self.mouseRayCast.position.z) 
			
			if cave.hasEditor():
				self.indicator.getTransform().setPosition(targetPosition.x, 0, targetPosition.z)
			else:
				self.indicator.kill()
			
			distanceToTarget = (targetPosition - selfPosVec).length()

			if distanceToTarget > 1: # check if target location has been reached
				self.currentAnimation = "dwarf_run"
				self.isAttacking = False
				direction = (targetPosition - selfPosVec).normalized()
				self.meshTransform.lookAtSmooth(-direction, 0.2)
				self.character.setWalkDirection(direction * self.runSpeed * self.dt)
			else:
				self.character.setWalkDirection(0, 0, 0)
				if self.mouseRayCast.entity.hasTag("enemy"):
					self.isAttacking = True
				else:
					self.isAttacking = False
					self.mouseRayCast = None
				
		else:
			# self.character.setWalkDirection(0, 0, 0)
			pass

		if events.active(cave.event.KEY_SPACE):
			self.currentAnimation = "dwarf_power"
		
		self.animator.playByName(self.currentAnimation, 0.1, 0, True)


	def end(self, scene):
		pass

	def castMouseRay(self) -> cave.RayCastOut:
		mousePos = cave.getMousePosition()
		mxn = mousePos.x / self.window.getWindowSize().x
		myn = mousePos.y / self.window.getWindowSize().y
		rayPos = self.camera.getScreenRay(mxn, myn)
		camPos = self.camera.getWorldPosition()
		out = self.scene.rayCast(camPos, camPos + rayPos * 1000)
		
		if not out.hit:
			return None

		return out







































































































































