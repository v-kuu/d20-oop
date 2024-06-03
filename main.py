import random
import sys
import csv
import curses
import time
from curses.textpad import rectangle

def main(stdscr):
    height, width = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    redNwhite = curses.color_pair(1)
    stdscr.box()
    stdscr.addstr(0, 2, '----D20----', curses.A_STANDOUT)
    stdscr.attron(redNwhite)
    rectangle(stdscr, 1, 1, 12, width - 3)
    rectangle(stdscr, 13, 1, height - 2, width -3)
    stdscr.attroff(redNwhite)
    stdscr.noutrefresh()
    graphicWin = curses.newwin(10, width - 5, 2, 2)
    graphicWin.noutrefresh()
    consoleWin = curses.newwin(height - 16, width - 5, 14, 2)
    consoleWin.noutrefresh()
    curses.doupdate()

    playerStats = statAssign('playerClasses.csv', consoleWin)
    consoleWin.clear()
    consoleWin.noutrefresh()
    curses.doupdate()
    while True:
        graphicWin.clear()
        graphicWin.addstr(1, 2, f"{playerStats['name']}".upper(), curses.A_REVERSE)
        graphicWin.addstr(3, 2, f"Hit points: {playerStats['hp']}")
        graphicWin.addstr(5, 2, f"Attack bonus: +{playerStats['ab']}")
        graphicWin.addstr(7, 2, f"Armor class: {playerStats['ac']}")
        graphicWin.noutrefresh()
        curses.doupdate()
        enemyStats = statAssign('enemyList.csv', consoleWin)
        results = combat(playerStats, enemyStats, graphicWin, consoleWin)
        graphicWin.addstr(3, 20, 'You rest for a while and heal.')
        playerStats['hp'] = results + 1
        graphicWin.addstr(5, 20, f"You now have {playerStats['hp']}HP.")
        graphicWin.noutrefresh()
        curses.doupdate()
        time.sleep(2)

class Combatant:
    def __init__(self, name, hp, ab, ac):
        self.name = name
        self.hp = hp
        self.ab = ab
        self.ac = ac


def statAssign(file, window):
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
        fields = "//".join(fieldNames)
        window.addstr(0, 1, fields.upper())
        line = 1
        for i, row in enumerate(dataBase):
            window.addstr(line, 1, f"{i+1}. {row['name']}, {row['hp']}, {row['ab']}, {row['ac']}")
            line += 1
        window.addstr(line + 1, 1, 'Pick a class (n):')
        window.noutrefresh()
        curses.doupdate()
        while True:
            key = window.getkey()
            try:
                if 1 <= int(key) <= len(nameList):
                    choice = nameList[int(key) - 1]
                    break
            except ValueError:
                continue

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


def combat(yourStats, theirStats, graphicWindow, textWindow):
    player = Combatant(**yourStats)
    enemy = Combatant(**theirStats)
    graphicWindow.addstr(3, 20, f'{player.name} encounters {enemy.name}!')
    graphicWindow.noutrefresh()
    while enemy.hp > 0 and player.hp > 0:
        textWindow.addstr(1, 1, 'Do you wish to (a)ttack or (r)un? (Run exits the game.)')
        textWindow.noutrefresh()
        curses.doupdate()
        choice = textWindow.getkey()
        textWindow.clear()
        if choice.lower() == 'a':
            if attack(enemy.ac, player.ab) == True:
                enemy.hp = enemy.hp - 1
                textWindow.addstr(3, 1, f"You attack and hit! Enemy has {enemy.hp}hp left.")
                textWindow.noutrefresh()
            else:
                textWindow.addstr(3, 1, 'You attack and miss!')
                textWindow.noutrefresh()
            if enemy.hp > 0:
                if attack(player.ac, enemy.ab) == True:
                    player.hp = player.hp - 1
                    textWindow.addstr(5, 1, f"The enemy counterattacks. You're hit! You have {player.hp}hp left.")
                    textWindow.noutrefresh()
                else:
                    textWindow.addstr(5, 1, 'The enemy strikes you. You dodge!')
                    textWindow.noutrefresh()
            curses.doupdate()
        elif choice.lower() == 'r':
            sys.exit()
        else:
            textWindow.clear()
            textWindow.addstr(1, 1, 'Invalid input')
            textWindow.noutrefresh()
            time.sleep(1)
    if enemy.hp == 0:
        textWindow.clear()
        textWindow.addstr(1, 1, 'Victory!', curses.A_STANDOUT)
        textWindow.noutrefresh()
        curses.doupdate()
        time.sleep(2)
        return player.hp
    else:
        textWindow.clear()
        textWindow.addstr(1, 1, 'Defeat!', curses.A_STANDOUT)
        textWindow.noutrefresh()
        curses.doupdate()
        time.sleep(2)
        sys.exit()


if __name__ == '__main__':
    main()
