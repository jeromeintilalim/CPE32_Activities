from typing import List, Tuple
import random
import requests
import html
import time
import threading
import os

scoresheet: List[Tuple[str, int]] = []

class Quiz:
# jeryk
    def __init__(self, num_questions=5, difficulty=1, mode="classic"):
        self.scores = []
        self.correct_answers = []
        self.incorrect_answers = []
        self.num_questions = num_questions
        self.difficulty = difficulty
        self.mode = mode
        self.questions = self.load_questions()
        self.lives = 5  # For survival mode

    def load_questions(self):
        difficulty_map = {1: "easy", 2: "medium", 3: "hard"}
        url = f"https://opentdb.com/api.php?amount={self.num_questions}&difficulty={difficulty_map.get(self.difficulty, 'medium')}&type=multiple&category=18"
        response = requests.get(url)
        questions_data = response.json()
        questions = []
        if not questions_data.get('results'):
            print("Failed to fetch questions. Please check your internet connection or try again later.")
            return []
                
        for item in questions_data['results']:
            question = html.unescape(item['question'])
            correct_answer = html.unescape(item['correct_answer'])
            incorrect_answers = [html.unescape(answer) for answer in item['incorrect_answers']]
            choices = [correct_answer] + incorrect_answers
            random.shuffle(choices)
            correct_index = choices.index(correct_answer)
            formatted_question = {"question": question, "choices": choices, "correct": correct_index}
            questions.append(formatted_question)
        return questions
# ryu
    def get_user_input(self, prompt, accept_only_ABCD=True):
        user_input = input(prompt)
        if not accept_only_ABCD or user_input.upper() in ['A', 'B', 'C', 'D']:
            return user_input.upper() if accept_only_ABCD else user_input
        else:
            print("Please enter a valid choice (A, B, C, D)." if accept_only_ABCD else "Invalid input, please try again.")
            return self.get_user_input(prompt, accept_only_ABCD)

    def play(self):
        if self.mode == "1":
            self.play_classic()
        elif self.mode == "2":
            self.play_timed()
        elif self.mode == "3":
            self.play_survival()
        else:
            print(f"Unknown mode: {self.mode}")
# ardy
    def play_classic(self):
        for question in self.questions:
            print(question["question"])
            for idx, choice in enumerate(question["choices"]):
                print(f"{chr(idx+65)}. {choice}")
            answer = self.get_user_input("Your answer: ").upper()
            if ord(answer) - 65 == question["correct"]:
                print("Correct!")
                self.scores.append(1)
                self.correct_answers.append(question["question"])
            else:
                print("Wrong!")
                self.scores.append(0)
                self.incorrect_answers.append((question["question"], question["choices"], question["correct"]))
        self.show_scoresheet()

    def play_timed(self):
        def wait_for_input(question, choices):
            timer = 15
            print(question)
            for idx, choice in enumerate(choices):
                print(f"{chr(idx+65)}. {choice}")
            answer = [None]
            def get_user_answer():
                answer[0] = self.get_user_input("Your answer: \n", accept_only_ABCD=True).upper()
            input_thread = threading.Thread(target=get_user_answer)
            input_thread.start()
            start_time = time.time()
            while timer > 0 and input_thread.is_alive():
                print(f"Time left: {timer}s", end="\r")
                time.sleep(1)
                timer = 15 - int(time.time() - start_time)
                if timer <= 0:
                    print("\nTime's up!")
                    if not input_thread.is_alive():
                        input_thread.join()
                    else:
                        input_thread.join(timeout=1)
                    break
            return answer[0]
        
        for question in self.questions:
            user_answer = wait_for_input(question["question"], question["choices"])
            if user_answer is None or ord(user_answer) - 65 != question["correct"]:
                print("Wrong!")
                self.scores.append(0)
                self.incorrect_answers.append((question["question"], question["choices"], question["correct"]))
            else:
                print("Correct!")
                self.scores.append(1)
                self.correct_answers.append(question["question"])
        self.show_scoresheet()

    def play_survival(self):
        for question in self.questions:
            print(f"Lives: {self.lives}")
            print(question["question"])
            for idx, choice in enumerate(question["choices"]):
                print(f"{chr(idx+65)}. {choice}")
            answer = self.get_user_input("Your answer: ", accept_only_ABCD=True)
            if ord(answer) - 65 == question["correct"]:
                print("Correct!")
                self.scores.append(1)
                self.correct_answers.append(question["question"])
            else:
                print("Wrong!")
                self.scores.append(0)
                self.incorrect_answers.append((question["question"], question["choices"], question["correct"]))
                self.lives -= 1
                if self.lives == 0:
                    print("Game Over!")
                    self.scores.append(0)
                    self.show_scoresheet()
                    return
        self.show_scoresheet()
