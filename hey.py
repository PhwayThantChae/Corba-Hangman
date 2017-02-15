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

    
class PageOne(tk.Frame):

    from HangMan_Frame import SampleApp
    
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
        self.hangmanImage.grid(padx = 16)
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


    
        #self.label=Label(self.controller, text="Please don't die!",font=("OratorStd",21,"bold"),fg="#ff5a5a",bg="#ff5a5a")
        #self.label.grid(row=1,column=1,rowspan=6,columnspan=20,pady=5)
        #label = tk.Label(self, text="This is page 1", font=TITLE_FONT)
        #label.pack(side="top", fill="x", pady=10)
        #self.label.pack(side="top",fill="x",pady=10)

        self.bg_qanda = Frame(self,bg="#ff5a5a")
        self.bg_qanda.grid()

        self.p1=Frame(self.bg_qanda,bg="#ff5a5a",pady=10)
        self.p1.grid()
        
        self.q=Label(self.p1,text="Questions :",font=("AdobeMyungjoStd-Medium",15,"bold"),bg="#ff5a5a",fg="white",justify=LEFT)#fg="#f40505"
        self.q.grid(row=1, column=1,padx=10,pady=10)
        
        self.question=Label(self.p1,text=self.get_question,fg="white",font=("AdobeMyungjoStd-Medium",15,"bold"),bg="#ff5a5a", wraplength=430) #yay
        self.question.grid(row=1,column=3,pady=10,rowspan=2,padx=5)
     
        self.ans=Label(self.p1,text="Answer :",fg="white",font=("AdobeMyungjoStd-Medium",15,"bold"),bg="#ff5a5a",justify=LEFT)
        self.ans.grid(row=3,column=1,padx=20)

        #For answer slots to appear randomly with _
        print self.get_answer
        answer_slot = ""
        for i in range(0,len(self.get_answer)):
            if(self.get_answer[i] == " "):
                answer_slot= answer_slot+" "
            answer_slot = answer_slot+"_ "
       
        self.t=answer_slot            
        self.answer=Label(self.p1,text=self.t,fg="white",font=("AdobeMyungjoStd-Medium",15,"bold"),bg="#ff5a5a")   #yay
        self.answer.grid(row=3,column=3,columnspan=2)

        

