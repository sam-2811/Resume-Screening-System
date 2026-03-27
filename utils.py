"""
utils.py - Utility Functions for Resume Screening System
=========================================================
Contains helper functions for text processing, file handling,
score calculation, and display formatting.

Author  : Saumya Agarwal
Course  : CSA2001 - Artificial Intelligence
Project : Resume Screening System (BYOP)
"""

import json
import os
import string
import datetime


# ─────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────

ROLES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "roles.json")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
HISTORY_FILE = os.path.join(DATA_DIR, "analysis_history.json")

# Grading thresholds
GRADE_EXCELLENT = 80
GRADE_GOOD = 60
GRADE_AVERAGE = 40


# ─────────────────────────────────────────────
#  Text Processing Functions
# ─────────────────────────────────────────────

def clean_text(text):
    """
    Preprocesses raw resume text for analysis.
    
    Steps:
        1. Convert to lowercase for case-insensitive matching
        2. Remove punctuation characters
        3. Normalize whitespace
    
    Args:
        text (str): Raw resume text input.
    
    Returns:
        str: Cleaned and normalized text.
    """
    # Step 1: Convert to lowercase
    text = text.lower()
    
    # Step 2: Remove punctuation (keep spaces and alphanumeric)
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)
    
    # Step 3: Normalize whitespace (collapse multiple spaces)
    text = " ".join(text.split())
    
    return text


def tokenize(text):
    """
    Splits cleaned text into individual word tokens.
    
    This is a simple whitespace-based tokenizer suitable
    for keyword matching in resume screening.
    
    Args:
        text (str): Cleaned text string.
    
    Returns:
        list: List of individual word tokens.
    """
    return text.split()


def extract_ngrams(tokens, n=2):
    """
    Generates n-grams (multi-word phrases) from a token list.
    
    This allows matching multi-word skills like "machine learning",
    "power bi", "react native", etc.
    
    Args:
        tokens (list): List of word tokens.
        n (int): Size of n-grams to generate (default: 2).
    
    Returns:
        list: List of n-gram strings.
    """
    ngrams = []
    for i in range(len(tokens) - n + 1):
        ngram = " ".join(tokens[i:i + n])
        ngrams.append(ngram)
    return ngrams


# ─────────────────────────────────────────────
#  Data Loading Functions
# ─────────────────────────────────────────────

def load_roles(filepath=None):
    """
    Loads job role definitions from the JSON file.
    
    Args:
        filepath (str, optional): Path to roles.json file.
                                  Defaults to ROLES_FILE constant.
    
    Returns:
        dict: Dictionary containing job roles and their required skills.
    
    Raises:
        FileNotFoundError: If the roles.json file doesn't exist.
        json.JSONDecodeError: If the JSON is malformed.
    """
    if filepath is None:
        filepath = ROLES_FILE
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            roles = json.load(f)
        return roles
    except FileNotFoundError:
        print(f"\n  [ERROR] Roles file not found: {filepath}")
        print("  Please ensure 'roles.json' exists in the project directory.")
        return {}
    except json.JSONDecodeError as e:
        print(f"\n  [ERROR] Invalid JSON in roles file: {e}")
        return {}


