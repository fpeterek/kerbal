# Kerbal

A simple game with a simple objective - to succesfully land a rocket.

## Gameplay

The premise of the game is very simple. Land on a platform out in the sea without destroying the rocket. Remember, rockets are
expensive.

A couple precautions are taken to ensure the task isn't as easy as it sounds. 

* Landing in water or plumetting into the platform at excessively high velocity damages the rocket, causing it to explode. 
* Dynamically generated wind can cause the rocket to drift away from its desired path, or even cause it to rotate around it's center of gravity.

### Controls

Use `W`/`A`/`D` to apply engine thrust, but be wary. Applying thrust on the side of the rocket causes the rocket to rotate.

`R` can be used to reset the game, in case you wander off too far with the rocket, your rocket explodes, or you successfully 
manage to land and you want to try again. 

If you believe current wind conditions pose no challenge, you can increase its velocity manually. Use `j` to decrement and `k`
to increment wind's velocity by 1 knot. Changing the wind speed manually disables dynamic changes, until the game is reset 
using the `R` key.

## How to run the game

#### The game is written in Python. Make sure you have Python3.6 or higher installed on your computer.

`sudo apt install python3` (Linux)

`brew install python3` (macOS)

#### Clone the repository

`git clone https://github.com/fpeterek/kerbal.git`

or alternatively, download the entire folder via the web interface.

#### Enter the newly downloaded directory

`cd kerbal/`

#### Create a virtual environment

`virtualenv venv`

#### Enter the virtual environment

`source venv/bin/activate`

#### Install dependencies from the requirements.txt file

`pip3 -r requirements.txt`

On macOS, the `keyboard` dependency can cause pip to install a whole lot of dependencies required to interact with the system
and get input from the keyboard. This doesn't happen on Linux.

#### Run the game

`sudo python3 kerbal/`

Unfortunately, the event based keyboard input from TKinter proved inadequate and I had to use the `keyboard` module.
This module, unfortunately, requires super user permissions, as it needs to interact with the system to find out if a key
is pressed. This means the game has to be run with super user permissions.

## Credits

The explosion sprite sheet was [kindly borrowed from here](https://opengameart.org/content/pixel-explosion-12-frames)

The rocket sprite was made by me and you're free to use it in any way you want, be it commercial or personal use.

## License

All code in this repository is licensed under the MIT license, which means you can use it in any way imaginable, be it 
personal, commercial or educational. Just don't hold me liable when your real life rocket fails to launch and explodes
in your garden.
