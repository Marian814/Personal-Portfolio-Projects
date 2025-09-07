import random
from QuizGame_QuestionModel import Question
from QuizGame_QuizData import question_data
from QuizGame_QuizBrain import QuizBrain

question_bank = []
for question in question_data:
    q = Question(question['question'], question['correct_answer'])
    question_bank.append(q)

random.shuffle(question_bank)

quiz = QuizBrain(question_bank)
while quiz.still_has_question():
    quiz.next_question()

print("You've completed the quiz!")
print(f"Your final score is {quiz.score}/{quiz.question_number}.")
