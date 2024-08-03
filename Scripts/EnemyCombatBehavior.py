import cave

class EnemyCombatBehavior(cave.Component):
	def start(self, scene):
		self.character = self.entity.get("Character")
		self.mesh = self.entity.getChild("Mesh")
		self.animator = self.mesh.get("Animation")

	def update(self):
		events = cave.getEvents()
	
	def receiveDamage(self, amount: float):
		self.animator.playByName("archer_hit", 0.1, 0, False)
		
	def end(self, scene):
		pass
	





























