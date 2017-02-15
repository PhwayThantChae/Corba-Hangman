#import tkinter as tk   # python3
import Tkinter as tk   # python
from random import randint
from Tkinter import *
import sys
import tkMessageBox
from HangMan_Frame import *

TITLE_FONT = ("Helvetica", 18, "bold")

#Import the CORBA module
from omniORB import CORBA

#Import the stubs for the CosNaming and Program_Hangman modules
import CosNaming, Program_Hangman

#Initialise the ORB
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

#Obtain a reference to the root naming context
obj = orb.resolve_initial_references("NameService")
rootContext = obj._narrow(CosNaming.NamingContext)

if rootContext is None:
    print "Failed to narrow the root naming context"
    sys.exit(1)

#Resolve the name "hangman.my_hangman/ExampleHangman.Object"
name = [CosNaming.NameComponent("hangman","my_hangman"),
        CosNaming.NameComponent("ExampleHangman","Object")]

try:
    obj = rootContext.resolve(name)

except CosNaming.NamingContext.NotFound, ex:
    print "Name not found"
    sys.exit(1)

# Narrow the object to an Program_Hangman:Hangman
hangmano = obj._narrow(Program_Hangman.HangMan)

if hangmano is None:
    print "Object reference is not an Program_Hangman:HangMan"
    sys.exit(1)
###############################################################################

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = tk.Frame(self,bg="#ff5a5a")
        self.container.pack(side="top", fill="both", expand=True)
        #container.pack()
        #container.grid_rowconfigure(0, weight=1)
        #container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.score = 0

        
        self.class_construction()

        self.show_frame("StartPage")

    def class_construction(self):
        
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self) #Start_Page= Start_Page(parent = container, controller = self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        if(page_name=="StartPage"):
            frame.tkraise()
        if(page_name=="PageOne"):
            frame.tkraise()
            self.menubar=Menu(self)  #menubar
            self.fileMenu=Menu(self.menubar,tearoff=0,bg="black",activebackground="skyblue",fg="white",font=("Impact",12))
            self.fileMenu.add_command(label="Main Menu",command=self.call_Main)  #command yay
            self.fileMenu.add_command(label="New Game",command=self.call_New)  #command yay
            self.fileMenu.add_separator()
            self.fileMenu.add_command(label="Quit",command=self.system_quit)
            self.menubar.add_cascade(label="Option",menu=self.fileMenu)
            self.config(menu=self.menubar)

    def system_quit(self):
        self.frames["StartPage"].destroy()
        self.frames["PageOne"].destroy()
        self.frames.clear()
        self.destroy()

    def call_Main(self):
        self.frames["StartPage"].destroy()
        self.frames["PageOne"].destroy()

        self.emptyMenu = Menu(self)
        self.config(menu=self.emptyMenu)
        self.frames={}
        self.show_score(self.score)
        
        self.class_construction()
        self.show_score(self.score)
        self.show_frame("StartPage")

    def call_New(self):
        self.frames["StartPage"].destroy()
        self.frames["PageOne"].destroy()
        self.frames={}
        self.class_construction()
        #print "New :" + str(self.score)
        print self.frames
        self.score =  self.get_score()
        self.show_frame("PageOne")
 

    def show_score(self,num):
        
        self.score = num

    def get_score(self):
        return self.score