def load_resume_from_file(filepath):
    """
    Reads resume text from a file.
    
    Supports .txt files containing resume content.
    
    Args:
        filepath (str): Path to the resume text file.
    
    Returns:
        str: Contents of the resume file, or empty string on error.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        if not content.strip():
            print("\n  [WARNING] The file is empty.")
            return ""
        
        return content
    except FileNotFoundError:
        print(f"\n  [ERROR] File not found: {filepath}")
        return ""
    except PermissionError:
        print(f"\n  [ERROR] Permission denied: {filepath}")
        return ""
    except UnicodeDecodeError:
        print(f"\n  [ERROR] Unable to read file (encoding issue): {filepath}")
        return ""


# ─────────────────────────────────────────────
#  Skill Matching & Scoring Functions
# ─────────────────────────────────────────────

def match_skills(resume_text, required_skills):
    """
    Matches resume text against a list of required skills.
    
    Uses both single-word and multi-word (n-gram) matching
    to accurately detect skills like "machine learning" or 
    "power bi" in the resume text.
    
    Args:
        resume_text (str): Raw resume text (will be cleaned internally).
        required_skills (list): List of required skill strings.
    
    Returns:
        tuple: (matched_skills, missing_skills) as two sorted lists.
    """
    # Clean and tokenize the resume text
    cleaned = clean_text(resume_text)
    tokens = tokenize(cleaned)
    
    # Generate bigrams and trigrams for multi-word skill matching
    bigrams = extract_ngrams(tokens, 2)
    trigrams = extract_ngrams(tokens, 3)
    
    # Combine all text representations for matching
    all_text_elements = set(tokens) | set(bigrams) | set(trigrams)
    # Also check if skill appears as substring in cleaned text
    
    matched = []
    missing = []
    
    for skill in required_skills:
        skill_lower = skill.lower().strip()
        
        # Check if the skill (single or multi-word) is found
        if skill_lower in all_text_elements or skill_lower in cleaned:
            matched.append(skill)
        else:
            missing.append(skill)
    
    return sorted(matched), sorted(missing)


def calculate_score(matched_count, total_count):
    """
    Calculates the resume match score as a percentage.
    
    Formula: score = (matched_skills / total_required_skills) * 100
    
    Args:
        matched_count (int): Number of skills found in the resume.
        total_count (int): Total number of required skills.
    
    Returns:
        float: Score as a percentage (0.0 to 100.0).
    """
    if total_count == 0:
        return 0.0
    
    score = (matched_count / total_count) * 100
    return round(score, 2)


def get_grade(score):
    """
    Assigns a descriptive grade based on the numeric score.
    
    Grading Scale:
        80-100  → Excellent Match
        60-79   → Good Match
        40-59   → Average Match
        0-39    → Needs Improvement
    
    Args:
        score (float): Numeric score (0-100).
    
    Returns:
        tuple: (grade_label, grade_emoji) for display.
    """
    if score >= GRADE_EXCELLENT:
        return "Excellent Match", "★★★★★"
    elif score >= GRADE_GOOD:
        return "Good Match", "★★★★☆"
    elif score >= GRADE_AVERAGE:
        return "Average Match", "★★★☆☆"
    else:
        return "Needs Improvement", "★★☆☆☆"


def generate_suggestions(missing_skills, role_name):
    """
    Generates actionable suggestions based on missing skills.
    
    Provides personalized feedback to help candidates improve
    their resume for the target role.
    
    Args:
        missing_skills (list): List of skills not found in the resume.
        role_name (str): Name of the target job role.
    
    Returns:
        list: List of suggestion strings.
    """
    suggestions = []
    
    if not missing_skills:
        suggestions.append(f"Your resume is well-aligned with the {role_name} role!")
        suggestions.append("Consider adding specific project examples to stand out.")
        return suggestions
    
    # Suggest adding top missing skills (prioritize first 5)
    top_missing = missing_skills[:5]
    skills_str = ", ".join(top_missing)
    suggestions.append(f"Add these key skills to your resume: {skills_str}")
    
    if len(missing_skills) > 5:
        remaining = len(missing_skills) - 5
        suggestions.append(f"Consider also adding {remaining} more relevant skills.")
    
    # General advice based on number of missing skills
    total_missing = len(missing_skills)
    if total_missing > 15:
        suggestions.append(
            "Your resume needs significant updates for this role. "
            "Consider taking relevant courses or working on projects "
            f"related to {role_name}."
        )
    elif total_missing > 8:
        suggestions.append(
            "Focus on building projects that showcase the missing skills. "
            "Online certifications can also strengthen your profile."
        )
    else:
        suggestions.append(
            "You're close! A few more skills and targeted experience "
            "will make your resume much stronger."
        )
    
    return suggestions


# ─────────────────────────────────────────────
#  Analysis History Functions
# ─────────────────────────────────────────────

def save_analysis(role_name, score, grade, matched, missing):
    """
    Saves the analysis result to a JSON history file.
    
    Creates a timestamped record of each resume analysis
    for future reference.
    
    Args:
        role_name (str): Target job role name.
        score (float): Calculated match score.
        grade (str): Grade label.
        matched (list): Skills that were matched.
        missing (list): Skills that were missing.
    """
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Load existing history or create new
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, IOError):
            history = []
    
    # Create new record
    record = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": role_name,
        "score": score,
        "grade": grade,
        "matched_skills": matched,
        "missing_skills": missing,
        "matched_count": len(matched),
        "total_required": len(matched) + len(missing)
    }
    
    history.append(record)
    
    # Save updated history
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"\n  [WARNING] Could not save analysis history: {e}")


def load_analysis_history():
    """
    Loads past analysis records from the history file.
    
    Returns:
        list: List of past analysis records, or empty list.
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


# ─────────────────────────────────────────────
#  Display / Formatting Functions
# ─────────────────────────────────────────────

def print_header():
    """Prints the application header/banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║            📄  RESUME SCREENING SYSTEM  📄                   ║
║         ─────────────────────────────────────                ║
║          AI-Powered Resume Analysis Tool                     ║
║          Using NLP & Keyword Matching                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """Prints the main menu options."""
    menu = """
