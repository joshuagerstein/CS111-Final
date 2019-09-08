A description of your program and its features:

This program creates and runs the game Mastermind. It has options for the user to play
the game guessing a code the computer randomly generated or for the user to select a code 
and watch the computer solve it. There are also options for how many turns the guesser in 
the game will have-- 8, 10, or 12. These options are chosen at the beginning of the game. 
When the "set code" option is chosen by the user, the computer will guess the code using 
the 5 guess algorithm created by Donald Knuth. When the game ends, a message is displayed
with either a win or lose statement. Then, a new game button is drawn giving the user the 
option to start a new game.




A brief description/justification of how it is constructed (class organization, how data
 are stored, etc.):

The game is organized into 4 classes. Several classes construct instances of common 
elements of the game. The class ColorOptions box creates the box of colors for the user to
choose from which allows the user to set code for the computer or make a guess. The class 
TextButton creates an instance of a rectangle with text and has a contains method. The 
class Row creates a row of pegs, the colors of which can be manipulated as the game is 
played. 
The other class has a wider scope and runs the main functions of the game. The 
class Mastermind creates the window for the game, runs the game and includes functions 
that analyze input from the window and run the game accordingly. This class also generates 
feedback and runs the algorithm the computer uses to guess the code. The Mastermind class 
creates instances of the other classes as needed to play the game. There is also a main function, which creates an instance of the class mastermind and calls its play method.



A discussion of the current status of your program - what works and what doesn't, etc.:
Currently everything in our Mastermind program works. The AI does take a lot of time 
when making its guesses, though the time decreases with each guess after the first guess, 
but we believe that is just in the nature of the algorithm. As far as it has been tested,
 the algorithm works, solving the code in 5 turns. The option for the human player (guess 
code) also functions correctly in all tests.

Instructions for running your program.:
To run FinalProject.py you need graphics.py, mastermind.gif, and FinalProject.py. 
The program runs from the command line by typing in python3 FinalProject.py