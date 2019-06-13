# Down with Society

## Background

This is a game made at the first gamejam held by the mk game devs meetup group. It was the brain child of 3 people on a saturday morning for the theme "Knocking Down" and the gamejam was completed in 34 hours. Unfortunately the availability of one team member was lower than they'd hoped and so we decided to make some improvements after the gamejam to make up for this lost time.

On day 1 we started with a blank py file. All of the code for the game can be considered to have been written from scratch with some borrowings involved to create the sound engine.

## How to play

ESC will exit the game after the splash screen.

Socialist player controls:

Arrow keys to move and right ctrl is the action button.

Capitalist player controls:

WASD to move and left ctrl is the action button.

-------

The winner of the game is the player to fill their score bar first (socialist's is red on the left, capitalists is blue on the right). Fill your score bar by completing constructions for your team (parks for socialists, factories for capitalists).

Each player has an energy bar. When the energy bar is green, you have enough energy to complete an action. A player's target cell is highlighted in red for socialists and blue for capitalists.

Using the action button while you have a blank cell selected will begin a construction for your team on that cell. (Construction progress bar is shown in green)

Using the action button while you have an enemy's construction selected will begin reversing the progress of the construction. (Construction progress bar will turn red).

Using the action button on one of your own constructions whose progress is reversing will return the construction to a normal progressing state.

All actions use the same amount of energy.

The socialist cyclist moves slower than the capitalist driver but their buildings are constructed faster and the socialist is able to cycle through their own parks. The capitalists buildings are constructed slower but they gain score for running over the cyclist.

## Get the game

The easiest way to play this game is by downloading the windows build from the itch io platform.

https://superdan.itch.io/down-with-society

For other platforms you will have to clone the source and install the python requirements from the requirements file. On linux and probably macs:

1. Clone this repository.

2. Cd to the directory that you'd like to contain your virtual python environment.

3. Create virtual env (you may need to install virtual env too):

```
virtualenv downwithsociety -p python3
```

4. Enter virtualenv:

```
source downwithsociety/bin/activate
```

5. Install prerequisites (requirements.txt is in this repo):

```
pip install -r requirements.txt
```

6. Cd to cloned repo and run check file from within your virtualenv. eg.

```
(gamejam-test) danny@danny-Mint-19:~/Documents/repos/others/gamejam-test$ python main.py
```

## Building

We've found this project builds easily for windows and linux using cx_freeze. A sample setup.py file is included in this repository but may need to be edited for your particular setup.