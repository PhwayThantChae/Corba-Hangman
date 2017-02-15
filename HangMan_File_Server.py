import sys
from omniORB import CORBA, PortableServer
import csv

#Import the stubs for the naming service
import CosNaming

#Import the stubs and skeletons for the Program_Hangman module
import Program_Hangman, Program_Hangman__POA

hangman_answer = {}

hangman_question = {}

#Reading from Quiz files and add into hangman_answer and hangman_question dictionaries

with open('Quiz.txt', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        hangman_question[row[0]] = row[1]
        hangman_answer[row[0]] = row[2]
    

#Define an implementation of the Hangman interface
#ques_no is for the number of questions in quiz so that we can get range random numbers for client program
class Hangman_class(Program_Hangman__POA.HangMan):

   def __init__(self,a): self._ques_no = a

   def _set_ques_no(self, a) : self._ques_no = a

   def _get_ques_no(self) : return self._ques_no
        
    
   def get_answer(self,number):
        for ans in hangman_answer.keys():
            if (number == ans):
                return hangman_answer[number]
   def get_question(self,number):
        for ans in hangman_question.keys():
            if (number == ans):
                return hangman_question[number]
    


# Initialise the ORB
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

# Find the root POA
poa = orb.resolve_initial_references("RootPOA")

#Creae an instance of Hangman_class
hangmanc = Hangman_class(len(hangman_question))


#Create an object reference, and implicitly activate the object
hangmano = hangmanc._this()

# Obtain a reference to the root naming context
obj         = orb.resolve_initial_references("NameService")
rootContext = obj._narrow(CosNaming.NamingContext)

if rootContext is None:
    print "Failed to narrow the root naming context"
    sys.exit(1)

#Bind a context named "hangman.my_hangman" to the root context
name = [CosNaming.NameComponent("hangman","my_hangman")]

try:
    testContext = rootContext.bind_new_context(name)
    print "New hangman context bounc"

except CosNaming.NamingContext.AlreadyBound, ex:
    print "Hangman context already exists"
    obj = rootContext.resolve(name)
    testContext = obj._narrow(CosNaming.NamingContext)
    if testContext is None:
        print "hangman.my_hangman exists but is not a NamingContext"
        sys.exit(1)

#Bind the hangman object to the hangman context
name = [CosNaming.NameComponent("ExampleHangman", "Object")]


try:
    testContext.bind(name,hangmano)
    print "New ExampleHangman object bound"

except CosNaming.NamingContext.AlreadyBound:
    testContext.rebind(name,hangmano)
    print "ExampleHangman binding already existed -- rebound"

    # Note that is should be sufficient to just call rebind() without
    # calling bind() first. Some Naming service implementations
    # incorrectl raise NotFound if rebind() is called for an unknown
    # name, so we use teh two-stage approach above

#Activate the POA
poaManager = poa._get_the_POAManager()
poaManager.activate()

# Everything is running now, but if this thread drops out of the end
# of the file, the process will exit. orb.run() just blocks until the
# ORB is shut down
orb.run()
    
        
