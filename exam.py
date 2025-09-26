import random
import threading
import time
from datetime import datetime
import os
import re
import json
import hashlib
import string
from getpass import getpass
from colorama import Fore, Style, init
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
import traceback
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image


init(autoreset=True)

# ---------- ANSI Colours ----------
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
CYAN = Fore.CYAN
MAGENTA = Fore.MAGENTA
RESET = Fore.RESET
BOLD = Style.BRIGHT

# ---------- Helper Printing ----------
def colour_print(text: str, effect: str) -> None:
    print(f"{effect}{text}{RESET}")

def line():
    print(f"{MAGENTA}{'*' * 80}{RESET}")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    banner = r"""
██████╗ ██╗ ██████╗ ██╗   ██╗██████╗  ██████╗ ███╗   ███╗
██╔══██╗██║██╔═══██╗██║   ██║██╔══██╗██╔═══██╗████╗ ████║
██████╔╝██║██║   ██║██║   ██║██████╔╝██║   ██║██╔████╔██║
██╔═══╝ ██║██║   ██║██║   ██║██╔═══╝ ██║   ██║██║╚██╔╝██║
██║     ██║╚██████╔╝╚██████╔╝██║     ╚██████╔╝██║ ╚═╝ ██║
╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝      ╚═════╝ ╚═╝     ╚═╝
    """
    color = random.choice([CYAN, GREEN, YELLOW, MAGENTA, RED])
    print(f"{color}{banner}{RESET}")

def get_integers(prompt):
    while True:
        temp = input(prompt)
        if temp.isnumeric():
            return int(temp)
        print(f"{temp} is not a valid number ")

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
chemistry_filename = r'questions/chemistry_questions.txt'
physics_filename   = r'questions/physics.txt'
maths_filename     = r'questions/mathematics.txt'
biology_filename   = r'questions/biology.txt'

crs_filename       = r'questions/crs.txt'
government_filename= r'questions/government.txt'
literature_filename= r'questions/literature.txt'
english_filename   = r'questions/english.txt'

account_filename   = r'questions/account.txt'
economics_filename = r'questions/economics.txt'
commerce_filename  = r'questions/commerce.txt'

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

# ---------- Exam Helpers ----------
def _normalize(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r'^[a-e]\s*[\.\)\-:]*\s*', '', s)
    s = re.sub(r'[^\w\s]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


CONFIG_FILE = "config.json"

def load_config():
    # If config file doesn't exist, create template
    if not os.path.exists(CONFIG_FILE):
        template = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "youremail@gmail.com",     # replace with your email
            "sender_password": "your_app_password"     # replace with your app password
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(template, f, indent=4)
        print(f"{YELLOW}⚠️ config.json created. Fill in your Gmail and app password!{RESET}")

    # Load config safely
    with open(CONFIG_FILE, "r") as f:
        try:
            cfg = json.load(f)
        except json.JSONDecodeError:
            cfg = {}

    # Provide safe defaults
    fixed_cfg = {
        "smtp_server": cfg.get("smtp_server", "smtp.gmail.com"),
        "smtp_port": cfg.get("smtp_port", 587),
        "sender_email": cfg.get("sender_email", "codis1723@gmail.com"),
        "sender_password": cfg.get("sender_password", "hkdzlilwcqbbvmjo")
    }

    if not fixed_cfg["sender_email"] or not fixed_cfg["sender_password"]:
        print(f"{RED}❌ sender_email or sender_password missing in config.json!{RESET}")

    return fixed_cfg


# ======== EMAIL ========
def send_email(recipient, subject, body, html=False, attachments=None):
    try:
        cfg = load_config()
        if not cfg["sender_email"] or not cfg["sender_password"]:
            print(f"{RED}Email not configured properly.{RESET}")
            return

        # Create email message
        msg = MIMEMultipart()
        msg["From"] = cfg["sender_email"]
        msg["To"] = recipient
        msg["Subject"] = subject

        # Attach plain or HTML body
        if html:
            msg.attach(MIMEText(body, "html"))
        else:
            msg.attach(MIMEText(body, "plain"))

        # Attach files if any
        if attachments:
            for path in attachments:
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        part = MIMEApplication(f.read(), Name=os.path.basename(path))
                        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(path)}"'
                        msg.attach(part)

        # Send email
        with smtplib.SMTP(cfg["smtp_server"], cfg["smtp_port"]) as server:
            server.starttls()
            server.login(cfg["sender_email"], cfg["sender_password"])
            server.send_message(msg)

        print(f"{GREEN}✅ Email sent to {recipient}{RESET}")

    except Exception as e:
        print(f"{RED}⚠️ Email failed: {e}{RESET}")
        traceback.print_exc()


