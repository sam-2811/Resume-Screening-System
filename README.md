# 📄 Resume Screening System

> A CLI-based AI-powered resume screening tool that evaluates resumes against predefined job role requirements using NLP techniques (tokenization, keyword matching) and simple scoring logic.

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)](https://python.org)
[![Course](https://img.shields.io/badge/Course-CSA2001-orange)](https://vitap.ac.in)

---

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [How to Set Up & Run](#how-to-set-up--run)
- [How to Use](#how-to-use)
- [Sample Input / Output](#sample-input--output)
- [Scoring Logic](#scoring-logic)
- [Available Job Roles](#available-job-roles)
- [Contributing](#contributing)

---

## 🧠 About the Project

### Problem Statement
Job seekers often struggle to assess how well their resume matches a target job role. Manually comparing skills against job descriptions is tedious and error-prone.

### Solution
This **Resume Screening System** provides an automated, terminal-based tool that:
- Accepts resume text (paste or file upload)
- Compares it against predefined skill sets for popular job roles
- Uses **NLP preprocessing** (tokenization, text cleaning) and **keyword matching**
- Produces a **match score (0–100%)**, lists matched/missing skills, and provides **actionable suggestions**

### AI/NLP Concepts Used
| Concept | Application |
|---------|------------|
| **Text Preprocessing** | Lowercasing, punctuation removal, whitespace normalization |
| **Tokenization** | Splitting text into individual word tokens |
| **N-gram Generation** | Creating bigrams/trigrams for multi-word skill matching |
| **Keyword Matching** | Comparing tokens against predefined skill dictionaries |
| **Scoring Algorithm** | Calculating percentage match based on skill overlap |

---

## ✨ Features

- ✅ **Paste or Upload Resume** — Enter text directly or load from `.txt` file
- ✅ **8 Job Roles** — Web Developer, Data Analyst, Software Engineer, ML Engineer, Cybersecurity Analyst, Mobile App Developer, DevOps Engineer, UI/UX Designer
- ✅ **Smart Matching** — Handles multi-word skills (e.g., "machine learning", "power bi")
- ✅ **Detailed Reports** — Score, grade, progress bar, matched/missing skills
- ✅ **Actionable Suggestions** — Personalized tips to improve your resume
- ✅ **Analysis History** — All past analyses saved automatically
- ✅ **Experience Bonus** — Extra points for relevant experience keywords
- ✅ **Beautiful CLI** — Color-coded output with Unicode formatting

---

## 📂 Project Structure

```
resume-screening-system/
├── main.py              # Main CLI application (entry point)
├── utils.py             # Helper functions (text processing, scoring, display)
├── roles.json           # Job roles database (skills & keywords)
├── README.md            # Project documentation
├── data/
│   ├── sample_resume.txt      # Sample resume for testing
│   └── analysis_history.json  # Auto-generated analysis history
└── report/
    └── project_report.md      # Project report document
```

---

## 🔧 Prerequisites

- **Python 3.7 or higher** (no external packages required!)
- A terminal / command prompt

Verify Python is installed:
```bash
python --version
```

> **Note:** This project uses only Python standard library modules (`json`, `os`, `string`, `datetime`, `sys`). No `pip install` needed!

---

## 🚀 How to Set Up & Run

### Step 1: Clone the Repository
```bash
git clone https://github.com/sam-2811/Resume-Screening-System
cd Resume-Screening-System
```

### Step 2: Run the Application
```bash
python main.py
```

That's it! The application will start in your terminal.

---

## 📖 How to Use

### Step-by-Step Guide

1. **Load your resume** (Option `1` or `2`)
   - Option `1`: Paste resume text directly into the terminal
   - Option `2`: Load from a `.txt` file (e.g., `data/sample_resume.txt`)

2. **Select a job role** (Option `3`)
   - Choose from 8 available roles by entering the role number

3. **Analyze** (Option `4`)
   - The system will process your resume and display:
     - Match score percentage
     - Grade (Excellent/Good/Average/Needs Improvement)
     - Visual progress bar
     - List of matched and missing skills
     - Personalized improvement suggestions

4. **View history** (Option `5`)
   - See all past analysis results

5. **Exit** (Option `0`)

---

## 📊 Sample Input / Output

### Sample Input
Using the provided sample resume (`data/sample_resume.txt`) with the **Web Developer** role:

```
  Enter your choice: 2
  File path: data/sample_resume.txt
  ✅  Resume loaded from: data/sample_resume.txt

  Enter your choice: 3
  [Select: 1 - Web Developer]
  ✅  Selected role: Web Developer

  Enter your choice: 4
```

### Sample Output
```
  ══════════════════════════════════════════════════════════════

  📊  RESUME ANALYSIS REPORT
  ────────────────────────────────────────

  🎯  Target Role   : Web Developer
  📈  Match Score   : 72.5%
  🏆  Grade         : Good Match
  ⭐  Rating        : ★★★★☆

  Progress: [██████████████░░░░░░] 72.5%

  ✅  MATCHED SKILLS (18/28):
      • api   • aws   • bootstrap
      • css   • django   • docker
      • figma   • git   • graphql
      • html   • javascript   • mongodb
      • nodejs   • python   • react
      • responsive   • sql   • typescript

  ❌  MISSING SKILLS (10):
      • angular   • flask   • jquery
      • php   • rest   • sass
      • ui   • ux   • vue
      • webpack

  💡  SUGGESTIONS:
      1. Add these key skills to your resume: angular, flask, jquery, php, rest
      2. Consider also adding 5 more relevant skills.
      3. You're close! A few more skills and targeted experience
         will make your resume much stronger.

  ══════════════════════════════════════════════════════════════
```

---

## 🧮 Scoring Logic

### Formula
```
Skill Score = (Matched Skills / Total Required Skills) × 100
Experience Bonus = (Matched Exp Keywords / Total Exp Keywords) × 10
Final Score = min(Skill Score + Experience Bonus, 100)
```

### Grading Scale

| Score Range | Grade | Rating |
|:-----------:|:-----:|:------:|
| 80–100% | Excellent Match | ★★★★★ |
| 60–79% | Good Match | ★★★★☆ |
| 40–59% | Average Match | ★★★☆☆ |
| 0–39% | Needs Improvement | ★★☆☆☆ |

---

## 🎯 Available Job Roles

| # | Role | Skills Count |
|---|------|:------------:|
| 1 | Web Developer | 28 |
| 2 | Data Analyst | 28 |
| 3 | Software Engineer | 29 |
| 4 | Machine Learning Engineer | 27 |
| 5 | Cybersecurity Analyst | 28 |
| 6 | Mobile App Developer | 27 |
| 7 | DevOps Engineer | 26 |
| 8 | UI/UX Designer | 26 |

---

## 🛠️ Technical Details

### NLP Techniques Used
- **Text Cleaning**: Lowercasing, punctuation removal
- **Tokenization**: Whitespace-based word splitting
- **N-gram Generation**: Bigrams and trigrams for multi-word skill detection
- **Keyword Matching**: Set-based intersection for O(1) lookup performance

### Key Design Decisions
- **No external dependencies**: Runs with Python standard library only
- **Modular architecture**: Separate `utils.py` for reusability
- **JSON-based roles**: Easy to add/modify job roles without code changes
- **Persistent history**: Analysis results saved for future reference

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-role`)
3. Add your changes
4. Commit (`git commit -m 'Add new job role'`)
5. Push (`git push origin feature/new-role`)
6. Open a Pull Request

### Adding a New Job Role
Simply add an entry to `roles.json`:
```json
{
    "New Role Name": {
        "description": "Role description here",
        "required_skills": ["skill1", "skill2", "skill3"],
        "experience_keywords": ["keyword1", "keyword2"]
    }
}
```

---


## 👤 Author

- **Name**: [Your Name]
- **Registration No**: [Your Reg No]
- **Course**: CSA2001 — Artificial Intelligence
- **University**: VIT AP University

---

> Built a BYOP (Bring Your Own Project) submission for CSA2001.
