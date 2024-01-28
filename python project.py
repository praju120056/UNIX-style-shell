import time
import os
import platform
class Question:
    def __init__(self, text, choices, correct_choice):
        self.text = text
        self.choices = choices
        self.correct_choice = correct_choice

    def display(self):
        print(self.text)
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    def check_answer(self, choice):
        return choice == self.correct_choice

    def modify_options(self):
        print(f"Current options: {self.choices}")
        new_options = [input(f"Enter new option {i}: ") for i in range(1, 5)]
        self.choices = new_options

    def modify_question(self):
        new_text = input("Enter the new question text: ")
        new_choices = [input(f"Enter new choice {i}: ") for i in range(1, 5)]
        new_correct_choice = int(input("Enter the new correct choice number: "))
        self.text = new_text
        self.choices = new_choices
        self.correct_choice = new_correct_choice


class Quiz:
    def __init__(self, questions, time_limit_per_question=15):
        self.questions = questions
        self.time_limit_per_question = time_limit_per_question
        self.scores = {}  # Dictionary to store student scores

    def start_quiz(self, student_name):
        print(f"Welcome, {student_name}, to the Online Quiz!")

        total_score = 0
        for i, question in enumerate(self.questions, start=1):
            print(f"\nQuestion {i}:")
            question.display()

            start_time = time.time()
            user_choice = None
            time_up = False

            while user_choice is None and not time_up:
                elapsed_time = time.time() - start_time

                if elapsed_time > self.time_limit_per_question:
                    print(f"\nTime's up for Question {i}! Moving to the next question.")
                    time.sleep(1)  # Add a small delay for better readability
                    time_up = True
                else:
                    try:
                        user_choice = int(input("Your choice (enter the number): "))
                    except ValueError:
                        print("Invalid input. Please enter a number.")

            if not time_up:
                if question.check_answer(user_choice):
                    print("Correct!")
                    total_score += 1
                else:
                    print(f"Wrong!")

        print(f"\nQuiz completed, {student_name}!")
        print(f"Your total score: {total_score}/{len(self.questions)}")

        # Store the total score in the dictionary
        self.scores[student_name] = total_score

    def display_scores(self):
        print("\nPrevious Test Scores:")
        for student, score in self.scores.items():
            print(f"{student}: {score}/{len(self.questions)}")

    def add_question(self, new_question):
        self.questions.append(new_question)

    def modify_question_options(self, question_index):
        if 0 <= question_index < len(self.questions):
            self.questions[question_index].modify_options()
        else:
            print("Invalid question index.")

    def modify_question(self, question_index):
        if 0 <= question_index < len(self.questions):
            self.questions[question_index].modify_question()
        else:
            print("Invalid question index.")

class Player:
    def __init__(self, name):
        self.name = name

    def display_player_info(self):
        print(f"\nPlayer: {self.name}")


class Teacher:
    def __init__(self, password):
        self.password = password

    def authenticate(self, entered_password):
        return entered_password == self.password

    def add_question(self):
        question_text = input("Enter the question: ")
        choices = [input(f"Enter choice {i}: ") for i in range(1, 5)]
        correct_choice = int(input("Enter the correct choice number: "))
        return Question(question_text, choices, correct_choice)

    def modify_question_options(self, quiz, question_index):
        quiz.modify_question_options(question_index)

    def modify_question(self, quiz, question_index):
        quiz.modify_question(question_index)

    def view_scores(self, quiz):
        quiz.display_scores()
def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
print("\t"*5,"WELCOME TO ONLINE QUIZ PORTAL:\n\n")

# Teacher sets the password
teacher_password = "teacher123"

# Create a Teacher object
teacher = Teacher(teacher_password)

# Ask the user whether they are a student or a teacher
user_type = input("Are you a student or a teacher? (student/teacher): ").lower()

# Depending on the user type, take appropriate actions
if user_type == "teacher":
    # Authenticate the teacher
    entered_password = input("Enter teacher password to add questions: ")
    if teacher.authenticate(entered_password):
        # Teacher can add questions
        num_questions = int(input("Enter the number of questions to add: "))
        time_limit_per_question = int(input("Enter the time limit per question: "))
        quiz_questions = [teacher.add_question() for _ in range(num_questions)]

        # If there are questions, allow the teacher to modify options or the entire question, or conduct the quiz
        if quiz_questions:
            quiz = Quiz(quiz_questions, time_limit_per_question=15)

            while True:
                choice = input("Do you want to modify questions or conduct the quiz? (modify/conduct):\n Enter exit if you want to stop: ").lower()
                
                if choice == "modify":
                    # Allow the teacher to modify options or the entire question for an existing question
                    modify_choice = input("Do you want to modify options or the entire question? (options/question): ").lower()

                    question_index_to_modify = int(input("Enter the index of the question to modify (0-based): "))

                    if modify_choice == "options":
                        teacher.modify_question_options(quiz, question_index_to_modify)
                    elif modify_choice == "question":
                        teacher.modify_question(quiz, question_index_to_modify)
                    else:
                        print("Invalid choice. No modifications made.")

                    # Display modified question options or the entire question
                    print("\nModified Question:")
                    quiz.questions[question_index_to_modify].display()

                elif choice == "conduct":
                    # Allow the teacher to conduct the quiz
                    clear_screen()
                    num_students = int(input("Enter the number of students: "))

                    # Create Player objects for each student
                    students = [Player(input(f"Enter the name of student {i + 1}: ")) for i in range(num_students)]

                    # Display player information, start the quiz for each student, and display scores
                    for student in students:
                        student.display_player_info()
                        quiz.start_quiz(student.name)
                        clear_screen()  # Clear the screen after each student takes the test

                    # Display previous test scores
                    quiz.display_scores()
                    clear_screen()

                    # Ask the user again after quiz is conducted
                    user_type = input("Are you a student or a teacher? (student/teacher): ").lower()

                    # If the user is a teacher, allow access to marks; otherwise, print farewell message
                    if user_type == "teacher":
                        entered_password = input("Enter teacher password to view scores: ")
                        if teacher.authenticate(entered_password):
                            teacher.view_scores(quiz)
                        else:
                            print("Authentication failed. Access denied to scores.")
                    else:
                        print("\t"*5, "QUIZ HAS ENDED. GOODBYE!!")
                        break
                elif choice == 'exit':
                    print("Thank you!!\nGOODBYE")
                    break
                else:
                    print("Invalid choice. Try again.")

    else:
        print("Authentication failed. You are a student.")
else:
    print("Question Paper is not yet set. Access denied.")
