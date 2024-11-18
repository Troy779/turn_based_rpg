# rpg_game.py

import random

class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.max_health = health  # Save max health for leveling up
        self.attack_power = attack_power
        self.level = 1
        self.experience = 0
        self.experience_to_level_up = 20

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def attack(self, other):
        damage = random.randint(0, self.attack_power)
        other.take_damage(damage)
        print(f"{self.name} attacks {other.name} for {damage} damage!")
        print(f"{other.name} has {other.health} health remaining.")

    def gain_experience(self, amount):
        self.experience += amount
        print(f"{self.name} gains {amount} experience!")
        if self.experience >= self.experience_to_level_up:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience -= self.experience_to_level_up
        self.experience_to_level_up += 10  # Increase XP required for next level
        self.max_health += 10
        self.attack_power += 5
        self.health = self.max_health  # Restore health
        print(f"{self.name} leveled up to level {self.level}!")
        print(f"Health increased to {self.max_health} and attack power increased to {self.attack_power}!")

class Player(Character):
    def heal(self):
        heal_amount = random.randint(5, 15)
        self.health += heal_amount
        if self.health > self.max_health:
            self.health = self.max_health
        print(f"{self.name} heals for {heal_amount} health!")
        print(f"{self.name} now has {self.health} health.")

class Monster(Character):
    pass

class Warrior(Player):
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=15)

class Mage(Player):
    def __init__(self, name):
        super().__init__(name, health=80, attack_power=25)

class Archer(Player):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=20)

def game_loop():
    print("Welcome to the RPG Game!")

    player_name = input("Enter your character's name: ")
    print("Choose your class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Archer")
    class_choice = input("Enter the number of your class choice: ")

    if class_choice == '1':
        player = Warrior(player_name)
    elif class_choice == '2':
        player = Mage(player_name)
    elif class_choice == '3':
        player = Archer(player_name)
    else:
        print("Invalid choice! Defaulting to Warrior.")
        player = Warrior(player_name)

    monster = Monster("Fierce Goblin", 100, 15)

    while player.is_alive() and monster.is_alive():
        print("\nYour turn:")
        action = input("Choose an action: (1) Attack, (2) Heal: ")

        if action == '1':
            player.attack(monster)
        elif action == '2':
            player.heal()
        else:
            print("Invalid action. Please choose 1 or 2.")
            continue

        if monster.is_alive():
            monster.attack(player)
        else:
            print(f"You have defeated the {monster.name}!")
            player.gain_experience(15)  # Gain XP for defeating the monster
            monster = Monster("Fierce Goblin", 100, 15)  # Respawn monster

        if not player.is_alive():
            print("You have been defeated. Game Over!")

if __name__ == "__main__":
    game_loop()
