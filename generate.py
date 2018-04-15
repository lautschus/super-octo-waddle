from . import Wood,Rock,Axe,Fuel,Apple#,Electricity
from . import ids
def Generate(id,location):

	if id == ids.WoodID:
		item = Wood.Wood(location.updates)
		location.addItem(item)

	elif id == ids.RockID:
		item = Rock.Rock(location.updates)
		location.addItem(item)

	elif id == ids.AxeID:
		item = Axe.Axe(location.updates)
		location.addItem(item)

	elif id == ids.FuelID:
		item = Fuel.Fuel(location.updates)
		location.addItem(item)

	elif id == ids.AppleID:
		item = Apple.Apple(location.updates)
		location.addItem(item)

	# elif id == Electricity.id:
		# item = Electricity.Electricity(location.updates)
		# location.addItem(item)