#####################################
        self.pjoin=Frame(self.bg_qanda,bg="#ff5a5a")
        self.pjoin.grid(padx=10,pady=10)

        self.bg_guess = Frame(self.pjoin,bg="#ff5a5a")
        self.bg_guess.grid(row=8,column=9)
        

        self.image=PhotoImage(file="blank.gif")   #yay
        self.hangmanImage=Label(self.bg_guess,image=self.image,bd=0)
        self.hangmanImage.grid(padx = 16)

              ##################### Available Guessed #################################################

        self.p3=Frame(self.pjoin,bg="#ff5a5a",bd=2,relief=RAISED,highlightcolor="#ff5a5a")
        self.p3.grid(row=8,column=10,padx=5,columnspan=10)
        
        self.guess=Label(self.p3,text="Available Guesses   : ",font=("Arial Rounded MT Bold",8),bg="#ff5a5a")
        self.guess.grid(row=1,column=15,padx=10,pady=5)

        self.guess_text=Label(self.p3,text="9",fg="green",font=("AdobeGothicStd-Bold",11),bg="#ff5a5a")  #yay
        self.guess_text.grid(row=1,column=16,padx=10,pady=5)

        self.score_text=Label(self.p3,text="          Score          :",font=("Arial Rounded MT Bold",8),bg="#ff5a5a",wraplength=100)
        self.score_text.grid(row=2,column=15,padx=10,pady=5)

        self.score_value=Label(self.p3,text=str(self.controller.get_score()),font=("AdobeGothicStd-Bold",11),bg="#ff5a5a",fg="green")  #yay
        self.score_value.grid(row=2,column=16,padx=10,pady=5)

        self.ngImage=PhotoImage(file="newgame.gif")
        self.new=Button(self.p3,image=self.ngImage,bd=0,highlightthickness=0,bg="#ff5a5a",command=SampleApp.call_New) #event/command yay
        self.new.grid(row=4,column=15,columnspan=2,padx=10,pady=10)

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

        

  
        
        

        self.p5=Frame(self.bg_qanda,bg="#ff5a5a")
        self.p5.grid(pady=15)

        self.aImage=PhotoImage(file="a.gif")
        self.a=Button(self.p5,image=self.aImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= aClick)     #a-z buttons
        self.a.grid(row=1,column=1,padx=4,pady=2)                                                           #event/command yay

        self.bImage=PhotoImage(file="b.gif")
        self.b=Button(self.p5,image=self.bImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= bClick)
        self.b.grid(row=1,column=2,padx=4)

        self.cImage=PhotoImage(file="c.gif")
        self.c=Button(self.p5,image=self.cImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= cClick)
        self.c.grid(row=1,column=3,padx=4)

        self.dImage=PhotoImage(	file="d.gif")
        self.d=Button(self.p5,image=self.dImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= dClick)
        self.d.grid(row=1,column=4,padx=4)

        self.eImage=PhotoImage(file="e.gif")
        self.e=Button(self.p5,image=self.eImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= eClick)
        self.e.grid(row=1,column=5,padx=4)

        self.fImage=PhotoImage(file="f.gif")
        self.f=Button(self.p5,image=self.fImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= fClick)
        self.f.grid(row=1,column=6,padx=4)

        self.gImage=PhotoImage(file="g.gif")
        self.g=Button(self.p5,image=self.gImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= gClick)
        self.g.grid(row=1,column=7,padx=4)

        self.hImage=PhotoImage(file="h.gif")
        self.h=Button(self.p5,image=self.hImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= hClick)
        self.h.grid(row=2,column=1,pady=2)

        self.iImage=PhotoImage(file="i.gif")
        self.i=Button(self.p5,image=self.iImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= iClick)
        self.i.grid(row=2,column=2)

        self.jImage=PhotoImage(file="j.gif")
        self.j=Button(self.p5,image=self.jImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= jClick)
        self.j.grid(row=2,column=3)

        self.kImage=PhotoImage(file="k.gif")
        self.k=Button(self.p5,image=self.kImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= kClick)
        self.k.grid(row=2,column=4)

        self.lImage=PhotoImage(file="l.gif")
        self.l=Button(self.p5,image=self.lImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= lClick)
        self.l.grid(row=2,column=5)

        self.mImage=PhotoImage(file="m.gif")
        self.m=Button(self.p5,image=self.mImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= mClick)
        self.m.grid(row=2,column=6)

        self.nImage=PhotoImage(file="n.gif")
        self.n=Button(self.p5,image=self.nImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= nClick)
        self.n.grid(row=2,column=7)

        self.oImage=PhotoImage(file="o.gif")
        self.o=Button(self.p5,image=self.oImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= oClick)
        self.o.grid(row=3,column=1,pady=2)

        self.pImage=PhotoImage(file="p.gif")
        self.p=Button(self.p5,image=self.pImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= pClick)
        self.p.grid(row=3,column=2)

        self.qImage=PhotoImage(file="q.gif")
        self.q=Button(self.p5,image=self.qImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= qClick)
        self.q.grid(row=3,column=3)

        self.rImage=PhotoImage(file="r.gif")
        self.r=Button(self.p5,image=self.rImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= rClick)
        self.r.grid(row=3,column=4)

        self.sImage=PhotoImage(file="s.gif")
        self.s=Button(self.p5,image=self.sImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= sClick)
        self.s.grid(row=3,column=5)

        self.tImage=PhotoImage(file="t.gif")
        self.t=Button(self.p5,image=self.tImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= tClick)
        self.t.grid(row=3,column=6)
     
        self.uImage=PhotoImage(file="u.gif")
        self.u=Button(self.p5,image=self.uImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= uClick)
        self.u.grid(row=3,column=7)

        self.vImage=PhotoImage(file="v.gif")
        self.v=Button(self.p5,image=self.vImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= vClick)
        self.v.grid(row=4,column=2,pady=2)

        self.wImage=PhotoImage(file="w.gif")
        self.w=Button(self.p5,image=self.wImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= wClick)
        self.w.grid(row=4,column=3)

        self.xImage=PhotoImage(file="x.gif")
        self.x=Button(self.p5,image=self.xImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= xClick)
        self.x.grid(row=4,column=4)

        self.yImage=PhotoImage(file="y.gif")
        self.y=Button(self.p5,image=self.yImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= yClick)
        self.y.grid(row=4,column=5)

        self.zImage=PhotoImage(file="z.gif")
        self.z=Button(self.p5,image=self.zImage,bg="#ff5a5a",bd=0,highlightthickness=0,command= zClick)
        self.z.grid(row=4,column=6)

        self.label=Label(self.p5,bg="#ff5a5a")
        self.label.grid()
        
        
        
        #llabel = tk.Label(self, text="This is page 1", font=TITLE_FONT)
        #llabel.pack(side="top", fill="x", pady=10)
        #button = tk.Button(self, text="Go to the start page",
                           #command=lambda: controller.show_frame("StartPage"))
        #button.pack()

    




if __name__ == "__main__":

    app = SampleApp()
        #w = 598 # width for the Tk root
    w = 585 # width for the Tk root
    h = 623 # height for the Tk root

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
