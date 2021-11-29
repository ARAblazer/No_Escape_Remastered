# No Escape Remastered


## What is this?
My very first python project was a simple text-based adventure game I called No Escape. You can find it on my GitHub 
as TRPG_1 (Text Role PLaying Game 1). Despite this, it's not much of an RPG. It is a very simple, rather difficult game
with a lot of poorly written code. This project at first was merely a back-end revamp. I wanted to clean up the code and
make it a little more readable and object-oriented. That done, however, it felt a little featureless for a "remaster" 
as I called it. So, I started by adding some fancy borders around the interface and little by little, things grew out 
of hand. Now there is a map, **color**, and various little changes to the original. It's still not perfect, and,
honesty, not even very good. But it's mine. Cliché as it sounds, it's a part of me.

TL;DR: A remake of my first ever project with a lot more features and (hopefully) better game design.

## How to play
### Requirements
- macOS (only supported platform so far _sorry!_)
- Python 3.10 or later

### Getting started
Unfortunately, because of the use of the curses module (if you don't know what that means, don't worry), the code for
this game has to be run directly from the command line. But don't let that intimidate you if you haven't done this
before. On Mac (I don't believe this will work properly on Windows in its current form), download the .zip file for the
project. Unzip it somewhere you can find it easily like the Desktop or Downloads folder, then context click the folder. 
On the menu that pops up, click **New Terminal at Folder**. Then type or copy/paste the following into the terminal
window that pops up:

```
python3 source/main.py
```

Make sure your terminal window is pretty large when you run it. Depending on how your terminal is configured, the font
size of the game could be different. For me 116x32 works the best, but that could change for different systems and
configurations. If you have trouble seeing some of the colors or if the map looks weird, try messing around with your
terminal preferences by hitting **⌘+comma**.

### Playing the Game
The game is a command-based interface. Basically, you type what you want to do, and your character does it. The valid
commands are as follows:

- **go/move [direction]**
  - This is how you move around the map. You can type the cardinal direction names (north, south, east, or west) or
  just the first letter. EX: 'go north' and 'move n' do the same thing 
- **get/take [item]**
  - Simple enough, this allows you to pick up items you see. These items will be clearly displayed. EX: 'take key'
- **use [item]** 
  - This command can only be used for some items. You'll discover them along the way. If you get stuck, try using your 
  - stuff. EX: 'use hammer'
- **help** 
  - displays this list in-game
  
You can quit at any time by hitting **ctrl+c**, but remember, there's no saving, so be prepared to start over.

### Objective
Despite the game's name, your objective is to, in fact, escape. There are three levels. In each one, you will find an
item denoted by its purple color and Capitalized Name. This item will allow you to move on to the next level. It's
pretty simple, but don't be fooled, the pathing is very precise. One mistake could lead to certain death. 

Side note: if
you get sent back to Level One from the second level, don't worry! It isn't a bug. This is to prevent you from 
soft-locking yourself since the second level require you to beat the first level a specific way. Sorry, that's how it
was in the original, and I'm nothing if not faithful.

## Story
Coming Soon...