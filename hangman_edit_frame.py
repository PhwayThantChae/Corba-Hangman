#import tkinter as tk   # python3
import Tkinter as tk   # python
from random import randint
from Tkinter import *
import sys
import tkMessageBox

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
        self.container = tk.Frame(self,bg="#e83232")
        self.container.pack(side="top", fill="both", expand=True)
        #container.pack()
        #container.grid_rowconfigure(0, weight=1)
        #container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.score = 0
        self.highscore = 0

        
        self.class_construction()

        self.show_frame("StartPage")

        self.menubar=Menu(self)  #menubar
        self.fileMenu=Menu(self.menubar,tearoff=0,bg="black",activebackground="skyblue",fg="white",font=("Impact",12))
        self.fileMenu.add_command(label="Main Menu",command=self.call_Main)  #command yay
        self.fileMenu.add_command(label="New Game",command=self.call_New)  #command yay
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Quit",command=self.system_quit)
        self.menubar.add_cascade(label="Option",menu=self.fileMenu)
        self.config(menu=self.menubar)

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
        frame.tkraise()

    def system_quit(self):
        self.frames["StartPage"].destroy()
        self.frames["PageOne"].destroy()
        self.frames.clear()
        self.destroy()

    def call_Main(self):
        self.frames["StartPage"].destroy()
        self.frames["PageOne"].destroy()
        self.frames={}
        #self.show_score(self.score)
        self.class_construction()
        self.show_score(self.score)
        self.show_highscore(self.highscore)
        self.show_frame("StartPage")

    def call_New(self):
        self.frames["StartPage"].destroy()
        self.frames["PageOne"].destroy()
        self.frames={}
        self.class_construction()
        #print "New :" + str(self.score)
        print self.frames
        self.score =  self.get_score()
        self.highscore = self.get_highscore()
        self.show_frame("PageOne")


    def show_score(self,num):
        
        self.score = num

    def get_score(self):
        return self.score
    
    def show_highscore(self,num):
        self.score = num

    def get_highscore(self):
        return self.highscore
        
        

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        
        self.main = Frame(self,bg="#e83232")
        self.main.grid(row=1,column=3)

        self.play_logo=PhotoImage(file="hangman_main.gif")
        self.c_main=Button(self.main,image=self.play_logo,bg="#e83232",bd=0,highlightthickness=0,command="")
        self.c_main.grid(row=1,column=6,padx=40,pady=20)

        self.play_game=PhotoImage(file="Play.gif")
        self.play_game_button=Button(self.main,image=self.play_game,bg="#e83232",bd=0,highlightthickness=0,command= lambda: controller.show_frame("PageOne"))
        self.play_game_button.grid(row=2,column=6,padx=70,pady=50)