# rojan
    def show_scoresheet(self):
        if (len(scoresheet) > 0):
            print("Scoresheet:")
        total_score = sum(self.scores)
        print(f"Your score: {total_score}/{len(self.questions)}")
        player_name = input("Enter your name for the scoresheet: ")
        mode_text = "(Classic)" if self.mode == "1" else "(Timed)" if self.mode == "2" else "(Survival)"
        self.update_scoresheet(f"{player_name} {mode_text} - {total_score}/{len(self.questions)}")
        print(f"Thank you, {player_name}. Your score has been recorded.")

        while True:
            print("Enter 'N' to start a new quiz, 'Q' to view quiz summary, 'S' to view the scoresheet, or enter any other key to exit.")
            action = self.get_user_input("Choose an option: ", accept_only_ABCD=False)
            if action.lower() == 'n':
                initialize()
            elif action.lower() == 'q':
                self.quiz_summary()
            elif action.lower() == 's':
                self.display_scoresheet()
            else:
                print("Thank you for playing!")
                break
            
    def update_scoresheet(self, player_name_with_mode):
        global scoresheet
        scoresheet.append((player_name_with_mode))
# parcia
    def display_scoresheet(self):
        if (len(scoresheet) > 0):
            print("Scoresheet:")
        for idx, name in enumerate(scoresheet):
            print(f"{idx+1}. {name}")
        input("Press enter to return to the main menu.")
        initialize()
        
    def quiz_summary(self):
        print("\nQuiz Summary:")
        print("Correct Answers:")
        for question in self.correct_answers:
            print(f"\n- {question}")
        print("\nIncorrect Answers:")
        for question, choices, correct in self.incorrect_answers:
            print(f"\n- Question: {question}")
            print("  Choices:")
            for idx, choice in enumerate(choices):
                print(f"    {chr(idx+65)}. {choice}")
            print(f"  Correct Answer: {choices[correct]}")
        print("\n")

# lim
def initialize():
    os.system('cls')
    print("Welcome to the Team Allstar Computer Trivia Quiz!")
    while True:
        mode = input("\nChoose a game mode (1. Classic, 2. Timed, 3. Survival): ")
        if mode in ["1", "2", "3"]:
            break
        else:
            print("Invalid mode selected. Please choose from '1. Classic', '2. Timed', or '3. Survival'.")
    num_questions = 30 if mode == "3" else None
    while num_questions is None:
        try:
            num_questions = int(input("\nHow many questions would you like? (5-30): "))
            if 5 <= num_questions <= 30:
                break
            else:
                print("Number of questions must be between 5 and 30.")
        except ValueError:
            print("Please enter a valid number.")
    while True:
        try:
            difficulty_input = input("\nSelect difficulty (1: Easy, 2: Medium, 3: Hard): ")
            if difficulty_input.lower() in ["1", "easy"]:
                difficulty = 1
                break
            elif difficulty_input.lower() in ["2", "medium"]:
                difficulty = 2
                break
            elif difficulty_input.lower() in ["3", "hard"]:
                difficulty = 3
                break
            else:
                print("Please select a valid difficulty level (1: Easy, 2: Medium, 3: Hard).")
        except ValueError:
            print("Please enter a valid number.")
    quiz = Quiz(num_questions=num_questions, difficulty=difficulty, mode=mode)
    quiz.play()