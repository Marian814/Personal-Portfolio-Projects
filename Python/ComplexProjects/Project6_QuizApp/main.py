from Question_Model import Question
from Data import question_data
from Quiz_Brain import QuizBrain
from UI import QuizInterface

question_bank = []
for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)

quiz_ui = QuizInterface(quiz)
