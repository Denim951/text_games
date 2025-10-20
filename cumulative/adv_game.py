"""Adventure game clues.

This module provides a small, reusable `clues` list used by the adventure game.
Each entry is a one-sentence hint about a past event and begins with "There is a...".
"""
from enum import Enum
from abc import ABC, abstractmethod


class encounter_outcome(Enum):
	CONTINUE = 1
	END = 2

# Preferred, PEP8-friendly name for use across the codebase.
EncounterOutcome = encounter_outcome


class Encounter(ABC):
	"""Abstract base class for encounters.

	Subclasses must implement `run_encounter` and return an `EncounterOutcome`.
	"""

	@abstractmethod
	def run_encounter(self) -> EncounterOutcome:
		"""Execute the encounter logic and return an EncounterOutcome.

		Implementations should return either `EncounterOutcome.CONTINUE` or
		`EncounterOutcome.END` to indicate how the game should proceed.
		"""
		raise NotImplementedError

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

	def pull_random_item(self):
		"""Compatibility proxy: return the same combined string as `get_senseclue`.

		This method exists so callers that expect a `pull_random_item` method can
		call it directly on the generator instance.
		"""
		return self.get_senseclue()



class DefaultEncounter(Encounter):
	"""Simple default encounter that prints a combined sense+clue and continues."""

	def __init__(self):
		# instantiate the singleton SenseClueGenerator
		self.scg = SenseClueGenerator()

	def run_encounter(self) -> EncounterOutcome:
		# pull a combined sensory+clue string and print it
		out = self.scg.pull_random_item()
		print(out)
		return EncounterOutcome.CONTINUE



class TreasureEncounter(Encounter):
    """An encounter that awards the player the treasure and ends the game."""

    def run_encounter(self) -> EncounterOutcome:
        print("As you enter, a chest gleams in the torchlight — you've found the treasure!")
        print("Congratulations, you have won the game.")
        return EncounterOutcome.END



class RedWizard(Encounter):
	"""A spell battle with the Red Wizard using fantasy-themed spells."""

	game_rules = {
		"Fireball": ["Ice Shard", "Lightning Bolt"],
		"Ice Shard": ["Wind Gust", "Earthquake"],
		"Wind Gust": ["Lightning Bolt", "Fireball"],
		"Lightning Bolt": ["Earthquake", "Ice Shard"],
		"Earthquake": ["Fireball", "Wind Gust"],
	}

	choices = list(game_rules.keys())

	def run_encounter(self) -> EncounterOutcome:
		print("A Red Wizard blocks your path and challenges you to a spell battle!")
		print("Cast the correct spell to vanquish the wizard; if he wins, you are banished from this castle.")

		while True:
			print("\nChoose a spell:")
			for i, c in enumerate(self.choices, 1):
				print(f"  {i}. {c}")
			choice = input("Enter number (1-5): ").strip()
			try:
				idx = int(choice) - 1
				if idx < 0 or idx >= len(self.choices):
					raise ValueError
			except ValueError:
				print("Invalid selection. Try again.")
				continue

			player = self.choices[idx]
			wizard = random.choice(self.choices)
			print(f"You cast {player}. The Red Wizard casts {wizard}.")

			if player == wizard:
				print("The spells clash evenly — the duel continues.")
				continue

			# player wins if wizard choice is in player's beaten list
			if wizard in self.game_rules[player]:
				print("Your spell overwhelms the Red Wizard — he is vanquished from this castle!")
				return EncounterOutcome.CONTINUE
			else:
				print("The Red Wizard's spell overpowers you — you are banished from this castle.")
				return EncounterOutcome.END




class Room:
	"""A room containing a name and an Encounter.

	visit_room() executes the room's encounter and returns its EncounterOutcome.
	"""

	def __init__(self, name: str, encounter: Encounter):
		self.name = name
		self.encounter = encounter

	def visit_room(self) -> EncounterOutcome:
		"""Run the room's encounter and return its result."""
		return self.encounter.run_encounter()


# Prebuilt castle rooms using the DefaultEncounter
castle_rooms = [
	Room("Great Hall", DefaultEncounter()),
	Room("Armory", DefaultEncounter()),
	Room("North Tower", DefaultEncounter()),
	Room("Library", DefaultEncounter()),
	Room("Courtyard", DefaultEncounter()),
	Room("Throne Room", DefaultEncounter()),
]

# add a Treasure Room with a Treasure Encounter to the rooms list
castle_rooms.append(Room("Treasure Room", TreasureEncounter()))

# create a room called “The Red Wizard’s Lair” with the Red Wizard Encounter and add it to the rooms list
castle_rooms.append(Room("The Red Wizard's Lair", RedWizard()))

class Castle:
	"""Manage room selection and navigation for the castle.

	- room_selector: RandomItemSelector initialized with the `castle_rooms` list
	"""

	def __init__(self, rooms=None):
		# default to the prebuilt castle_rooms if none provided
		rooms = rooms if rooms is not None else castle_rooms
		self.room_selector = RandomItemSelector(rooms)

	def select_door(self) -> int:
		"""Randomly determine number of doors (2-4), prompt the user to choose one.

		Returns the door number chosen (1-based).
		"""
		num_doors = random.randint(2, 4)
		print(f"\nYou approach a corridor with {num_doors} closed doors.")
		prompt = f"Select a door (1-{num_doors}): "
		while True:
			choice = input(prompt).strip()
			try:
				val = int(choice)
				if 1 <= val <= num_doors:
					print(f"You open door {val}...\n")
					return val
			except ValueError:
				pass
			print(f"Invalid selection. Enter a number between 1 and {num_doors}.")

	def next_room(self) -> EncounterOutcome:
		"""Select a door, pick a random room, announce it, visit it, and return outcome."""
		self.select_door()
		room = self.room_selector.pull_random_item()
		if room is None:
			print("No rooms available.")
			return EncounterOutcome.END

		print(f"You find yourself in the {room.name}.")
		return room.visit_room()

	def reset(self):
		"""Reset the room selector so all rooms become available again."""
		self.room_selector.reset()
		print("Castle rooms have been reset.")



class Game:
	"""High-level game manager that runs a play loop over a Castle instance."""

	def __init__(self, rooms=None):
		# rooms is expected to be a sequence (list/set) of Room objects
		self.castle = Castle(rooms=rooms)

	def play_game(self):
		"""Main game loop.

		Explains the objective, then repeatedly visits rooms until an END outcome.
		After game over, prompts the user to explore a different castle.
		"""
		print("Welcome to the castle exploration game!")
		print("Objective: Navigate the castle rooms and search for the treasure.\n")

		while True:
			outcome = self.castle.next_room()
			if outcome == EncounterOutcome.END:
				self.castle.reset()
				print("Game Over")
				again = input("Would you like to explore a different castle? (y/n): ").strip().lower()
				if again.startswith("y"):
					print("Starting a new exploration...\n")
					continue
				else:
					print("Thanks for playing!")
					break
			# otherwise continue exploring

# run the game
if __name__ == "__main__":
	game = Game()
	game.play_game()