┌──────────────────────────────────────┐
│           MAIN MENU                  │
├──────────────────────────────────────┤
│  [1]  Upload / Paste Resume Text     │
│  [2]  Load Resume from File          │
│  [3]  Select Job Role                │
│  [4]  Analyze Resume                 │
│  [5]  View Analysis History          │
│  [6]  View Available Roles           │
│  [7]  Help                           │
│  [0]  Exit                           │
└──────────────────────────────────────┘
    """
    print(menu)


def print_separator(char="─", length=60):
    """Prints a visual separator line."""
    print(f"\n  {char * length}")


def print_score_report(role_name, score, grade, rating, matched, missing, suggestions):
    """
    Prints a formatted analysis report to the terminal.
    
    Args:
        role_name (str): Target job role.
        score (float): Match score percentage.
        grade (str): Grade label.
        rating (str): Star rating string.
        matched (list): Matched skills.
        missing (list): Missing skills.
        suggestions (list): Improvement suggestions.
    """
    print_separator("═")
    print(f"\n  📊  RESUME ANALYSIS REPORT")
    print(f"  {'─' * 40}")
    print(f"\n  🎯  Target Role   : {role_name}")
    print(f"  📈  Match Score   : {score}%")
    print(f"  🏆  Grade         : {grade}")
    print(f"  ⭐  Rating        : {rating}")
    
    # Score bar visualization
    filled = int(score / 5)  # 20 blocks for 100%
    empty = 20 - filled
    bar = "█" * filled + "░" * empty
    print(f"\n  Progress: [{bar}] {score}%")
    
    # Matched Skills
    print(f"\n  ✅  MATCHED SKILLS ({len(matched)}/{len(matched) + len(missing)}):")
    if matched:
        # Display in columns (3 per row)
        for i in range(0, len(matched), 3):
            row = matched[i:i + 3]
            formatted = "   ".join(f"• {s}" for s in row)
            print(f"      {formatted}")
    else:
        print("      No matching skills found.")
    
    # Missing Skills
    print(f"\n  ❌  MISSING SKILLS ({len(missing)}):")
    if missing:
        for i in range(0, len(missing), 3):
            row = missing[i:i + 3]
            formatted = "   ".join(f"• {s}" for s in row)
            print(f"      {formatted}")
    else:
        print("      None — all skills matched!")
    
    # Suggestions
    print(f"\n  💡  SUGGESTIONS:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"      {i}. {suggestion}")
    
    print_separator("═")


def print_roles_list(roles):
    """
    Prints a numbered list of available job roles.
    
    Args:
        roles (dict): Dictionary of job roles.
    """
    print(f"\n  📋  AVAILABLE JOB ROLES:")
    print(f"  {'─' * 40}")
    
    for i, (role_name, role_data) in enumerate(roles.items(), 1):
        skill_count = len(role_data.get("required_skills", []))
        description = role_data.get("description", "No description")
        print(f"\n  [{i}] {role_name}")
        print(f"      {description}")
        print(f"      Required Skills: {skill_count}")


def print_history(history):
    """
    Prints past analysis records in a formatted table.
    
    Args:
        history (list): List of analysis record dictionaries.
    """
    if not history:
        print("\n  No analysis history found.")
        return
    
    print(f"\n  📜  ANALYSIS HISTORY ({len(history)} records)")
    print(f"  {'─' * 58}")
    print(f"  {'#':<4} {'Date & Time':<22} {'Role':<22} {'Score':<8} {'Grade'}")
    print(f"  {'─' * 58}")
    
    for i, record in enumerate(history, 1):
        timestamp = record.get("timestamp", "N/A")
        role = record.get("role", "N/A")
        score = record.get("score", 0)
        grade = record.get("grade", "N/A")
        
        # Truncate role name if too long
        if len(role) > 20:
            role = role[:17] + "..."
        
        print(f"  {i:<4} {timestamp:<22} {role:<22} {score:<8} {grade}")
    
    print(f"  {'─' * 58}")


def print_help():
    """Prints help information for the user."""
    help_text = """
  ╔════════════════════════════════════════════════════════╗
  ║                    HELP GUIDE                         ║
  ╠════════════════════════════════════════════════════════╣
  ║                                                        ║
  ║  HOW TO USE THIS TOOL:                                 ║
  ║                                                        ║
  ║  Step 1: Enter or load your resume text                ║
  ║          → Use Option [1] to paste text directly       ║
  ║          → Use Option [2] to load from a .txt file     ║
  ║                                                        ║
  ║  Step 2: Select a target job role                      ║
  ║          → Use Option [3] to choose from available     ║
  ║            roles (Web Developer, Data Analyst, etc.)   ║
  ║                                                        ║
  ║  Step 3: Analyze your resume                           ║
  ║          → Use Option [4] to run the analysis          ║
  ║          → View your score, matched/missing skills,    ║
  ║            and improvement suggestions                 ║
  ║                                                        ║
  ║  ADDITIONAL OPTIONS:                                   ║
  ║  [5] View past analysis history                        ║
  ║  [6] Browse all available job roles and skills         ║
  ║  [7] Show this help guide                              ║
  ║  [0] Exit the application                              ║
  ║                                                        ║
  ║  SCORING:                                              ║
  ║  Score = (Matched Skills / Total Required) × 100       ║
  ║                                                        ║
  ║  GRADES:                                               ║
  ║  80-100%  → Excellent Match  ★★★★★                    ║
  ║  60-79%   → Good Match       ★★★★☆                    ║
  ║  40-59%   → Average Match    ★★★☆☆                    ║
  ║   0-39%   → Needs Improvement ★★☆☆☆                   ║
  ║                                                        ║
  ╚════════════════════════════════════════════════════════╝
    """
    print(help_text)
