# 🎓 Exam Simulator

A Python-based Exam Simulator CLI application with student registration, login, exam timer, PDF slip generation, and email notifications.

---

## ✨ Features
- 🔑 **User Registration & Login**
  - Auto-generates unique **Username** & **Registration Number**
  - Validates **email** and enforces strong **passwords**
  - Stores account details securely (hashed passwords)

- 📄 **Registration Slip**
  - Generates a styled PDF slip with student details
  - Includes optional **logo branding**
  - Automatically emailed to the student after registration

- ⏳ **Exam Functionality**
  - Department-based exam durations (`SCIENCE`, `ART`, `COMMERCIAL`)
  - Countdown timer runs in the background
  - Questions are loaded once the exam starts

- 📊 **Result Management**
  - Check saved results after finishing the exam
  - Organized by department and username folders

- 🛠 **Account Management**
  - Change student name after registration
  - Prevents duplicate usernames, emails, or registration numbers

---

## 📂 Project Structure
.
├── results/ # Stores exam results
├── users/ # Stores user accounts
├── logo.png # Logo for registration PDF (optional)
├── main.py # Main program entry point
├── utils.py # Helper functions (validation, PDF, email, etc.)
├── requirements.txt # Python dependencies
└── README.md # Project documentation


---

## 🚀 Getting Started

### 1. Clone Repository
```bash
git clone https://github.com/your-username/exam-simulator.git
cd exam-simulator
```

### 2. Install Dependecies
Make sure you have Python 3.9+ installed.
Install required libraries:
``` bash 
pip install -r requirements.txt
```

### 3. Configure Email

Edit your email settings inside utils.py:
```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"
```

### 4. Run the App
``` bash
python main.py
```

---

# #🎮 Usage
**When the app starts, you’ll see the main menu:**
1. Register
2. Login
3. Exit

--

**After logging in:**
--- Logged In Menu ---
1. Take Exam
2. Check Result
3. Change Name
4. Logout



- Take Exam → Starts countdown timer & loads questions

- Check Result → View your past exam results

- Change Name → Edit your registered name

- Logout → Return to main menu

---

## 📸 Sample Registration Slip (PDF)

The system generates a Registration Slip like this:

Name: John Doe
Username: 2025245JD
Reg.No: 20251156789AB
Department: SCIENCE
Age: 17
Email: john.doe@exa

---

## 👨‍💻 Author


Udom Blessing is a seasoned Developer with focus on backend engineering.... You can look him up or contact him via [Github](https://github.com/BIGUDOM) or [Instagram](https://www.instagram.com/udomblessing481?igsh=dnUxNjE2dThrZGk3&utm_source=qr)


In order to contribute or to report any bug, kindly open a descriptive issue about the bug or contribution.

Adding an example of the bug or the intended feature or fix, is a good way to create an issue.

## License
MIT


<!-- 📘 Exam Simulator

An interactive Python-based exam system that allows students to take exams by department, get timed tests, save results, and check them later.

✨ Features

🎓 Department-based exams (Science, Art, Commercial)

⏳ Countdown timer visible during the exam

🎲 Shuffled questions & options each time

✅ Correct/Incorrect feedback after each question

📁 Results saved automatically in structured folders:

results/
    ├── science/
    │     └── John/
    │          └── exam_results_John.txt
    ├── art/
    └── commercial/


📜 Check results later through the menu

📌 Supports multiple attempts (results are appended in the same file)

🛠️ Requirements

Python 3.8+

No external libraries required (uses only built-in modules).

🚀 How to Run

1. Clone or download the project folder.
```bash
   git clone https://github.com/BIGUDOM/exam-simulator.git
   cd exam-simulator 
```

2. Place your question files in the questions/ directory.

3. Update the file paths inside exam.py if needed.

4. Run the program:
``` bash
   python exam.py
 ```


📖 Usage

When you start the program, you’ll see a menu:

🎓 Welcome to the Exam Simulator!
1. Take Exam
2. Check Result
3. Exit

🔹 Taking an Exam

Enter your name and select a department (Science/Art/Commercial).

Answer each question by typing A/B/C/D/E.

Commands during the exam:

NEXT → skip to the next question

BACK → go to the previous question

EXIT → end the exam early

🔹 Checking Results

Select 2 from the menu.

Enter your department and name to view saved results.

📂 Project Structure
exam-project/
│
├── exam.py              # Main program
├── questions/           # Question files
│   ├── chemistry_questions.txt
│   ├── physics.txt
│   ├── maths.txt
│   ├── biology.txt
│   ├── crs.txt
│   ├── government.txt
│   ├── literature.txt
│   ├── english.txt
│   ├── account.txt
│   ├── economics.txt
│   └── commerce.txt
└── results/             # Results saved here after running

📝 Sample Question File

Below is an example chemistry_questions.txt you can use for testing:

questions|options*|answer
What is H2O?|A. Hydrogen|B. Oxygen|C. Water|D. Salt|C
What is the chemical symbol for Oxygen?|A. O2|B. O|C. Ox|D. Oy|B
Which gas do plants absorb during photosynthesis?|A. Carbon Dioxide|B. Oxygen|C. Nitrogen|D. Hydrogen|A
What is the atomic number of Carbon?|A. 6|B. 8|C. 12|D. 4|A
Which of these is a noble gas?|A. Helium|B. Nitrogen|C. Hydrogen|D. Oxygen|A


📌 Explanation of format:

First line must always be:

questions|options*|answer


Each question is in the format:

Question?|Option1|Option2|Option3|Option4|CorrectOptionLetter


Options must be labeled A, B, C, D, E in order.

📅 Example Result File
============================================================
📅 Date: 2025-09-11 14:23:45
👤 Student: John

Chemistry      : 20/25 (80.00%)
Physics        : 18/25 (72.00%)
Biology        : 21/25 (84.00%)
Mathematics    : 22/25 (88.00%)

TOTAL SCORE: 81/100 (81.00%)
============================================================

👨‍💻 Author

Built with ❤️ by Udom Blessing. -->