def generate_registration_pdf(filepath, user_data, logo_path=None):
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Add logo if provided
    if logo_path and os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=80, height=80)  # adjust size as needed
            elements.append(img)
            elements.append(Spacer(1, 10))
        except Exception as e:
            print(f"⚠️ Could not load logo: {e}")

    # Title
    title = Paragraph(
        "<b><font size=16 color='navy'>Exam Simulator Registration Slip</font></b>",
        styles["Title"]
    )
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Build table data
    table_data = [["Field", "Value"]]
    for key, value in user_data.items():
        table_data.append([key, str(value)])

    # Table with styling
    table = Table(table_data, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(table)

    elements.append(Spacer(1, 30))
    footer = Paragraph(
        "<font size=10 color='grey'><i>This is an auto-generated slip. Keep it safe.</i></font>",
        styles["Normal"]
    )
    elements.append(footer)

    # Build PDF
    doc.build(elements)
    return filepath



def run_exam(input_filename, subject_name, num_questions=25):
    global time_left_str
    with open(input_filename, 'r', encoding="utf-8") as f:
        raw_lines = [ln.rstrip("\n") for ln in f if ln.strip()]

    if raw_lines and any(k in raw_lines[0].lower() for k in ("question", "option", "answer")):
        raw_lines = raw_lines[1:]

    all_qs = [line.split("|") for line in raw_lines]
    questions = [[part.strip() for part in parts] for parts in all_qs if len(parts) >= 3]
    questions = random.sample(questions, min(num_questions, len(questions)))

    answers = {}
    index = 0
    colour_print(f"\n🚀 Starting {subject_name} Exam...", GREEN)

    while 0 <= index < len(questions):
        parts = questions[index]
        q = parts[0]
        options = parts[1:-1]
        raw_correct = parts[-1].strip()

        labels = ['A', 'B', 'C', 'D', 'E'][:len(options)]
        norm_options = [_normalize(opt) for opt in options]
        norm_correct = _normalize(raw_correct)

        correct_label = None
        if raw_correct.upper() in labels:
            correct_label = raw_correct.upper()
        elif norm_correct in norm_options:
            correct_label = labels[norm_options.index(norm_correct)]

        clear_screen()
        line()
        print(f"{CYAN}Subject: {subject_name}{RESET}")
        print(f"{YELLOW}⏳ Time Remaining: {time_left_str}{RESET}")
        print(f"{YELLOW}❓ Q{index+1} of {len(questions)}{RESET}\n{q}\n")
        for lbl, opt in zip(labels, options):
            print(f"{lbl}. {opt}")

        if index in answers:
            colour_print(f"\n📌 Previously selected: {answers[index]}", CYAN)

        raw_input_choice = input(f"\n{CYAN}👉 Enter your choice (A/B/C/D/E or option / NEXT / BACK / EXIT): {RESET}").strip()
        if not raw_input_choice:
            colour_print("⚠️ Please enter something.", RED)
            continue

        cmd = raw_input_choice.upper().strip()

        if cmd == "EXIT":
            colour_print("🔚 Ending Exam...", BLUE)
            break
        elif cmd == "BACK":
            index = max(0, index - 1)
            continue
        elif cmd == "NEXT":
            index += 1
            continue

        chosen_label = None
        if cmd in labels:
            chosen_label = cmd
        else:
            norm_choice = _normalize(raw_input_choice)
            if norm_choice in norm_options:
                chosen_label = labels[norm_options.index(norm_choice)]

        if chosen_label is None:
            colour_print("⚠️ Invalid input.", RED)
            continue

        answers[index] = chosen_label
        if correct_label:
            if chosen_label == correct_label:
                colour_print("✅ Correct!", GREEN)
            else:
                colour_print(f"❌ Incorrect. Correct: {correct_label}", RED)

        index += 1

    score = 0
    for i, parts in enumerate(questions):
        if i not in answers:
            continue
        options = parts[1:-1]
        raw_correct = parts[-1].strip()
        labels = ['A', 'B', 'C', 'D', 'E'][:len(options)]
        norm_options = [_normalize(opt) for opt in options]
        norm_correct = _normalize(raw_correct)

        correct_label = None
        if raw_correct.upper() in labels:
            correct_label = raw_correct.upper()
        elif norm_correct in norm_options:
            correct_label = labels[norm_options.index(norm_correct)]

        if correct_label and answers[i] == correct_label:
            score += 1

    return answers, score, len(questions)

# ---------- Account Helpers ----------
ACCOUNTS_FOLDER = "accounts"
def get_user_folder(username):
    return os.path.join(ACCOUNTS_FOLDER, username)

def get_account_file(username):
    return os.path.join(get_user_folder(username), "account.json")

def pause():
    input(f"\n{YELLOW}Press Enter to continue...{RESET}")

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# ---------- Register ----------
import re
def check_user_exist(username=None, email=None, reg_no=None):
    base_folder = "accounts"  # FIXED (instead of results)

    for user in os.listdir(base_folder):
        user_folder = os.path.join(base_folder, user)
        acc_file = os.path.join(user_folder, "account.json")

        if not os.path.exists(acc_file):
            continue

        try:
            with open(acc_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if username and data.get("Username") == username:
                return True
            if email and data.get("Email") == email:
                return True
            if reg_no and data.get("Reg.No") == reg_no:
                return True

        except Exception as e:
            print(f"{RED}⚠️ Error reading {acc_file}: {e}{RESET}")

    return False



def is_valid_email(email: str) -> bool:
    # Basic email regex pattern
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None

def password_feedback(password: str) -> list:
    """Return feedback on missing requirements."""
    feedback = []
    if len(password) < 8:
        feedback.append("- At least 8 characters long")
    if not re.search(r"[A-Z]", password):
        feedback.append("- At least 1 uppercase letter")
    if not re.search(r"[a-z]", password):
        feedback.append("- At least 1 lowercase letter")
    if not re.search(r"[0-9]", password):
        feedback.append("- At least 1 digit")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        feedback.append("- At least 1 special character (!@#$%^&* etc.)")
    return feedback

def password_strength(password: str) -> tuple:
    """Return (label, bar) for password strength."""
    score = 0
    if len(password) >= 8: score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"[0-9]", password): score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): score += 1

    # Map score to levels
    if score <= 2:
        return (f"{RED}Weak{RESET}", f"{RED}▮▯▯{RESET}")
    elif score == 3 or score == 4:
        return (f"{YELLOW}Medium{RESET}", f"{YELLOW}▮▮▯{RESET}")
    else:
        return (f"{GREEN}Strong{RESET}", f"{GREEN}▮▮▮{RESET}")


