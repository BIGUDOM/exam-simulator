import random
import threading
import time
from datetime import datetime
import os

# ---------- ANSI Colours ----------
RED = '\u001b[31m'
GREEN = '\u001b[32m'
YELLOW = '\u001b[33m'
BLUE = '\u001b[34m'
CYAN = '\u001b[36m'
MAGENTA = '\u001b[35m'
RESET = '\u001b[0m'

# ---------- Helper Printing ----------
def colour_print(text: str, effect: str) -> None:
    print(f"{effect}{text}{RESET}")

def line():
    print(f"{MAGENTA}{'*' * 80}{RESET}")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# ---------- Instructions ----------
def Load_instructions():
    colour_print("\n📜 Instructions:", YELLOW)
    colour_print("1. Read each question carefully.", GREEN)
    colour_print("2. Choose the correct answer from the options provided.", GREEN)
    colour_print("3. Type 'NEXT' to move to the next question.", GREEN)
    colour_print("4. Type 'BACK' to return to the previous question.", GREEN)
    colour_print("5. Type 'EXIT' to end the exam.", GREEN)
    colour_print("6. Each department has a set duration for the whole exam.", GREEN)
    colour_print("✨ Good luck!\n", CYAN)

# ---------- File Paths ----------
chemistry_filename = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\questions\chemistry_questions.txt'
physics_filename   = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\questions\physics.txt'
maths_filename     = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\questions\mathematics.txt'
biology_filename   = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\questions\biology.txt'

crs_filename       = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\questions\crs.txt'
government_filename= r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\questions\government.txt'
literature_filename= r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\questions\literature.txt'
english_filename   = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\questions\english.txt'

account_filename   = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\questions\account.txt'
economics_filename = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\questions\economics.txt'
commerce_filename  = r'C:\Users\Elitebook 1040 G6\OneDrive\Desktop\web developmen\pythonfiles\exam-project\questions\commerce.txt'

# ---------- Departments ----------
departments = {
    "SCIENCE": {
        "subjects": {
            "CHEMISTRY": (chemistry_filename, "Chemistry"),
            "PHYSICS":   (physics_filename, "Physics"),
            "BIOLOGY":   (biology_filename, "Biology"),
            "MATHEMATICS": (maths_filename, "Mathematics"),
        },
        "duration": 60 * 120
    },
    "ART": {
        "subjects": {
            "CRS":        (crs_filename, "CRS"),
            "GOVERNMENT": (government_filename, "Government"),
            "LITERATURE": (literature_filename, "Literature"),
            "ENGLISH":    (english_filename, "English"),
        },
        "duration": 60 * 90
    },
    "COMMERCIAL": {
        "subjects": {
            "ACCOUNT":    (account_filename, "Account"),
            "ECONOMICS":  (economics_filename, "Economics"),
            "COMMERCE":   (commerce_filename, "Commerce"),
            "MATHEMATICS": (maths_filename, "Mathematics"),
        },
        "duration": 60 * 90
    }
}

# ---------- Timer ----------
time_left_str = "00:00"
timer_running = True

def countdown_timer(duration):
    global time_left_str, timer_running
    timer_running = True
    start_time = time.time()
    while timer_running:
        elapsed = int(time.time() - start_time)
        remaining = max(duration - elapsed, 0)
        mins, secs = divmod(remaining, 60)
        time_left_str = f"{mins:02}:{secs:02}"
        if remaining == 0:
            print(f"\n{RED}⏰ Time's up! Exam over!{RESET}")
            os._exit(0)
        time.sleep(1)

def stop_timer():
    global timer_running
    timer_running = False

