# Try to get the root parent's transform
root_parent = self.entity.getRootParent()
if root_parent:
	self.transf = root_parent.getTransform()
else:
	# If no root parent, try to get the parent's transform
	parent = self.entity.getParent()
	if parent:
		self.transf = parent.getTransform()
	else:
		# If neither root parent nor parent, use the entity's own transform
		self.transf = self.entity.getTransform()