def register_portal():
    clear_screen()
    print_banner()
    print(f"{BOLD}--- Register ---{RESET}")

    # ----- Name -----
    first_name = input(f"\n{CYAN}👤 Enter your first name: {RESET}").strip().replace(" ", "_")
    surname = input(f"\n{CYAN}👤 Enter your surname: {RESET}").strip().replace(" ", "_")
    name = f"{first_name} {surname}"

    # ----- Generate unique username -----
    while True:
        username = f"2025245{random.randint(1,1000)}{name[:2]}"
        if not os.path.exists(get_user_folder(username)):
            break
    print(f"Your username is : {username}")

    # ----- Validate email -----
    while True:
        email = input("Email: ").strip()
        if is_valid_email(email):
            break
        else:
            print(f"{RED}⚠️ Invalid email format! Try again.{RESET}")

    # ----- Password validation -----
    while True:
        password = getpass("Password: ").strip()
        confirm = getpass("Confirm Password: ").strip()

        if password != confirm:
            print(f"{RED}⚠️ Passwords do not match! Try again.{RESET}")
            continue

        # Show strength with bar
        label, bar = password_strength(password)
        print(f"🔒 Password strength: {label} {bar}")

        feedback = password_feedback(password)
        if feedback:
            print(f"{YELLOW}Tips to improve your password:{RESET}")
            for f in feedback:
                print(f"  {RED}{f}{RESET}")
            continue
        break

    # ----- Department -----
    dept = input("Enter your department (SCIENCE/ART/COMMERCIAL): ").strip().upper()

    # ----- DOB + Age -----
    year = get_integers("DOB. Enter year (yyyy): ")
    month = get_integers("DOB. Enter month (mm): ")
    day = get_integers("DOB. Enter day (dd): ")
    dob = f"{day:02d}-{month:02d}-{year}"

    today = datetime.now()
    age = today.year - year - ((today.month, today.day) < (month, day))
    if age < 15:
        print(f"{RED}⚠️ You are not eligible for the exam.\n Try again in {15 - age} years!{RESET}")
        pause()
        return

    # ----- Generate Reg.No -----
    reg_number = f"20251156789{random.randint(10,100)}{generate_random_string(2)}"

    # ----- Check duplicates (NOW safe) -----
    if check_user_exist(username=username):
        print(f"{RED}❌ Username already exists! Choose another.{RESET}")
        return
    if check_user_exist(email=email):
        print(f"{RED}❌ Email already registered!{RESET}")
        return
    if check_user_exist(reg_no=reg_number):
        print(f"{RED}❌ Reg.No already in system!{RESET}")
        return

    # ----- Save user -----
    os.makedirs(get_user_folder(username), exist_ok=True)
    acc_file = get_account_file(username)

    users = {
        "Date": datetime.now().isoformat(),
        "Reg.No": reg_number,
        "Name": name,
        "Username": username,
        "Department": dept,
        "Age": age,
        "DOB": dob,
        "Email": email,
        "Password": hashlib.sha256(password.encode()).hexdigest()
    }

    with open(acc_file, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

    print(f"{GREEN}✅ Registration successful!{RESET}")

    # ----- Build user data for PDF & Email -----
    user_data = {
        "Reg.No": reg_number,
        "Name": name,
        "Username": username,
        "Department": dept,
        "Age": age,
        "Email": email,
        "DOB": dob
    }

    welcome_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px;">
                <h2 style="color: #2c3e50;">🎉 Welcome to Exam Simulator, {name}!</h2>
                <p>Your account has been created successfully. Here are your details:</p>
                <ul>
                    <li><b>Username:</b> {username}</li>
                    <li><b>Reg.No:</b> {reg_number}</li>
                    <li><b>Department:</b> {dept}</li>
                </ul>
                <p style="margin-top: 20px;">A copy of your <b>Registration Slip</b> is attached as PDF 📎</p>
                <p>Good luck with your exams 🚀</p>
                <hr>
                <p style="font-size: 12px; color: #888;">This is an automated message, please do not reply.</p>
                </div>
            </body>
        </html>
    """

    pdf_path = os.path.join(get_user_folder(username), "registration_slip.pdf")
    logo_path = "logo.png"

    generate_registration_pdf(pdf_path, user_data, logo_path)

    send_email(
        email,
        "Exam Simulator - Registration Successful",
        welcome_html,
        html=True,
        attachments=[pdf_path]
    )

    pause()



# ---------- Login ----------
def login_portal():
    clear_screen()
    print_banner()
    print(f"{BOLD}--- Login ---{RESET}")
    username = input("👤 Enter username: ").strip()
    password = getpass("🔑 Password: ").strip()

    acc_file = get_account_file(username)
    if not os.path.exists(acc_file):
        print(f"{RED}⚠️ No such account. Please register first.{RESET}")
        pause(); return None

    with open(acc_file, "r", encoding="utf-8") as f:
        user_data = json.load(f)

    if user_data["Password"] == hashlib.sha256(password.encode()).hexdigest():
        print(f"{GREEN}✅ Login successful!{RESET}")
        pause()
        return username, user_data
    else:
        print(f"{RED}⚠️ Invalid credentials!{RESET}")
        pause()
        return None

# ---------- Save Results ----------
def save_results(name, username, results, total_score, total_questions, department_choice):
    student_folder = get_user_folder(username)
    os.makedirs(student_folder, exist_ok=True)

    filepath = os.path.join(student_folder, "exam_results.json")

    userresults = {
        "name": name,
        "username": username,
        "department": department_choice,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": (total_score / total_questions * 100 if total_questions else 0),
        "subjects": []
    }

    for subj, result in results.items():
        percent = (result['correct'] / result['total'] * 100 if result['total'] else 0)
        result_str = f"{result['correct']}/{result['total']} ({percent:.2f}%)"
        userresults["subjects"].append({"subject": subj, "result": result_str})

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(userresults, f, indent=2)

# ---------- Check Results ----------
def check_results():
    username = input(f"\n{CYAN}👤 Enter your username: {RESET}").strip()
    filepath = os.path.join(get_user_folder(username), "exam_results.json")

    if not os.path.isfile(filepath):
        colour_print("❌ No results found for this user.", RED)
        return

    with open(filepath, "r", encoding="utf-8") as f:
        re = json.load(f)

    print(f"\n{CYAN}📁 Exam Results for {re['name']} ({re['username']}):{RESET}\n")
    print(f"📅 Date: {re['date']}")
    print(f"🏫 Department: {re['department']}\n")

    for subj in re["subjects"]:
        print(f"{subj['subject']:15} : {subj['result']}")

    print(f"\nTOTAL SCORE: {re['total']:.2f}%\n")

# ---------- Edit Name ----------
def edit_name(username):
    account_file = get_account_file(username)

    if not os.path.exists(account_file):
        print(f"{RED}⚠️ Account not found for {username}.{RESET}")
        return

    with open(account_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    current_name = data.get("Name", "Unknown")
    print(f"Current name on record: {current_name}")

    choice = input("Do you want to change this name? (yes/no): ").strip().lower()
    if choice != "yes":
        print("No changes made.")
        return

    new_name = input("Enter the correct name: ").strip()
    if not new_name:
        print("Invalid name. No changes made.")
        return

    data["Name"] = new_name

    with open(account_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Name successfully updated from '{current_name}' to '{new_name}'.")


def check_user(username):
    filepath = os.path.join(get_user_folder(username), "exam_results.json")
    return os.path.exists(filepath)

# ---------- Load Question ----------
def load_question(username):
    account_file = os.path.join(get_user_folder(username), "account.json")
    if not os.path.exists(account_file):
        colour_print("❌ Account not found. Please register first.", RED)
        return

    with open(account_file, "r", encoding="utf-8") as f:
        user_data = json.load(f)

    name = user_data.get("Name")
    dept_choice = user_data.get("Department")

    if dept_choice == "SCIENCE":
        subjects = {
            "Mathematics": (maths_filename, "Mathematics"),
            "Physics": (physics_filename, "Physics"),
            "Biology": (biology_filename, "Biology"),
            "Chemistry": (chemistry_filename, "Chemistry"),
        }
    elif dept_choice == "ART":
        subjects = {
            "English": (english_filename, "English"),
            "CRS": (crs_filename, "CRS"),
            "Literature": (literature_filename, "Literature"),
            "Government": (government_filename, "Government"),
        }
    elif dept_choice == "COMMERCIAL":
        subjects = {
            "Mathematics": (maths_filename, "Mathematics"),
            "Economics": (economics_filename, "Economics"),
            "Accounting": (account_filename, "Accounting"),
            "Commerce": (commerce_filename, "Commerce"),
        }
    else:
        colour_print("❌ Invalid department in account file.", RED)
        return

    overall_results = {}
    total_qs, total_correct = 0, 0

    for _, (fname, subj_name) in subjects.items():
        ans, score, qcount = run_exam(fname, subj_name)
        overall_results[subj_name] = {
            "attempted": len(ans),
            "correct": score,
            "total": qcount,
        }
        total_qs += qcount
        total_correct += score

    stop_timer()
    save_results(name, username, overall_results, total_correct, total_qs, dept_choice)


# ---------- Menu ----------
def main_menu():
    while True:
        line()
        print(f"{YELLOW}Current Date: {datetime.now().strftime('%Y-%m-%d')}{RESET}")
        print(f"{YELLOW}Current Time: {datetime.now().strftime('%H:%M:%S')}{RESET}")
        if timer_running:
            colour_print(f"⏳ Timer: {time_left_str}", YELLOW)
        line()
        colour_print("🎓 Welcome to the Exam Simulator!", GREEN)
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        colour_print("Type 'help' for instructions.", CYAN)
        colour_print("Type 'clear' to clear screen ", CYAN)
        line()
        choice = input("\n👉 Enter choice: ").strip()

        if choice == "1":
            register_portal()

        elif choice == "2":
            login_result = login_portal()
            if not login_result:
                continue   # failed login, go back to main menu

            username, user_data = login_result  # unpack tuple

            # Show sub-menu only after successful login
            while True:
                print("\n--- Logged In Menu ---")
                print("1. Take Exam")
                print("2. Check Result")
                print("3. Change Name")
                print("4. Logout")
                sub_choice = input("\n👉 Enter choice: ").strip()

                if sub_choice == "1":
                    dept_choice = user_data.get("Department")
                    duration = departments.get(dept_choice, {}).get("duration", 0)
                    if duration:
                        threading.Thread(
                            target=countdown_timer,
                            args=(duration,),
                            daemon=True
                        ).start()
                    load_question(username)

                elif sub_choice == "2":
                    check_results()

                elif sub_choice == "3":
                    dept_choice = user_data.get("Department")
                    edit_name(username)

                elif sub_choice == "4":
                    colour_print("🔒 Logged out.", BLUE)
                    break

                else:
                    colour_print("❌ Invalid choice.", RED)

        elif choice == "3":
            colour_print("🙏 Thank you for using the Exam Simulator. Goodbye!", BLUE)
            break

        elif choice.lower() == "help":
            Load_instructions()

        elif choice.lower() == "clear":
            clear_screen()

        else:
            colour_print("❌ Invalid choice.", RED)


# ---------- Run ----------
if __name__ == "__main__":
    main_menu()
