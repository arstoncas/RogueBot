def paid(self, costs):
	if self.gold >= costs and costs >= 0:
		self.gold -= costs

		return True
	else:
		return False

def steal(self, price):
	self.gold = max(0, self.gold - price)

def found(self, gold):
  self.gold += gold