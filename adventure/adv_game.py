"""Adventure game clues.

This module provides a small, reusable `clues` list used by the adventure game.
Each entry is a one-sentence hint about a past event and begins with "There is a...".
"""
clues = [
	"There is a smudge of dried ink on the underside of the table.",
	"There is a faint scorch on the carpet as if something hot had been placed there.",
	"There is a single muddy footprint pressed into the rug's fringe.",
	"There is a scrap of paper folded three times and tucked into the baseboard.",
	"There is a whisper of perfume that doesn't match any occupant's clothing.",
	"There is a hidden latch behind the bookshelf, its edges recently worn.",
	"There is a streak of crimson along the windowsill that has dried a while.",
	"There is a child's toy, intact but abandoned, under the radiator.",
	"There is a calendar with one day circled and the ink smudged by a trembling hand.",
	"There is a loose floorboard with a small hollow stamped into dust beneath it.",
]

sense_exp = [
	"You see torchlight pooling along the flagstones, though no torch burns nearby.",
	"You hear the slow turning of gears somewhere deep in the wall, patient and eternal.",
	"You smell cold iron mixed with old beeswax and something floral that has lingered for years.",
	"You feel the carved stone hum faintly beneath your fingertips, as if remembering a name.",
	"You sense the room holding its breath, a quiet pressure that makes your heartbeat louder.",
	"You see motes of dust dancing in a shaft of moonlight that slices through a narrow slit.",
	"You hear a draped curtain stir though the air is still, like the echo of a passing cloak.",
	"You smell smoke and melted wax threaded through the tapestry's weave.",
	"You feel a chill run along the baseboard as if footsteps passed by moments ago.",
	"You see a shadow pause in the corner, not quite matching the shape of anything known.",
	"You hear a faint, off-key melody humming from behind a sealed door.",
	"You sense something familiar and foreign at once, a memory that belongs to someone else.",
]

# Try importing RandomItemSelector if this module is re-used elsewhere. If the
# import would fail (e.g., during initial module load in the same file), fall
# back to `None` — the class is defined later in this module and will be
# available by the time users import the module normally.
try:
	from adventure.adv_game import RandomItemSelector
except Exception:
	RandomItemSelector = None

import random


class RandomItemSelector:
	"""Select random items without immediate repetition.

	- items: list of available items (kept in insertion order)
	- used_items: list of items that have already been selected

	Methods
	- add_item(item): append a new item to the pool
	- pull_random_item(): return a random unused item, mark it used; when all
	  items have been used, the used list is cleared and selection resumes.
	- reset(): clear the used_items list so all items are available again.
	"""

	def __init__(self, items=None):
		# store a shallow copy so external mutations don't affect internal state
		self.items = list(items) if items else []
		self.used_items = []

	def add_item(self, item):
		"""Add a new item to the selection pool.

		The item will be available immediately for selection unless it's already
		present in the pool. Duplicates are allowed to support weighted selection.
		"""
		self.items.append(item)

	def pull_random_item(self):
		"""Return a random item that hasn't been used yet.

		If all items have been used, reset `used_items` to allow reuse.
		If there are no items at all, return None.
		"""
		if not self.items:
			# Nothing to choose from
			self.used_items = []
			return None

		# Build set of available indices for faster checks if lists grow large
		available_indices = [i for i in range(len(self.items)) if i not in
							 {self.items.index(x) for x in self.used_items if x in self.items}]

		# If nothing available, reset used_items and recompute available indices
		if not available_indices:
			self.reset()
			available_indices = list(range(len(self.items)))

		choice_idx = random.choice(available_indices)
		choice = self.items[choice_idx]
		self.used_items.append(choice)
		return choice

	def reset(self):
		"""Make all items available for selection again by clearing used_items."""
		self.used_items.clear()


class SenseClueGenerator:
	"""Singleton generator that combines a clue and a sensory expression.

	Uses two RandomItemSelector instances: one for `clues` and one for `sense_exp`.
	The singleton is stored in the class variable `_instance`.
	"""

	_instance = None

	def __new__(cls):
		if cls._instance is None:
			cls._instance = super().__new__(cls)

			# Ensure we have a selector class available. If the earlier import
			# failed, the local RandomItemSelector defined above will be used.
			selector_cls = RandomItemSelector if RandomItemSelector is not None else RandomItemSelector

			# Initialize selectors using module-level lists
			cls._instance.clue_selector = selector_cls(clues)
			cls._instance.sense_selector = selector_cls(sense_exp)

		return cls._instance

	def get_senseclue(self):
		"""Pull one clue and one sensory sentence and return them combined.

		Example output: "You hear a curtain stir though the air is still. There is a scrap of paper..."
		"""
		clue = self.clue_selector.pull_random_item()
		sense = self.sense_selector.pull_random_item()

		if clue and sense:
			return f"{sense} {clue}"
		return clue or sense or ""



