from tkinter import *
from tkinter import messagebox
import random

class MinesweeperCell(Label):
    '''represents a minesweeper cell'''

    def __init__(self,master,coord):
        '''MinesweeperCell(master,coord) -> SudokuCell
        creates a new blank MinesweeperCell with (row,column) coord'''
        Label.__init__(self,master,height=1,width=2,text='', bg='white',font=('Arial',20), relief = RAISED, bd = 3)
        
        self.value = 0
        self.flags = 0
        self.cells = {}
        self.width = 0
        self.length = 0
        self.mines = 0
        
        self.coord = coord  # (row,column) coordinate tuple
        self.readOnly = False     # starts as changeable
        self.isMine = False
        # set up listeners
        self.bind('<Button-1>',self.click)
        self.bind('<Button-3>',self.flag)

    def expose(self, coord):
        '''MinesweeperCell.expose(coord)
        exposes the adjacent squares if a
        player clicks on a blank square '''
        for deltaX, deltaY in [(-1,-1),(0,-1),(1,1),(-1,0),(1,0),(-1,1),(0,1),(1,-1)]:
            posX = coord[0] + deltaX
            posY = coord[1] + deltaY
            if (posX < 0) or (posY < 0) or (posX > self.width-1) or (posY > self.length-1):
                continue
            self.cells[(posX,posY)].reveal()
            if self.cells[(posX, posY)].value == 0:
                if self.readOnly == False:
                    self.expose((posX, posY))
        
    def flag(self, event):
        '''MinesweeperCell.flag(event)
        adds a flag on right click event'''
        if (self['text'] == '') and self.readOnly == False:
            self['text'] = '*'
            self.readOnly = True
            self.flags.flags -= 1
            Label(text = self.flags.flags, height = 1, width = 2,font = ('Arial', 28), bg = 'white').grid(row=1,column=0)
        elif (self['text'] == '*') and self.flags.lose == False:
            self['text'] = ''
            self.readOnly = False
            self.flags.flags += 1
            Label(text = self.flags.flags, font = ('Arial', 28), bg = 'white').grid(row=1,column=0)
        else:
            pass

    def click(self, event):
        '''MinesweeperCell.click(event)
        event handler for left clicks'''
        self.reveal()
        
    def reveal(self):
        '''MinesweeperCell.reveal()
        reveals the value of the cell'''
        
        colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
        
        if self.readOnly == False:  # only act on non-read-only cells
            self.flags.tiles_revealed += 1
            self.readOnly = True
            if self.isMine == True:
                self['bg'] = 'red'
                self['relief'] = SUNKEN
                self['text'] = '*'
                messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self)
                self.reveal_mines()
                self.flags.lost()
                self.flags.lose = True
            elif self.value == 0:
                self['bg'] = 'gray'
                self.expose(self.coord)
            else:
                self['bg'] = 'gray'
                self['fg'] = colormap[self.value]
                self['text'] = self.value
            if self.flags.tiles_revealed >= (self.length*self.width)-self.mines:
                messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self)
                self.flags.lost()

    def reveal_mines(self):
        '''MinesweeperCell.reveal_mines()
        reveals all the mines on the map'''
        for x in range(self.width):
            for y in range(self.length):
                if self.cells[(x,y)].isMine == True:
                    self.cells[(x,y)]['bg'] = 'red'
                    self.cells[(x,y)]['relief'] = SUNKEN
                    self.cells[(x,y)]['text'] = '*'

class MinesweeperGrid(Frame):
    '''object for a Minesweeper grid'''

    def __init__(self,master, length, width, mines):
        '''MinesweeperGrid(master)
        creates a new blank Minesweeper grid'''
        # initialize a new Frame
        Frame.__init__(self,master,bg='grey')
        self.grid()

        self.length = length
        self.width = width
        self.mines = mines
        self.minePos = []
        
        self.lose = False
        self.tiles_revealed = 0

        self.flags = mines
        

        # create the cells
        self.values = {}
        self.cells = {} # set up dictionary for cells
        for row in range(width):
            for column in range(length):
                coord = (row,column)
                self.cells[coord] = MinesweeperCell(self,coord)
                self.values[coord] = 0
                # cells go in even-numbered rows/columns of the grid
                self.cells[coord].grid(row=2*row,column=2*column)
                self.cells[coord].length = self.length
                self.cells[coord].width = self.width
                self.cells[coord].cells = self.cells
                self.cells[coord].mines = self.mines
                self.cells[coord].flags = self
        
        Label(text = self.flags, height = 1, width = 2, font = ('Arial', 28), bg = 'white').grid(row=1,column=0)
        
        self.place_mines()
        self.place_nums()

    def place_mines(self):
        '''MinesweeperGrid.place_mines()
        places all the mines on the board'''
        if self.mines == 0:
            return
        x = random.randint(0,self.width-1)
        y = random.randint(0,self.length-1)
        self.cells[(x,y)].isMine = True
        self.mines -= 1
        # replaces a mine if it there is already one in the same position
        if (x,y) in self.minePos:
            self.mines += 1
        self.minePos.append((x,y))
        self.place_mines()
            
    def place_nums(self):
        '''MinesweeperGrid.place_nums()
        places all the mines on a grid'''
        for x in range(self.width):
            for y in range(self.length):
                # Checks all the cells around the main cell for mines
                for deltaX, deltaY in [(-1,-1),(0,-1),(1,1),(-1,0),(1,0),(-1,1),(0,1),(1,-1)]:
                    if self.values[(x,y)] == 'mine':
                        break
                    posX = x + deltaX
                    posY = y + deltaY
                    if (posX < 0) or (posY < 0) or (posX > self.width-1) or (posY > self.length-1):
                        continue
                    if self.cells[(posX, posY)].isMine == True:
                        self.cells[(x,y)].value += 1
                        
    def lost(self):
        '''MinesweeperGrid.lost()
        prevents player from acting with
        the board after a loss or win'''
        for cell in self.cells:
            self.cells[(cell)].readOnly = True
                    
    
def play_minesweeper(length, width, mines):
    '''play_minesweeper()
    plays minesweeper'''
    root = Tk()
    root.title('Minesweeper')
    sg = MinesweeperGrid(root, length, width, mines)
    root.mainloop()

play_minesweeper(20,16,40)




