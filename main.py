import random
import sys

playerStats = {'hp': 0, 'ab': 0, 'ac': 0}
enemyStats = {'hp': 3, 'ab': 1, 'ac': 12}


def main():
    classSelector()
    combat(playerStats, enemyStats)


class Combatant:
    def __init__(self, hp, ab, ac):
        self.hp = hp
        self.ab = ab
        self.ac = ac


def classSelector():
    global playerStats
    while True:
        playerClass = input('Pick either Fighter or Barbarian: ')
        playerClass = playerClass.lower()
        if playerClass == 'fighter' or playerClass == 'barbarian':
            break

    print(f'You have chosen {playerClass}.')
    if playerClass == 'fighter':
        playerStats['hp'], playerStats['ab'], playerStats['ac'] = 3, 1, 15
    elif playerClass == 'barbarian':
        playerStats['hp'], playerStats['ab'], playerStats['ac'] = 4, 3, 10
    else:
        print('Error: Invalid class.')
    print(f"You have {playerStats['hp']} HP, {playerStats['ab']} AB and {playerStats['ac']} AC.")


def attack(targetAC, currentAB):
    if random.randint(1, 20) + currentAB >= targetAC:
        return True
    else:
        return False


def combat(yourStats, theirStats):
    player = Combatant(**yourStats)
    enemy = Combatant(**theirStats)
    print('An enemy of appears!')
    while enemy.hp > 0 and player.hp > 0:
        print('Do you wish to (a)ttack or (r)un?')
        choice = input()
        if choice == 'a':
            if attack(enemy.ac, player.ab) == True:
                enemy.hp = enemy.hp - 1
                print('You attack and hit! Enemy has ' + str(enemy.hp) + 'hp left.')
            else:
                print('You attack and miss!')
            if enemy.hp > 0:
                if attack(player.ac, enemy.ab) == True:
                    player.hp = player.hp - 1
                    print("The enemy counterattacks. You're hit! You have " + str(player.hp) + "hp left.")
                else:
                    print('The enemy strikes you. You dodge!')
        elif choice == 'r':
            sys.exit()
        else:
            print('Invalid input')
    if enemy.hp == 0:
        print('Victory!')
    else:
        print('Defeat!')


main()
