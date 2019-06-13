# Down with Society

## Background

This is a game made at the first gamejam held by the mk game devs meetup group. It was the brain child of 3 people on a saturday morning for the theme "Knocking Down" and the gamejam was completed in 34 hours. Unfortunately the availability of one team member was lower than they'd hoped and so we decided to make some improvements after the gamejam to make up for this lost time.

On day 1 we started with a blank py file. All of the code for the game can be considered to have been written from scratch with some borrowings involved to create the sound engine.

## How to play



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