class PageOne(tk.Frame):

    c = 9
    r = 9
    final_answer = ""
    final_list=[]
    already_guessed = ""
    count_right = 0
    score = 0
    

    def gameover(self):
        ask_question_answer = tkMessageBox.askquestion("GAME OVER","Seriously, Don't hang yourself next time. Do you want to play again?")

        if ask_question_answer == "yes" :
            self.controller.show_score(0)
            self.controller.call_New()
        else:
            self.controller.system_quit()
        

    def success_gameover(self):

        
        ask_question_answer = tkMessageBox.askquestion("YOU DID IT!!","Congratulation. Your maximum score is "+ str(self.controller.get_score())+". Do you want to play again?")

        if ask_question_answer == "yes" :
            self.controller.call_New()
        else:
            self.controller.system_quit()
        

    #def hangman_image_error(self,num):
    def hangman_image_error(self,num):
        #global hangmanImage
        print num
        if( num == 8):
            file_path = "hangman_one.gif"
        elif( num == 7):
            file_path = "hangman_two.gif"
        elif( num == 6):
            file_path = "hangman_three.gif"
        elif( num == 5):
            file_path = "hangman_four.gif"
        elif( num == 4):
            file_path = "hangman_five.gif"
        elif( num == 3):
            file_path = "hangman_six.gif"
        elif( num == 2):
            file_path = "hangman_seven.gif"
        elif( num == 1):
            file_path = "hangman_eight.gif"
        else:
            file_path = "hangman_nine.gif"
            
        
        
        #self.hangmanImage.config(image="")
        self.hangmanImage.destroy()
        self.image=PhotoImage(file=file_path)   #yay
        self.hangmanImage=Label(self.bg_guess,image=self.image,bd=0)
        self.hangmanImage.grid()
        if (num == 0):
            self.gameover()

    def hangman_image_success(self,num):
        if (num == len(self.get_answer)):
            PageOne.score = PageOne.score + 1
            #print "Hangman_image_success PageOne.score:"+str(PageOne.score)
            self.score_value.config(text=str(PageOne.score))
            self.controller.show_score(PageOne.score)
            self.success_gameover()

    def match_letter_with_answer(self,letter):

        print PageOne.final_list
        
        #PageOne.already_guessed = PageOne.already_guessed + letter
        #self.guess_letter_text.config(text=PageOne.already_guessed)
       
        right_flag = 0
        
        key = 0
        for key,i in enumerate(self.get_answer):
            if(i == letter):
                
                if(PageOne.final_list[key] == '0' or PageOne.final_list[key] == '_ ' or PageOne.final_list[key] == '_'):
                
                    PageOne.final_list[key] = i
                    right_flag = 1
                    PageOne.count_right = PageOne.count_right + 1
                
            else:
                if(PageOne.final_list[key] == '1' or PageOne.final_list[key] == ' '):
                    PageOne.final_list[key] = ' '
                    
                if( PageOne.final_list[key] == '0' or PageOne.final_list[key] == '_' or PageOne.final_list[key] == '_ '):
                    PageOne.final_list[key] =  '_ '
                

        print_answer = ''.join(PageOne.final_list)
        print print_answer
        self.answer.config(text=print_answer)
        
        
        if(right_flag == 1):
            PageOne.r = PageOne.r-1
            self.hangman_image_success(PageOne.count_right)
        else:
            PageOne.c =PageOne.c - 1
            if(PageOne.c >= 0):
                self.guess_text.config(text=str(PageOne.c))
            self.hangman_image_error(PageOne.c)

        


    def __init__(self, parent, controller):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        self.controller = controller

        PageOne.final_answer = ""
        PageOne.final_list=[]
        PageOne.already_guessed = ""
        PageOne.c =9
        PageOne.r = 9
        PageOne.count_right = 0
        ### Score ####
        PageOne.score = self.controller.get_score()
        
        
       
        #Invoke the get_answer operation

        #Get random number for question
        self.random_question = 0
        print "question no :"+ str(hangmano._get_ques_no())
        self.random_question = randint(1,hangmano._get_ques_no())
        print "self.random_question :"+ str(self.random_question)
        self.get_question = hangmano.get_question(str(self.random_question))
        self.get_answer = hangmano.get_answer(str(self.random_question))

        for i in range(len(self.get_answer)):
            if(self.get_answer[i] == " "):
                PageOne.final_answer += str('1')
                PageOne.count_right = PageOne.count_right + 1
            else:
                PageOne.final_answer += str('0')
        PageOne.final_list = list(PageOne.final_answer)


    
        #self.label=Label(self.controller, text="Please don't die!",font=("OratorStd",21,"bold"),fg="black",bg="white")
        #self.label.grid(row=1,column=1,rowspan=6,columnspan=20,pady=5)
        #label = tk.Label(self, text="This is page 1", font=TITLE_FONT)
        #label.pack(side="top", fill="x", pady=10)
        #self.label.pack(side="top",fill="x",pady=10)

        self.bg_qanda = Frame(self,bg="#e83232")
        self.bg_qanda.grid(row=1,column=12)

        self.q=Label(self.bg_qanda,text="Questions :",font=("AdobeMyungjoStd-Medium",15,"bold"),bg="#e83232",fg="black",justify=LEFT)#fg="#f40505"
        self.q.grid(row=1, column=1,pady=10)
        
        self.question=Label(self.bg_qanda,text=self.get_question,fg="black",font=("AdobeMyungjoStd-Medium",15,"bold"),bg="#e83232", wraplength=280) #yay
        self.question.grid(row=1,column=2,pady=10)
     
        self.ans=Label(self.bg_qanda,text="Answer :",fg="black",font=("AdobeMyungjoStd-Medium",15,"bold"),bg="#e83232",justify=LEFT)
        self.ans.grid(row=2,column=1)

        #For answer slots to appear randomly with _
        print self.get_answer
        answer_slot = ""
        for i in range(0,len(self.get_answer)):
            if(self.get_answer[i] == " "):
                answer_slot= answer_slot+" "
            answer_slot = answer_slot+"_ "
       
            
        self.answer=Label(self.bg_qanda,text=answer_slot,fg="black",font=("AdobeMyungjoStd-Medium",15,"bold"),bg="#e83232")   #yay
        self.answer.grid(row=2,column=2)

        

