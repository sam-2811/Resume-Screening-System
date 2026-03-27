# PROJECT REPORT
## Resume Screening System — CLI-Based AI Tool for Resume Evaluation

---

**Course:** CSA2001 — Artificial Intelligence  
**Semester:** Second Semester  
**Name:** Saumya Agarwal   
**Registration No:** 25BCE10298   
**Faculty:** J. Subash Chandra Bose   

---

## TABLE OF CONTENTS

1. [Title](#1-title)
2. [Introduction](#2-introduction)
3. [Motivation of the Project](#3-motivation-of-the-project)
4. [Problem Statement](#4-problem-statement)
5. [Objective of the Project](#5-objective-of-the-project)
6. [Methodology / Approach](#6-methodology--approach)
7. [System Architecture](#7-system-architecture)
8. [Implementation Details](#8-implementation-details)
9. [Key Decisions and Design Choices](#9-key-decisions-and-design-choices)
10. [Challenges Faced](#10-challenges-faced)
11. [Results and Output](#11-results-and-output)
12. [Constraints of the Project](#12-constraints-of-the-project)
13. [Future Enhancements](#13-future-enhancements)
14. [Conclusion](#14-conclusion)
15. [References](#15-references)

---

## 1. TITLE

**Resume Screening System — A CLI-Based AI Tool for Automated Resume Evaluation Using NLP and Keyword Matching**

---

## 2. INTRODUCTION

The Resume Screening System is a terminal-based application developed in Python that assists job seekers in evaluating how well their resume aligns with the requirements of a specific job role. The system leverages fundamental concepts from Natural Language Processing (NLP) and Artificial Intelligence (AI) — specifically text preprocessing, tokenization, n-gram generation, and keyword-based pattern matching — to analyze resume content against predefined skill sets.

In today's competitive job market, applicants often apply for multiple roles without tailoring their resumes to each position's requirements. This tool bridges that gap by providing an automated, instant assessment with actionable feedback — all within the terminal, without requiring any internet connection, API calls, or advanced machine learning models.

The project is designed as a Bring Your Own Project (BYOP) submission for the CSA2001 Artificial Intelligence course, demonstrating practical application of course concepts in a real-world scenario.

---

## 3. MOTIVATION OF THE PROJECT

The motivation behind this project stems from several real-world observations:

1. **Resume-Job Mismatch**: Many candidates submit generic resumes for all job applications. They often fail to include relevant technical keywords that Applicant Tracking Systems (ATS) and human recruiters look for.

2. **Lack of Self-Assessment Tools**: While there are online resume screening tools, most require internet access, account creation, or paid subscriptions. A simple, offline, terminal-based tool fills this gap.

3. **Course Application**: The CSA2001 course covers foundational AI concepts including knowledge representation, search, NLP fundamentals, and intelligent agents. This project applies several of these concepts in a practical, useful manner:
   - **Knowledge Representation**: Job roles and their requirements stored as structured JSON data
   - **NLP Techniques**: Text preprocessing, tokenization, and pattern matching
   - **Intelligent Agent Behavior**: The system acts as an intelligent agent that perceives (reads resume), reasons (matches skills), and acts (provides score and suggestions)

4. **Accessibility**: By keeping the tool fully CLI-based with zero external dependencies, it can run on any machine with Python installed — making it accessible to all students.

---

## 4. PROBLEM STATEMENT

Job seekers, particularly students and fresh graduates, often lack a quick and reliable way to assess whether their resume is adequately tailored for a specific job role. They may:

- Miss including critical technical skills expected for the role
- Not know which skills are most important for their target position
- Struggle to get feedback without applying to actual jobs

**The problem**: How can we build a simple, offline tool that automatically evaluates a resume against the skill requirements of a target job role and provides actionable improvement feedback?

---

## 5. OBJECTIVE OF THE PROJECT

The primary objectives of this project are:

1. **Build a CLI application** that accepts resume text input (via paste or file upload) and evaluates it against a selected job role.

2. **Implement NLP preprocessing** techniques including text cleaning (lowercasing, punctuation removal), tokenization, and n-gram generation.

3. **Develop a keyword matching algorithm** that compares resume content against predefined required skills and experience keywords for each job role.

4. **Calculate a match score** using the formula:  
   `Score = (Matched Skills / Total Required Skills) × 100`

5. **Provide detailed feedback** including matched skills, missing skills, grade, visual progress bar, and personalized suggestions for improvement.

6. **Maintain analysis history** for tracking progress over time.

7. **Ensure the tool is beginner-friendly**, well-documented, modular, and runs entirely in the terminal without external dependencies.

---

## 6. METHODOLOGY / APPROACH

The system follows a structured pipeline for resume screening:

### 6.1 Data Collection & Preparation
- Created a comprehensive `roles.json` file containing 8 popular job roles
- Each role includes: description, required skills (25-29 per role), and experience keywords (9-11 per role)
- Skills are curated based on industry job descriptions and requirements

### 6.2 Text Preprocessing (NLP)
When a resume is submitted, the following preprocessing steps are applied:

| Step | Technique | Purpose |
|------|-----------|---------|
| 1 | Lowercasing | Case-insensitive matching |
| 2 | Punctuation Removal | Remove noise characters |
| 3 | Whitespace Normalization | Collapse multiple spaces |
| 4 | Tokenization | Split text into individual words |
| 5 | N-gram Generation | Create bigrams/trigrams for multi-word skills |

### 6.3 Skill Matching Algorithm
```
INPUT:  cleaned resume text, required skills list
OUTPUT: matched skills, missing skills

1. Generate token set from resume (unigrams)
2. Generate bigram set from resume
3. Generate trigram set from resume
4. Combine all into a unified text element set
5. For each required skill:
   a. If skill exists in the unified set → MATCHED
   b. If skill is a substring of cleaned text → MATCHED
   c. Else → MISSING
6. Return matched and missing skill lists
```

### 6.4 Scoring Algorithm
```
Skill Score      = (|matched_skills| / |required_skills|) × 100
Experience Bonus = (|matched_exp_keywords| / |total_exp_keywords|) × 10
Final Score      = min(Skill Score + Experience Bonus, 100)
```

### 6.5 Grading & Feedback
- Scores are mapped to grades (Excellent/Good/Average/Needs Improvement)
- Missing skills are used to generate personalized improvement suggestions
- All results are displayed in a formatted terminal report

---

## 7. SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    RESUME SCREENING SYSTEM                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │  INPUT    │    │  PROCESSING  │    │     OUTPUT       │   │
│  │          │    │              │    │                  │   │
│  │ • Paste  │───▶│ • Clean Text │───▶│ • Match Score    │   │
│  │ • File   │    │ • Tokenize   │    │ • Grade          │   │
│  │ • Role   │    │ • N-grams    │    │ • Matched Skills │   │
│  │  Select  │    │ • Match      │    │ • Missing Skills │   │
│  │          │    │ • Score      │    │ • Suggestions    │   │
│  └──────────┘    └──────────────┘    └──────────────────┘   │
│                         │                      │             │
│                    ┌────▼────┐            ┌────▼────┐       │
│                    │roles.json│           │ history  │       │
│                    │(Database)│           │ (JSON)   │       │
│                    └─────────┘            └─────────┘       │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  main.py          │  utils.py           │  roles.json       │
│  (CLI Interface)  │  (Core Logic)       │  (Data Store)     │
└─────────────────────────────────────────────────────────────┘
```

### Module Breakdown

| Module | Responsibility |
|--------|---------------|
| `main.py` | CLI menu loop, user input handling, workflow orchestration |
| `utils.py` | Text processing, skill matching, scoring, display formatting, file I/O |
| `roles.json` | Job role definitions with required skills and experience keywords |
| `data/` | Storage for sample resumes and analysis history |

---

## 8. IMPLEMENTATION DETAILS

### 8.1 Technology Stack
- **Language**: Python 3.7+
- **Libraries**: Standard library only (`json`, `os`, `string`, `datetime`, `sys`)
- **Data Format**: JSON for role definitions and analysis history
- **Interface**: Command-line interface (CLI)

### 8.2 Key Functions

| Function | Module | Purpose |
|----------|--------|---------|
| `clean_text()` | utils.py | Preprocesses raw text (lowercase, remove punctuation) |
| `tokenize()` | utils.py | Splits text into word tokens |
| `extract_ngrams()` | utils.py | Generates n-grams for multi-word matching |
| `match_skills()` | utils.py | Core matching algorithm |
| `calculate_score()` | utils.py | Computes percentage score |
| `get_grade()` | utils.py | Maps score to grade label |
| `generate_suggestions()` | utils.py | Creates improvement recommendations |
| `save_analysis()` | utils.py | Persists results to JSON |
| `handle_analyze()` | main.py | Orchestrates the full analysis pipeline |
| `main()` | main.py | Entry point and menu loop |

### 8.3 Code Quality
- **Modular Design**: Functions are small, focused, and reusable
- **Documentation**: Every function has a detailed docstring
- **Error Handling**: Input validation, file not found, empty input, invalid choices
- **Type Hints**: Clear parameter and return type documentation in docstrings
- **Constants**: Configurable thresholds and file paths

---

## 9. KEY DECISIONS AND DESIGN CHOICES

### 9.1 Why CLI Instead of GUI?
- The project constraints require terminal-only operation
- CLI tools are faster to develop and easier to test
- Focus remains on AI/NLP logic rather than UI frameworks
- Universal compatibility across all operating systems

### 9.2 Why JSON for Role Data?
- Human-readable and easy to edit
- No database setup required
- Python's `json` module makes parsing trivial
- Easy for others to add new roles without touching code

### 9.3 Why N-gram Matching?
Simple word-by-word matching fails for multi-word skills like:
- "machine learning" (2 words)
- "power bi" (2 words)  
- "react native" (2 words)

By generating bigrams and trigrams, the system correctly identifies these compound skills.

### 9.4 Why Experience Bonus?
A resume that mentions experience-related terms (e.g., "deployment", "code review") demonstrates practical knowledge beyond just listing skills. The 10% bonus rewards this without overshadowing technical skill matching.

---

## 10. CHALLENGES FACED

| Challenge | Solution |
|-----------|----------|
| Multi-word skill matching (e.g., "machine learning") | Implemented n-gram generation (bigrams, trigrams) alongside unigram matching |
| Handling varied resume formats | Aggressive text cleaning normalizes all input formats |
| Balancing skill lists (not too specific, not too generic) | Curated 25-29 skills per role based on real job descriptions |
| User experience in CLI | Used Unicode box-drawing characters and emojis for visual appeal |
| Avoiding false positives (e.g., "react" matching "reactive") | Used exact token matching from sets, not substring matching on individual words |
| Persisting analysis history | JSON-based append-only history file in the data directory |

---

## 11. RESULTS AND OUTPUT

### Test Case: Sample Resume vs. Web Developer Role

**Input**: A sample resume for a full-stack developer with skills in JavaScript, React, Node.js, Python, MongoDB, etc.

**Output**:
- **Score**: ~72.5% (Good Match)  
- **Matched**: 18 out of 28 required skills
- **Missing**: 10 skills (angular, flask, jquery, php, rest, sass, ui, ux, vue, webpack)
- **Suggestions**: Add key missing skills, consider relevant certifications

### Test Case: Same Resume vs. Data Analyst Role

**Output**:
- **Score**: ~25% (Needs Improvement)
- **Matched**: 7 out of 28 skills (python, sql, mongodb, mysql, postgresql, database, numpy mentioned elsewhere)
- **Missing**: 21 skills
- **Suggestions**: Significant resume updates needed, take data analysis courses

These results demonstrate the system's ability to differentiate resume fitness across different roles.

---

## 12. CONSTRAINTS OF THE PROJECT

1. **No Advanced ML Models**: The system uses keyword matching, not semantic understanding. It cannot understand context (e.g., "I built a machine learning pipeline" vs. listing "machine learning" as a skill).

2. **No APIs**: The tool operates fully offline with no internet dependency.

3. **Text Input Only**: Resumes must be in plain text format (.txt). PDF/DOCX parsing is not supported.

4. **Predefined Roles Only**: Job roles are limited to those defined in `roles.json`. Custom roles require manual JSON editing.

5. **English Only**: The system processes English-language resumes only.

6. **No Semantic Similarity**: Skills must match exactly (after cleaning). "JS" won't match "JavaScript", and "ML" won't match "Machine Learning".

---

## 13. FUTURE ENHANCEMENTS

1. **PDF Resume Parsing**: Add support for `.pdf` and `.docx` file formats using libraries like `PyPDF2` or `python-docx`.

2. **Synonym Matching**: Map common abbreviations and synonyms (e.g., "JS" → "JavaScript", "ML" → "Machine Learning").

3. **TF-IDF Scoring**: Implement Term Frequency-Inverse Document Frequency for weighted skill importance.

4. **Web Interface**: Build a Flask/Streamlit web front-end for easier access.

5. **Resume Comparison**: Compare multiple resumes against the same role to rank candidates.

6. **Custom Role Creation**: Allow users to define custom roles and skills through the CLI.

7. **Database Integration**: Use SQLite for persistent storage of resumes and analysis results.

8. **Skill Categorization**: Group skills into categories (programming languages, frameworks, tools) for more nuanced scoring.

9. **Export Reports**: Generate PDF or HTML reports of analysis results.

10. **Cosine Similarity**: Implement vector-based similarity for more nuanced matching.

---

## 14. CONCLUSION

The Resume Screening System successfully demonstrates how fundamental AI and NLP concepts can be applied to solve a real-world problem. By combining text preprocessing, tokenization, n-gram analysis, and keyword matching, the tool provides meaningful resume evaluations without requiring complex machine learning models or external services.

The project achieves all its stated objectives:
- ✅ Functional CLI application with intuitive menu system
- ✅ NLP preprocessing pipeline for resume text
- ✅ Keyword matching algorithm with n-gram support
- ✅ Percentage-based scoring with clear grading scale
- ✅ Detailed feedback with actionable suggestions
- ✅ Persistent analysis history
- ✅ Clean, modular, well-documented code
- ✅ Zero external dependencies

The system, while simple in its AI approach, provides genuine utility for students and job seekers who want quick feedback on their resume's alignment with target roles. It serves as a practical demonstration that effective AI tools don't always require deep learning — sometimes, well-applied fundamentals are enough.

---

## 15. REFERENCES

1. Bird, S., Klein, E., & Loper, E. (2009). *Natural Language Processing with Python*. O'Reilly Media.
2. Jurafsky, D., & Martin, J.H. (2023). *Speech and Language Processing* (3rd ed.). Stanford University.
3. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
4. Python Software Foundation. (2024). *Python 3 Documentation*. https://docs.python.org/3/
5. Manning, C.D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
6. Indeed.com — Job description skill requirements reference
7. LinkedIn Job Listings — Industry skill set benchmarking

---

*This report is submitted as part of the BYOP (Bring Your Own Project) requirement for CSA2001 — Artificial Intelligence.*
