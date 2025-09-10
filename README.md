# 📝 Exam Simulator

A Python-based **Exam Simulator** that allows students to take subject-based exams under timed conditions. Supports multiple departments (Science, Art, Commercial), each with their own subjects and question sets.

---

## 📂 Features
- Multiple **departments**: Science, Art, Commercial  
- Each department has **4 subjects** with questions loaded from `.txt` files  
- **Randomized** 25 questions per subject attempt  
- Navigation support (`NEXT`, `BACK`, `EXIT`)  
- **Timer per department** (e.g., Science = 2 hours for 4 subjects)  
- **Results saved** automatically under the student’s name  

---

## ⚡ Requirements
- Python **3.8+**  
- No external libraries required (all modules are built-in: `random`, `time`, `datetime`, `threading`)  

Optional (for prettier cross-platform colors):  
```txt
colorama>=0.4.6
```

---

## ⚙️ Setup & Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/exam-simulator.git
   cd exam-simulator
   ```

2. Ensure Python 3.8+ is installed:
   ```bash
   python --version
   ```

3. Run the exam simulator:
   ```bash
   python exam_simulator.py
   ```

---

## 📁 Project Structure
```
exam-simulator/
│── exam_simulator.py      # Main program
│── requirements.txt       # Dependencies (optional)
│── README.md              # Documentation
│── questions/
│   ├── chemistry_questions.txt
│   ├── physics.txt
│   ├── mathematics.txt
│   ├── biology.txt
│   ├── crs.txt
│   ├── government.txt
│   ├── literature.txt
│   ├── english.txt
│   ├── account.txt
│   ├── economics.txt
│   └── commerce.txt
│── results/
│   └── <username>_results.txt
```

---

## 📊 Example Result
After finishing an exam, results are saved in the `results/` folder under the student’s name:  

```
RESULT SUMMARY for JohnDoe
Date: 2025-09-08 15:40:22
Department: SCIENCE

Chemistry: 18/25 (72.00%)
Physics: 20/25 (80.00%)
Biology: 15/25 (60.00%)
Mathematics: 21/25 (84.00%)

TOTAL SCORE: 74/100 (74.00%)
```

---

## 👨‍💻 Author
Developed by **Udom Blessing**
