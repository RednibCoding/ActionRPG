import cave

# This script will display the UI Element Component at its Entity as a 3D sprite.
# You can specify an offset (if you want to adjust the position of the 3D sprite relative to the entity, e.g., above the head, etc.).
#
# ClampX and ClampY are used to clamp the 3D sprite on the canvas inside an area smaller than the screen. Values from 0.0 to 1.0 are allowed.
#
# The entity that contains this script as Python component must also contain the UI Element (your image etc. you want to display) since this script
# tries to reference it

class Sprite3d(cave.Component):
	offsetX = 0.0
	offsetY = 1.0
	offsetZ = 0.0
	clampX = 0.0
	clampY = 0.0

	def start(self, scene):
		self.display = self.entity.get("UI Element")
		if self.display is None:
			print("You have to create a UI Element component first\nAdd a UI Element component to the entity that contains this script!")
		self.transform = self.tryGetTransform()

	def update(self):
		events = cave.getEvents()

		cam = self.entity.getScene().getCamera()
		worldPos = self.transform.getWorldPosition() + cave.Vector3(self.offsetX, self.offsetY, self.offsetZ)
		screenPos = cam.getScreenPos(worldPos)

		# UI Elements use a different coordinate system, so we have to convert to it
		screenPos -= cave.Vector2(0.5)
		screenPos.y *= -1.0

		if self.clampX > 0.0:
			screenPos.x = cave.math.clamp(screenPos.x, -self.clampX, self.clampX)
		if self.clampY > 0.0:
			screenPos.y = cave.math.clamp(screenPos.y, -self.clampY, self.clampY)

		self.display.position = cave.UIVector(screenPos.x, screenPos.y)

	def end(self, scene):
		pass
	
	def tryGetTransform(self) -> cave.Transform:
		root_parent = self.entity.getRootParent()
		if root_parent:
			return root_parent.getTransform()
		else:
			parent = self.entity.getParent()
			if parent:
				return parent.getTransform()
			else:
				return self.entity.getTransform()
