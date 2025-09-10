import random
import threading
import time
from datetime import datetime

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
        choice = input(f"\n{CYAN}👉 Choose an option (A/B/C/D/E/NEXT/BACK/EXIT): {RESET}").strip().upper()
        if choice in valid_choices:
            return choice
        colour_print("❌ Invalid option. Please enter A, B, C, D, E, NEXT, BACK, or EXIT.", RED)


def Load_instructions():
    colour_print("\n📜 Instructions:", YELLOW)
    colour_print("1. Read each question carefully.", GREEN)
    colour_print("2. Choose the correct answer from the options provided.", GREEN)
    colour_print("3. Type 'NEXT' to move to the next question.", GREEN)
    colour_print("4. Type 'BACK' to return to the previous question.", GREEN)
    colour_print("5. Type 'EXIT' to end the exam.", GREEN)
    colour_print("6. Each department has a set duration for the whole exam.", GREEN)
    colour_print("✨ Good luck!\n", CYAN)


def line():
    print(f"{MAGENTA}{'*' * 80}{RESET}")


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
        "subjects": {
            "CHEMISTRY": (chemistry_filename, "Chemistry"),
            "PHYSICS": (physics_filename, "Physics"),
            "BIOLOGY": (biology_filename, "Biology"),
            "MATHEMATICS": (maths_filename, "Mathematics"),
        },
        "duration": 60 * 120  # 2 hours
    },
    "ART": {
        "subjects": {
            "CRS": (crs_filename, "CRS"),
            "GOVERNMENT": (government_filename, "Government"),
            "LITERATURE": (literature_filename, "Literature"),
            "ENGLISH": (english_filename, "English"),
        },
        "duration": 60 * 90  # 1.5 hours
    },
    "COMMERCIAL": {
        "subjects": {
            "ACCOUNT": (account_filename, "Account"),
            "ECONOMICS": (economics_filename, "Economics"),
            "COMMERCE": (commerce_filename, "Commerce"),
            "MATHEMATICS": (maths_filename, "Mathematics"),
        },
        "duration": 60 * 90  # 1.5 hours
    }
}


# ----------------- TIMER -----------------
def countdown_timer(seconds):
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        time_format = f"{mins:02}:{secs:02}"
        print(f"{YELLOW}⏳ Time Remaining: {time_format}{RESET}", end='\r')
        time.sleep(1)
    print(f"\n{RED}⏰ Time's up! Exam over!{RESET}")
    exit(0)


def run_exam(input_filename, subject_name, num_questions=25):
    """Runs an exam from a given question file."""
    with open(input_filename, 'r', encoding="UTF-8") as f:
        f.readline()  # skip header
        all_questions = [line.strip("\n").split("|") for line in f]

    questions = random.sample(all_questions, min(num_questions, len(all_questions)))

    index = 0
    answers = {}
    score = 0

    colour_print(f"\n🚀 Starting {subject_name} Exam...", GREEN)
    line()

    while 0 <= index < len(questions):
        q, *options, correct_answer = questions[index]
        question_number = index + 1
        print(f"\n{YELLOW}❓ Question {question_number} of {len(questions)}:{RESET}")
        print(q, *options, sep="\t\n")

        if index in answers:
            colour_print(f"📌 Previously selected: {answers[index]}", CYAN)

        user_choice = get_valid_choice()

        if user_choice == "EXIT":
            colour_print("🔚 Ending Exam...", BLUE)
            break
        elif user_choice == "BACK":
            if index > 0:
                index -= 1
            else:
                colour_print("⚠ You are at the first question. Can't go back further.", RED)
            continue
        elif user_choice == "NEXT":
            index += 1
            continue
        else:
            answers[index] = user_choice
            if user_choice == correct_answer:
                colour_print("✅ Correct!", GREEN)
                score += 1
            else:
                colour_print(f"❌ Incorrect, {correct_answer} is the correct one.", RED)
            line()
            index += 1

    return answers, score, len(questions)


def save_results(username, results, total_score, total_questions):
    """Save exam summary to a file in user's name."""
    filename = f"exam_results_{username}.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"👤 Student: {username}\n\n")
        for subj, result in results.items():
            percent = (result['correct'] / result['total']) * 100 if result['total'] else 0
            f.write(f"{subj:15}: {result['correct']}/{result['total']} ({percent:.2f}%)\n")
        overall_percent = (total_score / total_questions) * 100 if total_questions else 0
        f.write(f"\nTOTAL SCORE: {total_score}/{total_questions} ({overall_percent:.2f}%)\n")
        f.write("=" * 60 + "\n")
    colour_print(f"\n📁 Results saved to {filename}", CYAN)


def load_question():
    username = input(f"\n{CYAN}👤 Enter your name: {RESET}").strip().replace(" ", "_")

    colour_print("\n⚡ Enter `EXIT` anytime to quit the exam ", YELLOW)

    overall_results = {}
    total_questions = 0
    total_correct = 0

    choice = input(f"\n{CYAN}📚 Choose your Department (Science/Commercial/Art): {RESET}").strip().upper()
    if choice not in departments:
        colour_print("❌ Invalid department. Exiting...", RED)
        return

    subjects = departments[choice]["subjects"]
    exam_duration = departments[choice]["duration"]

    # start countdown timer for the whole department
    timer_thread = threading.Thread(target=countdown_timer, args=(exam_duration,), daemon=True)
    timer_thread.start()

    for subject_choice, (filename, subject_name) in subjects.items():
        answers, score, question_count = run_exam(filename, subject_name)

        overall_results[subject_name] = {
            "attempted": len(answers),
            "correct": score,
            "total": question_count
        }
        total_questions += question_count
        total_correct += score

    colour_print("\n📑 FINAL EXAM SUMMARY", YELLOW)
    line()
    for subj, result in overall_results.items():
        percentage = (result["correct"] / result["total"]) * 100 if result["total"] else 0
        print(f"{subj:15}: {result['correct']}/{result['total']} ({percentage:.2f}%)")

    overall_percentage = (total_correct / total_questions) * 100 if total_questions else 0
    line()
    colour_print(f"🏆 TOTAL SCORE: {total_correct}/{total_questions} ({overall_percentage:.2f}%)", GREEN)
    colour_print("🙏 Thank you for using the Exam Simulator. Goodbye!", BLUE)

    # save results to file
    save_results(username, overall_results, total_correct, total_questions)


# ----------------- RUN PROGRAM -----------------
colour_print("🎓 Welcome to the Exam Simulator!", GREEN)
colour_print("📢 Read Instructions Carefully", YELLOW)
Load_instructions()
line()
load_question()
