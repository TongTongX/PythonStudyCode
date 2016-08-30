Project Title: Gomoku game

Team Members:	Alan (Xutong) Zhao
				Yue Ma

Code running instruction:
	- Locates the correct directory.
	  Type python main.py on terminal window (note: don't try to run it using python3 since Tkinter is for python2)
	- Note: The game is played on a Tkinter window. However, there is some quite useful information 
			printed onto the terminal such as the simple visualizaiton of the board after each turn,
			messages indicating which step the user reaches at, and the game over message. The user
			does not need to look at what shows up on the terminal.

Acknowledgement:
	- I refered to effbot.org/tkinterbook, as well as some other resources online like stackoverflow, to learn how 
		to build a GUI.
	- I read and used the idea of Alpha-Beta Pruning pseudo code on Wikipedia.
	- I tested my program with Yiding Fan without sharing our code.

Description: 
We developed the abstract strategy board game Gomoku (also called Gobang, Five in a Row, etc) using python, 
with the interface displayed on the computer screen. On a Go board with 15*15 intersections, two 
users (one has black stones and the other has white stones) alternate in placing one single stone 
of their color on an empty intersection. Once placed, stones are not moved or removed from the board. 
The winner is the first player to get an unbroken row of five stones of the one�s color horizontally, 
vertically, or diagonally. Note that it is not required to have a row of exactly five stones for a win;
a row of more than five stones also qualifies.

This project is comprised of 4 major components stated below:

1. Game board object
	- Create a 15*15 nested list self.__board as the board to store values at each intersection on the game board.
		0 - empty intersection, 1 - black stone placed, 2 - white stone placed.
		Each posision is initially set to be 0.

	- Create a set self.won = {} to store positions of 5 stones in a line.
	
	- Define a few functions to do the following in this object:
		reset (self)			clear the board (set all position to 0)
		get (self, row, col)	get the value at a coord
		check (self)			check if there is a winner
		board (self)			return the board array
		show (self)				output on terminal


2. Evaluation object
	Assign a score to each intersection on the board based on the rules of the game. A portion of code of 
	this part is quite ugly since I used more than 100 lines if-elif-else statements to discuss every single
	possible scenarios that could occur.
	
	- Create a list self.POS for adding weight to each intersetion. Add weight of 7 to the center, 6 to 
		the outer square, then 5, 4, 3, 2, 1, at last 0 to the outermost square.
	
	- Consider different situations listed below:
		self.cTwo		# chong'er	2 stones in a row, 1 move to make a chongsan
		self.cThree		# chongsan	3 stones in a row, 1 move to make a chongsi
		self.cFour		# chongsi	4 stones in a row, 1 move(1 possible position) to make a 5
		self.two		# huo'er	2 stones in a row, 1 move to make a huosan
		self.three		# huosan	3 stones in a row, 1 move to make a huosi
		self.four		# huosi		4 stones in a row, 1 move(2 possible positions) to make a 5
		self.five		# huowu		5 stones in a row
		self.analyzed		# has benn analyzed
		self.unanalyzed		# has not been analyzed

	- Define a list self.result to save current reslut of analyzation in a line.
		
	- Define a list self.line to store current data in a line.
		
	- Define a list self.record to save result of analysis of whole board.
		Result is in the format of each item in list is record[row][col][dir].

	- Define a lsit self.count to store the count of each situation: count[black/white][situation]

	- Define a few functions to do the following in this object:
		reset (self)								reset data
		
		evaluate (self, board, turn)				analyze & evaluate board 
													return score based on analysis result
		
		__evaluate (self, board, turn)				analyze & evaluate board in 4 directinos: horizontal, 
														vertical, diagonal(left-hand or right-hand)
													return score difference between players based on analysis result
		
		__analysis_horizon (self, board, i, j)			anaylze horizontally
		__analysis_vertical (self, board, i, j)			analyze vertically
		__analysis_left (self, board, i, j)				analyze left-hand diagonally
		__analysis_right (self, board, i, j)			analyzed right-hand diagonally
		
		analysis_line (self, line, record, num, pos)	analyze a line, find out different situations
														(i.e., five, four, three, etc)


3. Searcher object

	- Set the self.maxdepth to 3 so that the running time for each move is not too long
		(runn time for different depth: 1 - <1 sec, 2 - a few sec, 3 - up to 4 min).

	- Define a few functions to do the following in this object:
		genMoves (self, turn)
											generate all possible moves for the current board and store the 
											score and position of each move in a list in format of (score, i, j).
		
		__search (self, turn, depth, alpha = -0x7fffffff, beta = 0x7fffffff)
											recursive search, returns the best score
											minimax algorithm with alpha-beta pruning
											0x7fffffff == (2^31)-1, indicating a large value

		search (self, turn, depth = 3)				# specific search
	
	- Note: alpha beta pruning: removes nodes that are evaluated by the minimax algorithm
			in the search tree, eliminates branches that cannot posibbly influence the final decision.
	

4. GUI
	
	I used Tkinter to implememted a bery basic GUI. The Tkinter Canvas Widget is to plot the 
	game board and stones. Since the baord is actually quite simple, to draw it is just applying 
	create_line and create_oval methods, which are pre-defined in Tkinter. 
	Note: Tkinter is for python 2, while tkinter is for python 3. 
