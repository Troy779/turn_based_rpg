import random

class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def take_damage(self, damage):
        self.health -= damage
        print(f"{self.name} takes {damage} damage. Remaining health: {self.health}")

    def is_alive(self):
        return self.health > 0


class Player(Character):
    def __init__(self, name, character_class):
        super().__init__(name, health=100, attack_power=10)
        self.character_class = character_class
        self.weapon = self.choose_weapon(character_class)

    @staticmethod
    def choose_weapon(character_class):
        if character_class == "Warrior":
            return Weapon("Iron Sword", 30, "Common")
        elif character_class == "Mage":
            return Weapon("Magic Staff", 20, "Common")
        elif character_class == "Archer":
            return Weapon("Bow", 25, "Common")
        else:
            raise ValueError("Invalid character class")

    def attack(self, enemy):
        damage = self.weapon.attack_power
        enemy.take_damage(damage)
        print(f"{self.name} attacks {enemy.name} with {self.weapon.name} for {damage} damage!")

    def heal(self):
        self.health += 20
        print(f"{self.name} heals for 20 health. Total health: {self.health}")


class Monster(Character):
    def __init__(self, name, health, drop_items):
        super().__init__(name, health, attack_power=0)  # Attack power is defined but not used
        self.drop_items = drop_items  # List of possible items to drop

    def drop(self):
        drop_chance = random.randint(1, 100)
        
        # 1% chance for a legendary item
        if drop_chance == 1:  # Exactly 1% chance
            return Weapon("Legendary Artifact", 100, "Legendary")

        for item in self.drop_items:
            # Destructure the item tuple properly
            item_name, threshold, attack_power, rarity = item
            if drop_chance <= threshold:  # Check if drop chance is within rarity
                return Weapon(item_name, attack_power, rarity)  # Return dropped weapon
        return None  # No item dropped


class Weapon:
    def __init__(self, name, attack_power, rarity):
        self.name = name
        self.attack_power = attack_power
        self.rarity = rarity


def main():
    print("Welcome to the RPG Game!")
    
    player_name = input("Enter your character's name: ")
    player_class = input("Choose your class (Warrior, Mage, Archer): ")
    player = Player(player_name, player_class)

    enemies = [
        Monster("Fierce Goblin", 100,
                [("Goblin Dagger", 40, 25, "Common"),
                 ("Goblin's Club", 20, 15, "Uncommon")]),
        Monster("Fire Dragon", 150,
                [("Dragon Scale", 50, 35, "Rare"),
                 ("Fire Gem", 10, 0, "Epic"),
                 ("Dragon Sword", 5, 40, "Epic")])
    ]

    for enemy in enemies:
        print(f"\nA wild {enemy.name} appears!")
        
        while player.is_alive() and enemy.is_alive():
            action = input("Choose an action: (1) Attack (2) Heal: ")
            if action == '1':
                player.attack(enemy)
                if enemy.is_alive():
                    # Monster attacks back
                    monster_damage = random.randint(5, 15)  # Example fixed damage for the monster
                    enemy.take_damage(monster_damage)
            elif action == '2':
                player.heal()
            else:
                print("Invalid action.")

        if enemy.is_alive():
            print(f"{enemy.name} has defeated you!")
            break
        else:
            print(f"You have defeated {enemy.name}!")
            dropped_weapon = enemy.drop()
            if dropped_weapon:
                print(f"You found a {dropped_weapon.name} (Attack: {dropped_weapon.attack_power}, Rarity: {dropped_weapon.rarity})!")


if __name__ == "__main__":
    main()
