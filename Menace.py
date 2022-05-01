import random as rand
import json
from collections import Counter

class GameBoard:
    def __init__(self):                          
        self.GameBoard=[' ',' ',' ',' ',' ',' ',' ',' ',' ']

    #display the game board
    def __str__(self):                   
        return("\n 0 || 1 || 2 \t %s || %s || %s \n 3 || 4 || 5\t %s || %s || %s \n 6 || 7 || 8\t %s || %s || %s " % (self.GameBoard[0], self.GameBoard[1], self.GameBoard[2], self.GameBoard[3], self.GameBoard[4], self.GameBoard[5], self.GameBoard[6], self.GameBoard[7], self.GameBoard[8]))

    #check for the move is valid or not
    def is_valid_move(self,playerMove):              
        try:                           
            playerMove=int(playerMove)
        except ValueError:
            return False

    #check if the position given by player is empty
        if 0<=playerMove<=8 and self.GameBoard[playerMove]==" ":       
            return True
        return False

    def get_win_condition(self):                         
        return ((self.GameBoard[0] != ' ' and            
                 ((self.GameBoard[0] == self.GameBoard[1] == self.GameBoard[2]) or
                  (self.GameBoard[0] == self.GameBoard[3] == self.GameBoard[6]) or
                  (self.GameBoard[0] == self.GameBoard[4] == self.GameBoard[8])))
                or (self.GameBoard[4] != ' ' and
                    ((self.GameBoard[1] == self.GameBoard[4] == self.GameBoard[7]) or
                    (self.GameBoard[3] == self.GameBoard[4] == self.GameBoard[5]) or
                    (self.GameBoard[2] == self.GameBoard[4] == self.GameBoard[6])))
                or (self.GameBoard[8] != ' ' and
                    ((self.GameBoard[2] == self.GameBoard[5] == self.GameBoard[8]) or
                    (self.GameBoard[6] == self.GameBoard[7] == self.GameBoard[8]))))    

    #check if it is a draw or not
    def draw_condition(self):                             
        return all((x!=" " for x in self.GameBoard))


    # place move on the board
    def play_move(self,pos, marker):        
        self.GameBoard[pos]=marker

    #append all the played pos in the board
    def append_move(self):                          
        return ''.join(self.GameBoard)

    
class Menace:
    def __init__(self):
        #storing states during the game
        self.match_boxes = {}      
        #number of loses, draws and wins of menace
        self.num_lose=0
        self.num_draw=0
        self.num_win=0
    
    #init list of moves played by menace
    def start_game(self):
        self.played_moves=[]

    #get all possible moves for menace

    def get_possible_moves(self, GameBoard):       
        #get the current state
        GameBoard=GameBoard.append_move()      

        if GameBoard not in self.match_boxes:
            #new beads denotes the possible positions to play
            newBeads=[pos for pos,mark in enumerate(GameBoard) if mark==" "] 
            self.match_boxes[GameBoard]=newBeads * ((len(newBeads)+2)//2)

        beads=self.match_boxes[GameBoard]

        if len(beads):
            bead=rand.choice(beads)
            self.played_moves.append((GameBoard,bead))      
        else:
            bead=-1
        return bead

    def if_win(self):
        for (GameBoard,bead) in self.played_moves:
            self.match_boxes[GameBoard].extend([bead,bead,bead])
        self.num_win+=1

    def if_draw(self):
        for (GameBoard,bead) in self.played_moves:
            self.match_boxes[GameBoard].append(bead)
        self.num_draw+=1
    
    def if_lose(self):
        for (GameBoard,bead) in self.played_moves:
            matchbox=self.match_boxes[GameBoard]
            del matchbox[matchbox.index(bead)]
        self.num_lose+=1
        
    #count the number of stored states
    def length(self):
        return (len(self.match_boxes))

    
class Player:
    def __init__(self):
        pass

    def start_game(self):
        print("Get Set Ready!")

    #take the playerMove from user
    def get_possible_moves(self, GameBoard):
        while True:
            playerMove=input("make playerMove ")
            if GameBoard.is_valid_move(playerMove):
                break
            print("not a valid playerMove")
            
        return int(playerMove)

    #to print the results of the games
    def if_win(self):
        print("Player Won")
        
    def if_draw(self):
        print("You and me are equal. Its a draw")
        
    def if_lose(self):
        print("Player Lost the game")
        

#function to play game
def play_game(first, second, silent=False):
    game_board = GameBoard()
    first.start_game()
    second.start_game()

    if not silent:
        print("\nStarting a new game...")
        print(game_board)
    
    while True:
        playerMove=first.get_possible_moves(game_board)
        if playerMove==-1:
            if not silent:
                print("Player Resigned")
            first.if_lose()
            second.if_win()
            break
        
        game_board.play_move(playerMove,'X')

        if not silent:
            print(game_board)
        if game_board.get_win_condition():
            first.if_win()
            second.if_lose()
            break
        if game_board.draw_condition():
            first.if_draw()
            second.if_draw()
            break


        playerMove=second.get_possible_moves(game_board)

        if playerMove==-1:
            if not silent:
                print("Player Resigned")
            second.if_lose()
            first.if_win()
            break
        
        game_board.play_move(playerMove,'O')

        if not silent:
            print(game_board)
        if game_board.get_win_condition():
            second.if_win()
            first.if_lose()
            break


    
if __name__=='__main__':
    menaceFirst=Menace()
    menaceSecond=Menace()
    player=Player()

    print("Input 1 to use trained model otherwise press 0")
    n = int(input())

    #user selected not to use trained model, then train it for 100000 matches
    if n==0:
        for i in range(100000):
            play_game(menaceFirst,menaceSecond,silent=True)
     
        state1 = menaceFirst.length()
        state2 = menaceSecond.length()
        
        if state1>=state2:
            print("Number of states ",state1)
            with open('states.json', 'w') as f:
                json.dump(menaceFirst.match_boxes, f, sort_keys=False, indent=4)

        else:
            print("Number of states ",state2)
            with open('states.json', 'w') as f:
                json.dump(menaceSecond.match_boxes, f, sort_keys=False, indent=4)

        play_game(menaceFirst,player)

    #user selected to use the trained model, so fetch it from the json file
    elif n==1:
        menaceTrained = Menace()
        with open('states.json', 'r') as f:
            menaceTrained.match_boxes = json.load(f)
        print("Number of states ",menaceTrained.length())
        play_game(menaceTrained,player)
