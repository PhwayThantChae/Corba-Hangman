import csv
from collections import defaultdict

questions = {}
answers = {}


with open('Quiz.txt', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        questions[row[0]] = row[1]
        answers[row[0]] = row[2]

print "Questions : " + str(questions)
print "Answers : " + str(answers)
