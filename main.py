import random
import sys
import csv


def main():
    playerStats = statAssign('playerClasses.csv')
    print(f"You have {playerStats['hp']}HP, {playerStats['ab']}AB and {playerStats['ac']}AC.")
    while True:
        enemyStats = statAssign('enemyList.csv')
        results = combat(playerStats, enemyStats)
        print('You rest for a while and heal.')
        playerStats['hp'] = results + 1
        print(f"You now have {playerStats['hp']}HP.")


class Combatant:
    def __init__(self, name, hp, ab, ac):
        self.name = name
        self.hp = hp
        self.ab = ab
        self.ac = ac


def statAssign(file):
    nameList, dataBase, fieldNames = ([] for i in range(3))
    with open(file, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldNames.extend(reader.fieldnames)
        for row in reader:
            nameList.append(row['name'])
            dataBase.append(row)
    for stats in dataBase:
        for key in stats:
            if stats[key].isnumeric():
                stats[key] = int(stats[key])
    if file == 'playerClasses.csv':
        print(*fieldNames)
        for row in dataBase:
            print(row['name'], row['hp'], row['ab'], row['ac'])
        while True:
            choice = input('Pick a class: ')
            if choice in nameList:
                print(f'You have chosen {choice}')
                break
            else:
                print('Class not found.')
    elif file == 'enemyList.csv':
        choice = random.choice(nameList)
    else:
        raise FileNotFoundError('Invalid filename.')
    return next(filter(lambda name: name['name'] == choice, dataBase))
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
                print(f"You attack and hit! Enemy has {enemy.hp}hp left.")
            else:
                print('You attack and miss!')
            if enemy.hp > 0:
                if attack(player.ac, enemy.ab) == True:
                    player.hp = player.hp - 1
                    print(f"The enemy counterattacks. You're hit! You have {player.hp}hp left.")
                else:
                    print('The enemy strikes you. You dodge!')
        elif choice == 'r':
            sys.exit()
        else:
            print('Invalid input')
    if enemy.hp == 0:
        print('Victory!')
        return player.hp
    else:
        print('Defeat!')
        sys.exit()


if __name__ == '__main__':
    main()