# ---------- Run Exam ----------
def run_exam(input_filename, subject_name, num_questions=25):
    global time_left_str
    with open(input_filename, 'r', encoding="utf-8") as f:
        f.readline()
        all_qs = [line.strip("\n").split("|") for line in f]

    questions = [[x.strip() for x in q] for q in all_qs]
    questions = random.sample(questions, min(num_questions, len(questions)))

    answers, score, index = {}, 0, 0
    colour_print(f"\n🚀 Starting {subject_name} Exam...", GREEN)

    while 0 <= index < len(questions):
        q, *options, correct = questions[index]
        labels = ['A', 'B', 'C', 'D', 'E'][:len(options)]
        pairs = list(zip(labels, options))
        random.shuffle(pairs)
        shuffled_labels, shuffled_opts = zip(*pairs)

        try:
            correct_label = shuffled_labels[
                [o.lower() for o in shuffled_opts].index(correct.lower())
            ]
        except ValueError:
            correct_label = None

        clear_screen()
        line()
        print(f"{CYAN}Subject: {subject_name}{RESET}")
        print(f"{YELLOW}⏳ Time Remaining: {time_left_str}{RESET}")
        print(f"{YELLOW}❓ Q{index+1} of {len(questions)}{RESET}\n{q}")
        for lbl, opt in pairs:
            print(f"{lbl}. {opt}")

        if index in answers:
            colour_print(f"📌 Previously selected: {answers[index]}", CYAN)

        user_choice = input(f"\n{CYAN}👉 Enter your choice (A/B/C/D/E/NEXT/BACK/EXIT): {RESET}").strip().upper()

        if user_choice == "EXIT":
            colour_print("🔚 Ending Exam...", BLUE)
            break
        elif user_choice == "BACK":
            index = max(0, index - 1)
            continue
        elif user_choice == "NEXT":
            index += 1
            continue
        else:
            answers[index] = user_choice
            if correct_label and user_choice == correct_label:
                colour_print("✅ Correct!", GREEN)
                score += 1
            else:
                if correct_label:
                    colour_print(f"❌ Incorrect. Correct: {correct_label}", RED)
                else:
                    colour_print("❌ Skipped: No correct match in file", RED)
            index += 1

    return answers, score, len(questions)

# ---------- Save Results ----------
def save_results(username, results, total_score, total_questions, department_choice):
    base_folder = "results"
    dept_map = {"SCIENCE": "science", "ART": "art", "COMMERCIAL": "commercial"}
    dept_folder = dept_map.get(department_choice, "other")

    student_folder = os.path.join(base_folder, dept_folder, username)
    os.makedirs(student_folder, exist_ok=True)

    filename = f"exam_results_{username}.txt"
    filepath = os.path.join(student_folder, filename)

    with open(filepath, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"👤 Student: {username}\n\n")
        for subj, result in results.items():
            percent = (result['correct'] / result['total']) * 100 if result['total'] else 0
            f.write(f"{subj:15}: {result['correct']}/{result['total']} ({percent:.2f}%)\n")
        overall_percent = (total_score / total_questions) * 100 if total_questions else 0
        f.write(f"\nTOTAL SCORE: {total_score}/{total_questions} ({overall_percent:.2f}%)\n")
        f.write("=" * 60 + "\n\n")

# ---------- Check Results ----------
def check_results():
    dept_choice = input(f"\n{CYAN}📚 Enter Department (Science/Commercial/Art): {RESET}").strip().upper()
    if dept_choice not in departments:
        colour_print("❌ Invalid department.", RED)
        return

    username = input(f"\n{CYAN}👤 Enter your name: {RESET}").strip().replace(" ", "_")
    filepath = os.path.join("results", dept_choice.lower(), username, f"exam_results_{username}.txt")

    if not os.path.isfile(filepath):
        colour_print("❌ No results found for this user.", RED)
        return

    with open(filepath, "r", encoding="utf-8") as f:
        print(f"\n{CYAN}📁 Exam Results for {username}:{RESET}\n")
        print(f.read())

# ---------- Load Exam ----------
def load_question():
    username = input(f"\n{CYAN}👤 Enter your name: {RESET}").strip().replace(" ", "_")
    dept_choice = input(f"\n{CYAN}📚 Choose Department (Science/Commercial/Art): {RESET}").strip().upper()
    if dept_choice not in departments:
        colour_print("❌ Invalid department.", RED)
        return

    subjects = departments[dept_choice]["subjects"]
    exam_duration = departments[dept_choice]["duration"]

    timer_thread = threading.Thread(target=countdown_timer, args=(exam_duration,), daemon=True)
    timer_thread.start()

    overall_results, total_qs, total_correct = {}, 0, 0

    for _, (fname, subj_name) in subjects.items():
        ans, score, qcount = run_exam(fname, subj_name)
        overall_results[subj_name] = {"attempted": len(ans), "correct": score, "total": qcount}
        total_qs += qcount
        total_correct += score

    stop_timer()
    save_results(username, overall_results, total_correct, total_qs, dept_choice)

# ---------- Menu ----------
def main_menu():
    while True:
        line()
        colour_print("🎓 Welcome to the Exam Simulator!", GREEN)
        print("1. Take Exam")
        print("2. Check Result")
        print("3. Exit")
        choice = input("\n👉 Enter choice: ").strip()

        if choice == "1":
            Load_instructions()
            load_question()
        elif choice == "2":
            check_results()
        elif choice == "3":
            colour_print("🙏 Thank you for using the Exam Simulator. Goodbye!", BLUE)
            break
        else:
            colour_print("❌ Invalid choice.", RED)

# ---------- Run ----------
main_menu()
