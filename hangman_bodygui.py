from Tkinter import *
from random import randint
import tkMessageBox


import sys

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

#Invoke the get_answer operation

#Get random number for question

random_question = randint(1,hangmano._get_ques_no())
#print str(random_question)

get_question = hangmano.get_question(str(random_question))
get_answer = hangmano.get_answer(str(random_question))







########################################### GUI PART

class bodyGui(object):

    c = 9
    r = 9
    final_answer = ""
    for i in range(len(get_answer)):
        final_answer += str('0')
    final_list = list(final_answer)
    already_guessed = ""
    ############ Match letter with answer #################

    #def gameover(self):
        

    def hangman_image_error(self,num):
        #global hangmanImage
        if( num == 9):
            file_path = "hangman_one.gif"
        elif( num == 8):
            file_path = "hangman_two.gif"
        elif( num == 7):
            file_path = "hangman_three.gif"
        elif( num == 6):
            file_path = "hangman_four.gif"
        elif( num == 5):
            file_path = "hangman_five.gif"
        elif( num == 4):
            file_path = "hangman_six.gif"
        elif( num == 3):
            file_path = "hangman_seven.gif"
        elif( num == 2):
            file_path = "hangman_eight.gif"
        elif( num == 1):
            file_path = "hangman_nine.gif"
        else:
            gameover()

        #self.hangmanImage.config(image="")
        self.hangmanImage.destroy()
        self.image=PhotoImage(file=file_path)   #yay
        self.hangmanImage=Label(self.p2,image=self.image,bd=0)
        self.hangmanImage.grid()
        
    def match_letter_with_answer(self,letter):

        print bodyGui.final_list
        
        bodyGui.already_guessed = bodyGui.already_guessed + letter
        self.guess_letter_text.config(text=bodyGui.already_guessed)
       
        right_flag = 0
        key = 0
        for key,i in enumerate(get_answer):
            if(i == letter):
                if(bodyGui.final_list[key] == '0' or bodyGui.final_list[key] == '_ ' or bodyGui.final_list[key] == '_'):
                    bodyGui.final_list[key] = i
                    right_flag = 1

            else:
                if( bodyGui.final_list[key] == '0' or bodyGui.final_list[key] == '_' or bodyGui.final_list[key] == '_ '):
                    bodyGui.final_list[key] =  '_ '

        print_answer = ''.join(bodyGui.final_list)
        self.question.config(text=print_answer)
        
        if(right_flag == 1):
            bodyGui.r = bodyGui.r-1
        else:
            self.hangman_image_error(bodyGui.c)
            bodyGui.c =bodyGui.c - 1
            self.guess_text.config(text=str(bodyGui.c))        

        
        

    
    def __init__(self,parent):

        
        self.parent=parent
        global root
        
        
        #self.parent.geometry('900x600+275+80')
        #........parent..........................................
        self.container=Frame(root,bg="#ffffff")
        self.container.pack()

        #.......container...........................................


        self.p1=Label(self.container,bg="#ffffff")
        self.p1.pack()
   
        self.label=Label(self.p1, text="Please don't die!",font=("OratorStd",21,"bold"),fg="black",bg="white")
        self.label.grid(row=3,column=1,rowspan=6,columnspan=20,pady=5)
        #.......p1......panel for title............................................

        self.p4=Frame(self.container,bg="#ffffff",pady=10)
        self.p4.pack()
        
        self.q=Label(self.p4,text="Q :",font=("AdobeMyungjoStd-Medium",15,"bold"),bg="#ffffff",fg="#f40505")
        self.q.grid(row=1,column=2)

        
        self.question=Label(self.p4,text=get_question,fg="#f40505",font=("AdobeMyungjoStd-Medium",15,"bold"),bg="#ffffff") #yay
        self.question.grid(row=1,column=3)
     
        self.ans=Label(self.p4,text="A :",fg="#f40505",font=("AdobeMyungjoStd-Medium",15,"bold"),bg="#ffffff")
        self.ans.grid(row=2,column=2)

        #For answer slots to appear randomly with _
        print get_answer
        answer_slot = ""
        #while(i<len(get_answer)+3):
        for i in range(0,len(get_answer)):
            answer_slot = answer_slot+"_ "
       
            
        self.question=Label(self.p4,text=answer_slot,fg="#f40505",font=("AdobeMyungjoStd-Medium",15,"bold"),bg="#ffffff")   #yay
        self.question.grid(row=2,column=3)
            
            
        #........p4.........panel for question and answer.................................................................

        self.pjoin=Frame(self.container,bg="#ffffff")
        self.pjoin.pack()
        #.......pjoin........................................................................
        
        self.p2 = Frame(self.pjoin)
        self.p2.grid(row=8,column=9,pady=0)

        self.image=PhotoImage(file="blank.gif")   #yay
        self.hangmanImage=Label(self.p2,image=self.image,bd=0)
        self.hangmanImage.grid()
        #.......p2............left panel for hangman image........................................................................
    
        self.p3=Frame(self.pjoin,bg="#ffffff",bd=2,relief=RAISED,highlightcolor="red")
        self.p3.config(highlightcolor="red")
        self.p3.grid(row=8,column=11)
        
        self.guess=Label(self.p3,text="Available Guesses:",font=("Arial Rounded MT Bold",8),bg="#ffffff")
        self.guess.grid(row=1,column=10,padx=10,pady=8)

        self.guess_text=Label(self.p3,text="9",fg="blue",font=("Arial Rounded MT Bold",8),bg="#ffffff")  #yay
        self.guess_text.grid(row=1,column=11,padx=10)

        self.guess_letter=Label(self.p3,text="Guessesd Letters:",font=("Arial Rounded MT Bold",8),bg="#ffffff")
        self.guess_letter.grid(row=2,column=10,padx=10)

        self.guess_letter_text=Label(self.p3,text="",fg="blue",font=("Arial Rounded MT Bold",8),bg="#ffffff")  #yay
        self.guess_letter_text.grid(row=2,column=11,padx=10)

        self.ngImage=PhotoImage(file="newgame.gif")
        self.new=Button(self.p3,image=self.ngImage,command="",bd=0,highlightthickness=0) #event/command yay
        self.new.grid(row=4,column=10,pady=10,columnspan=2)

        #........p3......right panel for available guess and new game button....................................................
        def aClick():
            print "a"
            self.match_letter_with_answer("a")
        def bClick():
            print "b"
            self.match_letter_with_answer("b")
        def cClick():
            print "c"
            self.match_letter_with_answer("c")
        def dClick():
            print "d"
            self.match_letter_with_answer("d")
        def eClick():
            print "e"
            self.match_letter_with_answer("e")
        def fClick():
            print "f"
            self.match_letter_with_answer("f")
        def gClick():
            print "g"
            self.match_letter_with_answer("g")
        def hClick():
            print "h"
            self.match_letter_with_answer("h")
        def iClick():
            print "i"
            self.match_letter_with_answer("i")
        def jClick():
            print "j"
            self.match_letter_with_answer("j")
        def kClick():
            print "k"
            self.match_letter_with_answer("k")
        def lClick():
            print "l"
            self.match_letter_with_answer("l")
        def mClick():
            print "m"
            self.match_letter_with_answer("m")
        def nClick():
            print "n"
            self.match_letter_with_answer("n")
        def oClick():
            print "o"
            self.match_letter_with_answer("o")
        def pClick():
            print "p"
            self.match_letter_with_answer("p")
        def qClick():
            print "q"
            self.match_letter_with_answer("q")
        def rClick():
            print "r"
            self.match_letter_with_answer("r")
        def sClick():
            print "s"
            self.match_letter_with_answer("s")
        def tClick():
            print "t"
            self.match_letter_with_answer("t")
        def uClick():
            print "u"
            self.match_letter_with_answer("u")
        def vClick():
            print "v"
            self.match_letter_with_answer("v")
        def wClick():
            print "w"
            self.match_letter_with_answer("w")
        def xClick():
            print "x"
            self.match_letter_with_answer("x")
        def yClick():
            print "y"
            self.match_letter_with_answer("y")
        def zClick():
            print "z"
            self.match_letter_with_answer("z")

        
            
                    
        
        self.p6=Frame(self.container,bg="#ffffff")
        self.p6.pack()
        
        self.p5=Frame(self.p6,bg="#ffffff")
        self.p5.grid(pady=12)

        self.aImage=PhotoImage(file="a.gif")
        self.a=Button(self.p5,image=self.aImage,bg="#ffffff",bd=0,highlightthickness=0,command= aClick)     #a-z buttons
        self.a.grid(row=1,column=1,padx=2,pady=2)                                                           #event/command yay

        self.bImage=PhotoImage(file="b.gif")
        self.b=Button(self.p5,image=self.bImage,bg="#ffffff",bd=0,highlightthickness=0,command= bClick)
        self.b.grid(row=1,column=2,padx=2)

        self.cImage=PhotoImage(file="c.gif")
        self.c=Button(self.p5,image=self.cImage,bg="#ffffff",bd=0,highlightthickness=0,command= cClick)
        self.c.grid(row=1,column=3,padx=2)

        self.dImage=PhotoImage(file="d.gif")
        self.d=Button(self.p5,image=self.dImage,bg="#ffffff",bd=0,highlightthickness=0,command= dClick)
        self.d.grid(row=1,column=4,padx=2)

        self.eImage=PhotoImage(file="e.gif")
        self.e=Button(self.p5,image=self.eImage,bg="#ffffff",bd=0,highlightthickness=0,command= eClick)
        self.e.grid(row=1,column=5,padx=2)

        self.fImage=PhotoImage(file="f.gif")
        self.f=Button(self.p5,image=self.fImage,bg="#ffffff",bd=0,highlightthickness=0,command= fClick)
        self.f.grid(row=1,column=6,padx=2)

        self.gImage=PhotoImage(file="g.gif")
        self.g=Button(self.p5,image=self.gImage,bg="#ffffff",bd=0,highlightthickness=0,command= gClick)
        self.g.grid(row=1,column=7,padx=2)

        self.hImage=PhotoImage(file="h.gif")
        self.h=Button(self.p5,image=self.hImage,bg="#ffffff",bd=0,highlightthickness=0,command= hClick)
        self.h.grid(row=2,column=1,pady=2)

        self.iImage=PhotoImage(file="i.gif")
        self.i=Button(self.p5,image=self.iImage,bg="#ffffff",bd=0,highlightthickness=0,command= iClick)
        self.i.grid(row=2,column=2)

        self.jImage=PhotoImage(file="j.gif")
        self.j=Button(self.p5,image=self.jImage,bg="#ffffff",bd=0,highlightthickness=0,command= jClick)
        self.j.grid(row=2,column=3)

        self.kImage=PhotoImage(file="k.gif")
        self.k=Button(self.p5,image=self.kImage,bg="#ffffff",bd=0,highlightthickness=0,command= kClick)
        self.k.grid(row=2,column=4)

        self.lImage=PhotoImage(file="l.gif")
        self.l=Button(self.p5,image=self.lImage,bg="#ffffff",bd=0,highlightthickness=0,command= lClick)
        self.l.grid(row=2,column=5)

        self.mImage=PhotoImage(file="m.gif")
        self.m=Button(self.p5,image=self.mImage,bg="#ffffff",bd=0,highlightthickness=0,command= mClick)
        self.m.grid(row=2,column=6)

        self.nImage=PhotoImage(file="n.gif")
        self.n=Button(self.p5,image=self.nImage,bg="#ffffff",bd=0,highlightthickness=0,command= nClick)
        self.n.grid(row=2,column=7)

        self.oImage=PhotoImage(file="o.gif")
        self.o=Button(self.p5,image=self.oImage,bg="#ffffff",bd=0,highlightthickness=0,command= oClick)
        self.o.grid(row=3,column=1,pady=2)

        self.pImage=PhotoImage(file="p.gif")
        self.p=Button(self.p5,image=self.pImage,bg="#ffffff",bd=0,highlightthickness=0,command= pClick)
        self.p.grid(row=3,column=2)

        self.qImage=PhotoImage(file="q.gif")
        self.q=Button(self.p5,image=self.qImage,bg="#ffffff",bd=0,highlightthickness=0,command= qClick)
        self.q.grid(row=3,column=3)

        self.rImage=PhotoImage(file="r.gif")
        self.r=Button(self.p5,image=self.rImage,bg="#ffffff",bd=0,highlightthickness=0,command= rClick)
        self.r.grid(row=3,column=4)

        self.sImage=PhotoImage(file="s.gif")
        self.s=Button(self.p5,image=self.sImage,bg="#ffffff",bd=0,highlightthickness=0,command= sClick)
        self.s.grid(row=3,column=5)

        self.tImage=PhotoImage(file="t.gif")
        self.t=Button(self.p5,image=self.tImage,bg="#ffffff",bd=0,highlightthickness=0,command= tClick)
        self.t.grid(row=3,column=6)
     
        self.uImage=PhotoImage(file="u.gif")
        self.u=Button(self.p5,image=self.uImage,bg="#ffffff",bd=0,highlightthickness=0,command= uClick)
        self.u.grid(row=3,column=7)

        self.vImage=PhotoImage(file="v.gif")
        self.v=Button(self.p5,image=self.vImage,bg="#ffffff",bd=0,highlightthickness=0,command= vClick)
        self.v.grid(row=4,column=2,pady=2)

        self.wImage=PhotoImage(file="w.gif")
        self.w=Button(self.p5,image=self.wImage,bg="#ffffff",bd=0,highlightthickness=0,command= wClick)
        self.w.grid(row=4,column=3)

        self.xImage=PhotoImage(file="x.gif")
        self.x=Button(self.p5,image=self.xImage,bg="#ffffff",bd=0,highlightthickness=0,command= xClick)
        self.x.grid(row=4,column=4)

        self.yImage=PhotoImage(file="y.gif")
        self.y=Button(self.p5,image=self.yImage,bg="#ffffff",bd=0,highlightthickness=0,command= yClick)
        self.y.grid(row=4,column=5)

        self.zImage=PhotoImage(file="z.gif")
        self.z=Button(self.p5,image=self.zImage,bg="#ffffff",bd=0,highlightthickness=0,command= zClick)
        self.z.grid(row=4,column=6)

    
        
        #........p5........pannen for a-z buttons...........................................................................


        

        

        
################    MAIN MENU #######################
    
root =Tk() # create a Tk root window



def system_quit():
    root.destroy()

menubar=Menu(root)  #menubar
fileMenu=Menu(menubar,tearoff=0,bg="black",activebackground="skyblue",fg="white",font=("Impact",12))
#fileMenu.add_command(label="New Game",command="")  #command yay
#fileMenu.add_command(label="Main Menu",command="")
#fileMenu.add_separator()
fileMenu.add_command(label="Quit",command=system_quit)
menubar.add_cascade(label="Option",menu=fileMenu)
root.config(menu=menubar)



#w = 598 # width for the Tk root
w = 600 # width for the Tk root
h = 720 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/25) - (h/25)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))


body=bodyGui(root)
#body = MainMenu(root)
#root.resizable(0,0)

root.mainloop() # starts the mainloop      


