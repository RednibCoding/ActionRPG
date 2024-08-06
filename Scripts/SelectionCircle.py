import cave

class SelectionCircle(cave.Component):
	def start(self, scene):
		self.transform = self.entity.getTransform()

	def update(self):
		events = cave.getEvents()
		self.transform.rotate(0, 1 * cave.getDeltaTime(), 0)
		
	def end(self, scene):
		pass
	
