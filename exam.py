import random

# ANSI escape sequences for colours and effects
RED = '\u001b[31m'
GREEN = '\u001b[32m'
YELLOW = '\u001b[33m'
BLUE = '\u001b[34m'
CYAN = '\u001b[36m'
MAGENTA = '\u001b[35m'
RESET = '\u001b[0m'


def colour_print(text: str, effect: str) -> None:
    """Print `text` using the ANSI sequences to change colour, etc"""
    print(f"{effect}{text}{RESET}")


def get_valid_choice():
    """Ask user for a choice until a valid one is entered."""
    valid_choices = {'A', 'B', 'C', 'D', 'E', 'NEXT', 'BACK', 'EXIT'}
    while True:
        choice = input("Choose an option (A/B/C/D/E/NEXT/BACK/EXIT): ").strip().upper()
        if choice in valid_choices:
            return choice
        colour_print("Invalid option. Please enter A, B, C, D, E, NEXT, BACK, or EXIT.", RED)


def Load_instructions():
    colour_print("Instructions:", RED)
    colour_print("1. Read each question carefully.", RED)
    colour_print("2. Choose the correct answer from the options provided.", RED)
    colour_print("3. Type 'NEXT' to move to the next question.", RED)
    colour_print("4. Type 'EXIT' to end the exam.", RED)
    colour_print("Good luck!\n", RED)


def line():
    print("*" * 80)


# ----------------- FILE PATHS -----------------
chemistry_filename = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\chemistry_questions.txt'
physics_filename = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\physics.txt'
maths_filename = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\mathematics.txt'
biology_filename = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\biology.txt'

crs_filename = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\crs.txt'
government_filename = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\government.txt'
literature_filename = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\literature.txt'
english_filename = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\english.txt'

account_filename = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\account.txt'
economics_filename = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\economics.txt'
commerce_filename = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\commerce.txt'

# ----------------- DEPARTMENT → SUBJECTS MAP -----------------
departments = {
    "SCIENCE": {
        "CHEMISTRY": (chemistry_filename, "Chemistry"),
        "PHYSICS": (physics_filename, "Physics"),
        "BIOLOGY": (biology_filename, "Biology"),
        "MATHEMATICS": (maths_filename, "Mathematics"),
    },
    "ART": {
        "CRS": (crs_filename, "CRS"),
        "GOVERNMENT": (government_filename, "Government"),
        "LITERATURE": (literature_filename, "Literature"),
        "ENGLISH": (english_filename, "English"),
    },
    "COMMERCIAL": {
        "ACCOUNT": (account_filename, "Account"),
        "ECONOMICS": (economics_filename, "Economics"),
        "COMMERCE": (commerce_filename, "Commerce"),
        "MATHEMATICS": (maths_filename, "Mathematics"),
    }
}


def run_exam(input_filename, subject_name, num_questions=25):
    """Runs an exam from a given question file."""
    with open(input_filename, 'r', encoding="UTF-8") as f:
        f.readline()  # skip header
        all_questions = [line.strip("\n").split("|") for line in f]

    questions = random.sample(all_questions, min(num_questions, len(all_questions)))

    index = 0
    answers = {}
    score = 0

    colour_print(f"Starting {subject_name} Exam...", GREEN)
    colour_print("Please wait while we load your exam...", YELLOW)
    colour_print("Exam loaded successfully!", GREEN)
    line()

    while 0 <= index < len(questions):
        q, *options, correct_answer = questions[index]
        question_number = index + 1
        print(f"\nQuestion {question_number} of {len(questions)}:")
        print(q, *options, sep="\t\n")

        if index in answers:
            colour_print(f"Previously selected: {answers[index]}", CYAN)

        user_choice = get_valid_choice()

        if user_choice == "EXIT":
            colour_print("Ending Exam.....", BLUE)
            break
        elif user_choice == "BACK":
            if index > 0:
                index -= 1
            else:
                colour_print("You are at the first question. Can't go back further.", RED)
            continue
        elif user_choice == "NEXT":
            index += 1
            continue
        else:
            answers[index] = user_choice
            if user_choice == correct_answer:
                colour_print("Correct", GREEN)
                score += 1
            else:
                colour_print(f"Incorrect, {correct_answer} is the correct one.", RED)
            line()
            index += 1

    total_attempted = len(answers)
    percentage = (score / len(questions)) * 100 if questions else 0
    colour_print("\nExam Finished!", YELLOW)
    colour_print(f"Total Questions: {len(questions)}", CYAN)
    colour_print(f"Attempted: {total_attempted}", CYAN)
    colour_print(f"Correct: {score}", GREEN)
    colour_print(f"Score: {score}/{len(questions)} ({percentage:.2f}%)", MAGENTA)

    return answers, score


def load_question():
    print("Enter `EXIT` anytime to quit the exam ")

    overall_results = {}
    total_questions = 0
    total_correct = 0

    while True:
        choice = input("Choose your Department (Science/Commercial/Art or EXIT): ").strip().upper()
        if choice == "EXIT":
            break

        if choice not in departments:
            colour_print("Invalid choice. Please select a valid department.", RED)
            continue

        subjects = departments[choice]
        subject_names = "/".join(subjects.keys())
        subject_choice = input(f"Choose your Subject ({subject_names} or EXIT): ").strip().upper()

        if subject_choice == "EXIT":
            break
        if subject_choice not in subjects:
            colour_print(f"Invalid subject. Please enter one of: {subject_names}", RED)
            continue

        filename, subject_name = subjects[subject_choice]
        answers, score = run_exam(filename, subject_name)

        overall_results[subject_name] = {
            "attempted": len(answers),
            "correct": score,
            "total": len(answers)
        }
        total_questions += len(answers)
        total_correct += score

        again = input("\nDo you want to attempt another subject? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            break

    colour_print("\nFINAL EXAM SUMMARY", YELLOW)
    line()
    for subj, result in overall_results.items():
        percentage = (result["correct"] / result["total"]) * 100 if result["total"] else 0
        print(f"{subj}: {result['correct']}/{result['total']} ({percentage:.2f}%)")

    overall_percentage = (total_correct / total_questions) * 100 if total_questions else 0
    line()
    colour_print(f"TOTAL SCORE: {total_correct}/{total_questions} ({overall_percentage:.2f}%)", GREEN)
    colour_print("Thank you for using the Exam Simulator. Goodbye!", BLUE)


# ----------------- RUN PROGRAM -----------------
colour_print("Welcome to the Exam Simulator!", GREEN)
colour_print("Read Instructions Carefully", GREEN)
Load_instructions()
line()
load_question()
