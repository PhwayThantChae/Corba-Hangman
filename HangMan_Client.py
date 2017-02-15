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

bodyparts = ["head","spine","left arm","right arm","left leg","right leg"]
print hangmano.get_answer("3")
ans = hangmano.get_answer("3")
print "Number of questions " +str(hangmano._get_ques_no())

print hangmano.get_question("3")

c = len(bodyparts)-1
r = len(bodyparts)-1

final_answer = ""
for i in range(len(ans)):
    final_answer += str('0')
    
#wrong_flag = 0
right_flag = 0
final_list = list(final_answer)


while(c > 0 and r>0):
    
    input_answer = raw_input("Enter a character : ");
    right_flag = 0
    key = 0
    for key,i in enumerate(ans):
        if ( i == input_answer):
            if( final_list[key] == '0' or final_list[key] == '_'):
                final_list[key] =   i
                right_flag = 1

        else:
            if( final_list[key] == '0' or final_list[key] == '_'):
                final_list[key] =  '_'

    aa = ''.join(final_list)
    print aa
    if(right_flag == 1):
        r = r - 1
    else:
        c = c - 1
    print "c "+str(c)
    print "r "+str(r)
    
else:
    if(c<=0):
        print "You are dead"
    else:
        print "You win"


