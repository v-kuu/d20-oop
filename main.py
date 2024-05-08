import random
import sys
import csv


def main():
    playerStats = statAssign('player')
    enemyStats = statAssign('enemy')
    combat(playerStats, enemyStats)


class Combatant:
    def __init__(self, name, hp, ab, ac):
        self.name = name
        self.hp = int(hp)
        self.ab = int(ab)
        self.ac = int(ac)


def statAssign(type):
    nameList = []
    database = []
    if type == 'player':
        with open('playerClasses.csv', mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            print(*reader.fieldnames)
            for row in reader:
                print(row['name'], row['hp'], row['ab'], row['ac'])
                nameList.append(row['name'])
                database.append(row)
        while True:
            playerClass = input('Pick a class: ')
            if playerClass in nameList:
                print(f'You have chosen {playerClass}')
                break
            else:
                print('Class not found.')
        return next(filter(lambda name: name['name'] == playerClass, database))
    elif type == 'enemy':
        with open('enemyList.csv', mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                nameList.append(row['name'])
                database.append(row)
        choice = random.choice(nameList)
        return next(filter(lambda name: name['name'] == choice, database))
    else:
        print('Error: Expected player or enemy.')
def attack(targetAC, currentAB):
    if random.randint(1, 20) + currentAB >= targetAC:
        return True
    else:
        return False


def combat(yourStats, theirStats):
    player = Combatant(**yourStats)
    enemy = Combatant(**theirStats)
    print(f'{player.name} encounters {enemy.name}!')
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


if __name__ == '__main__':
    main()