#####################################
        self.bg_guess = Frame(self.bg_qanda,bg="#e83232")
        self.bg_guess.grid(row=3,column=2,padx=8,pady=8)
        

        self.image=PhotoImage(file="blank.gif")   #yay
        self.hangmanImage=Label(self.bg_guess,image=self.image,bd=0,padx = 16)
        self.hangmanImage.grid()

        #.......p2............left panel for hangman image........................................................................

        def aClick():
            print "a"
            self.a.config(state='disabled')
            self.match_letter_with_answer("a")
        def bClick():
            print "b"
            self.b.config(state='disabled')
            self.match_letter_with_answer("b")
        def cClick():
            print "c"
            self.c.config(state='disabled')
            self.match_letter_with_answer("c")
        def dClick():
            print "d"
            self.d.config(state='disabled')
            self.match_letter_with_answer("d")
        def eClick():
            print "e"
            self.e.config(state='disabled')
            self.match_letter_with_answer("e")
        def fClick():
            print "f"
            self.f.config(state='disabled')
            self.match_letter_with_answer("f")
        def gClick():
            print "g"
            self.g.config(state='disabled')
            self.match_letter_with_answer("g")
        def hClick():
            print "h"
            self.h.config(state='disabled')
            self.match_letter_with_answer("h")
        def iClick():
            print "i"
            self.i.config(state='disabled')
            self.match_letter_with_answer("i")
        def jClick():
            print "j"
            self.j.config(state='disabled')
            self.match_letter_with_answer("j")
        def kClick():
            print "k"
            self.k.config(state='disabled')
            self.match_letter_with_answer("k")
        def lClick():
            print "l"
            self.l.config(state='disabled')
            self.match_letter_with_answer("l")
        def mClick():
            print "m"
            self.m.config(state='disabled')
            self.match_letter_with_answer("m")
        def nClick():
            print "n"
            self.n.config(state='disabled')
            self.match_letter_with_answer("n")
        def oClick():
            print "o"
            self.o.config(state='disabled')
            self.match_letter_with_answer("o")
        def pClick():
            print "p"
            self.p.config(state='disabled')
            self.match_letter_with_answer("p")
        def qClick():
            print "q"
            self.q.config(state='disabled')
            self.match_letter_with_answer("q")
        def rClick():
            print "r"
            self.r.config(state='disabled')
            self.match_letter_with_answer("r")
        def sClick():
            print "s"
            self.s.config(state='disabled')
            self.match_letter_with_answer("s")
        def tClick():
            print "t"
            self.t.config(state='disabled')
            self.match_letter_with_answer("t")
        def uClick():
            print "u"
            self.u.config(state='disabled')
            self.match_letter_with_answer("u")
        def vClick():
            print "v"
            self.v.config(state='disabled')
            self.match_letter_with_answer("v")
        def wClick():
            print "w"
            self.w.config(state='disabled')
            self.match_letter_with_answer("w")
        def xClick():
            print "x"
            self.x.config(state='disabled')
            self.match_letter_with_answer("x")
        def yClick():
            print "y"
            self.y.config(state='disabled')
            self.match_letter_with_answer("y")
        def zClick():
            print "z"
            self.z.config(state='disabled')
            self.match_letter_with_answer("z")

        

        ##################### Available Guessed #################################################
        
        self.guess=Label(self.bg_qanda,text="Available Guesses:",font=("Arial Rounded MT Bold",8),bg="green",wraplength=100)
        self.guess.grid(row=1,column=3)

        self.guess_text=Label(self.bg_qanda,text="9",fg="blue",font=("Arial Rounded MT Bold",8),bg="green")  #yay
        self.guess_text.grid(row=1,column=4,padx = 50,pady=5)

        self.score_text=Label(self.bg_qanda,text="Score:",font=("Arial Rounded MT Bold",8),bg="green",wraplength=100)
        self.score_text.grid(row=2,column=3,padx = 5)

        self.score_value=Label(self.bg_qanda,text=str(self.controller.get_score()),font=("Arial Rounded MT Bold",8),bg="green")  #yay
        self.score_value.grid(row=2,column=4,pady=5,padx = 50)

        self.highscore_text=Label(self.bg_qanda,text="High Score:",font=("Arial Rounded MT Bold",8),bg="green",wraplength=100)
        self.highscore_text.grid(row=3,column=3)

        self.highscore_value=Label(self.bg_qanda,text=str(self.controller.get_highscore()),font=("Arial Rounded MT Bold",8),bg="green")  #yay
        self.highscore_value.grid(row=3,column=4)

        

        

        self.p5=Frame(self.bg_qanda,bg="#e83232")
        self.p5.grid(row=6,column=2,padx=20,pady=70)

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


        
        
        
        #llabel = tk.Label(self, text="This is page 1", font=TITLE_FONT)
        #llabel.pack(side="top", fill="x", pady=10)
        #button = tk.Button(self, text="Go to the start page",
                           #command=lambda: controller.show_frame("StartPage"))
        #button.pack()

    




if __name__ == "__main__":

    app = SampleApp()
        #w = 598 # width for the Tk root
    w = 630 # width for the Tk root
    h = 750 # height for the Tk root

# get screen width and height
    ws = app.winfo_screenwidth() # width of the screen
    hs = app.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/25) - (h/25)
    # set the dimensions of the screen 
    # and where it is placed
    app.geometry('%dx%d+%d+%d' % (w, h, x, y))
    app.resizable(0,0)
    app.mainloop()
