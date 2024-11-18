# rpg_game.py

import random

class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power

    def is_alive(self):
        return self.health > 0

    def attack(self, target):
        target.take_damage(self.attack_power)
        print(f"{self.name} attacks {target.name} for {self.attack_power} damage.")

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        print(f"{self.name} takes {damage} damage, {self.health} health left.")

    def heal(self, amount=20):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        print(f"{self.name} heals for {amount}. Health is now {self.health}.")

class Spell:
    def __init__(self, name, damage=0, heal=0, mana_cost=0, rarity="Common"):
        self.name = name
        self.damage = damage
        self.heal = heal
        self.mana_cost = mana_cost
        self.rarity = rarity

    def cast(self, caster, target):
        if self.heal > 0:
            target.health += self.heal
            if target.health > target.max_health:
                target.health = target.max_health
            print(f"{caster.name} casts {self.name} and heals {self.heal} health!")
        elif self.damage > 0:
            target.take_damage(self.damage)
            print(f"{caster.name} casts {self.name} and deals {self.damage} damage to {target.name}!")
        else:
            print("Spell has no effect.")

class Item:
    def __init__(self, name, rarity):
        self.name = name
        self.rarity = rarity

    def __str__(self):
        return f"{self.name} (Rarity: {self.rarity})"

class Weapon(Item):
    def __init__(self, name, attack_power, rarity):
        super().__init__(name, rarity)
        self.attack_power = attack_power

class Monster(Character):
    def __init__(self, name, health, attack_power, drop_items):
        super().__init__(name, health, attack_power)
        self.drop_items = drop_items  # List of possible items to drop

    def drop(self):
        drop_chance = random.randint(1, 100)
        
        # 1% chance for a legendary item
        if drop_chance == 1:  # Exactly 1% chance
            return Weapon("Legendary Artifact", 100, "Legendary")
        
        for item in self.drop_items:
            if drop_chance <= item[1]:  # Check if drop chance is within rarity
                return Weapon(item[0], item[2], item[3])  # Return dropped weapon
        return None  # No item dropped

# Define some example spells
spells = [Spell("Fireball", damage=25, rarity="Rare"), 
          Spell("Heal", heal=20, rarity="Common"),
          Spell("Lightning Bolt", damage=30, rarity="Epic")]

# Define some weapons for different classes
weapons = {
    "Warrior": [
        Weapon("Basic Sword", 10, "Common"),
        Weapon("Great Axe", 20, "Rare"),
        Weapon("Dragon Sword", 35, "Epic"),
    ],
    "Mage": [
        Weapon("Magic Staff", 15, "Common"),
        Weapon("Fire Wand", 25, "Rare"),
        Weapon("Ice Sceptre", 40, "Epic"),
    ],
    "Archer": [
        Weapon("Short Bow", 10, "Common"),
        Weapon("Crossbow", 20, "Rare"),
        Weapon("Longbow", 30, "Epic"),
    ]
}

# Define monsters with their drops including weapons
goblin = Monster("Fierce Goblin", 100, [("Goblin Dagger", 40, 25, "Common"),
                                         ("Goblin's Club", 20, 15, "Uncommon")])

dragon = Monster("Fire Dragon", 150, [("Dragon Scale", 50, 35, "Rare"),
                                       ("Fire Gem", 10, 0, "Epic"),
                                       ("Dragon Sword", 5, 40, "Epic")])

# Class selection for characters
def choose_class():
    print("Choose your class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Archer")
    class_choice = input("Select class (1, 2, or 3): ")
    class_map = {"1": "Warrior", "2": "Mage", "3": "Archer"}
    return class_map.get(class_choice, "Warrior")  # Default to Warrior if invalid

# Main game logic
def game_loop():
    player_class = choose_class()
    player_weapon = random.choice(weapons[player_class])  # Start with a random weapon from class
    player = Character("Hero", 100, player_weapon.attack_power)
    
    print(f"You are a {player_class} with a {player_weapon} as your weapon!")

    monster = goblin  # Change to dragon for a stronger enemy

    while player.is_alive() and monster.is_alive():
        print("\nYour turn:")
        print("1. Attack")
        print("2. Heal")
        print("3. Cast Spell")
        action = input("Choose an action: ")

        if action == '1':
            player.attack(monster)
        elif action == '2':
            player.heal()
        elif action == '3':
            print("Available spells:")
            for idx, spell in enumerate(spells):
                print(f"{idx + 1}. {spell.name} (Rarity: {spell.rarity})")
            spell_choice = int(input("Choose a spell: ")) - 1
            if 0 <= spell_choice < len(spells):
                spells[spell_choice].cast(player, monster)
            else:
                print("Invalid spell choice.")
            continue
        else:
            print("Invalid action. Please choose 1, 2, or 3.")
            continue

        if monster.is_alive():
            monster.attack(player)
        else:
            print(f"You have defeated the {monster.name}!")
            dropped_item = monster.drop()
            if dropped_item:
                print(f"You found a {dropped_item} with {dropped_item.attack_power} attack power!")
            else:
                print("No items dropped.")

        if not player.is_alive():
            print("You have been defeated. Game Over!")

# Start the game
if __name__ == "__main__":
    game_loop()
