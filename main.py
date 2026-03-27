"""
main.py - Resume Screening System (CLI Application)
=====================================================
A terminal-based AI tool that evaluates resumes against
predefined job role requirements using NLP techniques
like tokenization and keyword matching.

Author  : Saumya Agarwal
Reg No  : 25BCE10298
Course  : CSA2001 - Artificial Intelligence
Project : Resume Screening System (BYOP)

Usage:
    python main.py
"""

import sys
from utils import (
    clean_text,
    tokenize,
    load_roles,
    load_resume_from_file,
    match_skills,
    calculate_score,
    get_grade,
    generate_suggestions,
    save_analysis,
    load_analysis_history,
    print_header,
    print_menu,
    print_score_report,
    print_roles_list,
    print_history,
    print_help,
    print_separator,
)


# ─────────────────────────────────────────────
#  Global State
# ─────────────────────────────────────────────

resume_text = ""          # Stores the current resume text
selected_role = ""        # Stores the currently selected job role


# ─────────────────────────────────────────────
#  Menu Handler Functions
# ─────────────────────────────────────────────

def handle_paste_resume():
    """
    Option [1]: Allows the user to paste resume text directly.
    
    The user types or pastes their resume content line by line.
    An empty line signals the end of input.
    """
    global resume_text
    
    print("\n  📝  PASTE YOUR RESUME TEXT")
    print("  ─" * 20)
    print("  Type or paste your resume content below.")
    print("  Press ENTER twice (empty line) to finish.\n")
    
    lines = []
    empty_count = 0
    
    try:
        while True:
            line = input("  > ")
            if line.strip() == "":
                empty_count += 1
                if empty_count >= 1 and lines:  # End on first empty line after content
                    break
                elif not lines:
                    print("  [INFO] Please enter some text first.")
                    empty_count = 0
            else:
                empty_count = 0
                lines.append(line)
    except EOFError:
        pass
    
    if lines:
        resume_text = "\n".join(lines)
        word_count = len(tokenize(clean_text(resume_text)))
        print(f"\n  ✅  Resume loaded successfully!")
        print(f"  📊  Word count: {word_count} words")
        print(f"  📄  Lines: {len(lines)}")
    else:
        print("\n  ⚠️  No text was entered. Please try again.")


def handle_load_file():
    """
    Option [2]: Loads resume text from a .txt file.
    
    Prompts the user for the file path and reads the content.
    """
    global resume_text
    
    print("\n  📂  LOAD RESUME FROM FILE")
    print("  ─" * 20)
    print("  Enter the path to your resume file (.txt)")
    print("  Example: data/my_resume.txt\n")
    
    try:
        filepath = input("  File path: ").strip()
    except EOFError:
        return
    
    if not filepath:
        print("\n  ⚠️  No file path provided.")
        return
    
    # Validate file extension
    if not filepath.endswith(".txt"):
        print("\n  ⚠️  Only .txt files are supported.")
        print("  Please save your resume as a plain text file.")
        return
    
    content = load_resume_from_file(filepath)
    
    if content:
        resume_text = content
        word_count = len(tokenize(clean_text(resume_text)))
        print(f"\n  ✅  Resume loaded from: {filepath}")
        print(f"  📊  Word count: {word_count} words")
    else:
        print("\n  ❌  Failed to load resume. Check the file path and try again.")


def handle_select_role(roles):
    """
    Option [3]: Allows the user to select a target job role.
    
    Displays available roles and lets the user pick one by number.
    
    Args:
        roles (dict): Dictionary of available job roles.
    """
    global selected_role
    
    if not roles:
        print("\n  ❌  No roles available. Check roles.json file.")
        return
    
    print_roles_list(roles)
    
    role_names = list(roles.keys())
    
    print(f"\n  Enter role number (1-{len(role_names)}): ", end="")
    try:
        choice = input().strip()
    except EOFError:
        return
    
    # Validate input
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(role_names):
            selected_role = role_names[choice_num - 1]
            role_data = roles[selected_role]
            skill_count = len(role_data.get("required_skills", []))
            print(f"\n  ✅  Selected role: {selected_role}")
            print(f"  📋  Skills to match: {skill_count}")
        else:
            print(f"\n  ⚠️  Invalid choice. Please enter a number between 1 and {len(role_names)}.")
    except ValueError:
        print("\n  ⚠️  Invalid input. Please enter a valid number.")


def handle_analyze(roles):
    """
    Option [4]: Runs the resume analysis against the selected role.
    
    Performs the full screening pipeline:
        1. Validates that resume and role are set
        2. Matches skills using NLP techniques
        3. Calculates score
        4. Generates grade and suggestions
        5. Displays the report
        6. Saves to history
    
    Args:
        roles (dict): Dictionary of available job roles.
    """
    global resume_text, selected_role
    
    # ── Validation ──
    if not resume_text:
        print("\n  ⚠️  No resume loaded!")
        print("  Please use Option [1] or [2] to load a resume first.")
        return
    
    if not selected_role:
        print("\n  ⚠️  No job role selected!")
        print("  Please use Option [3] to select a target role first.")
        return
    
    if selected_role not in roles:
        print(f"\n  ❌  Role '{selected_role}' not found in roles database.")
        return
    
    # ── Get role requirements ──
    role_data = roles[selected_role]
    required_skills = role_data.get("required_skills", [])
    experience_keywords = role_data.get("experience_keywords", [])
    
    if not required_skills:
        print(f"\n  ⚠️  No skills defined for role '{selected_role}'.")
        return
    
    print(f"\n  🔍  Analyzing resume for: {selected_role}")
    print("  ⏳  Processing...\n")
    
    # ── Perform skill matching ──
    matched_skills, missing_skills = match_skills(resume_text, required_skills)
    
    # ── Also check experience keywords (bonus) ──
    matched_exp, _ = match_skills(resume_text, experience_keywords)
    
    # ── Calculate scores ──
    skill_score = calculate_score(len(matched_skills), len(required_skills))
    
    # Bonus points for experience keywords (up to 10% bonus)
    if experience_keywords:
        exp_bonus = calculate_score(len(matched_exp), len(experience_keywords)) * 0.1
    else:
        exp_bonus = 0
    
    # Final score (capped at 100)
    final_score = min(round(skill_score + exp_bonus, 2), 100.0)
    
    # ── Get grade and suggestions ──
    grade, rating = get_grade(final_score)
    suggestions = generate_suggestions(missing_skills, selected_role)
    
    # Add experience keyword info to suggestions if relevant
    if matched_exp:
        suggestions.append(
            f"Good: Your resume mentions relevant experience terms like: "
            f"{', '.join(matched_exp[:3])}"
        )
    
    # ── Display report ──
    print_score_report(
        role_name=selected_role,
        score=final_score,
        grade=grade,
        rating=rating,
        matched=matched_skills,
        missing=missing_skills,
        suggestions=suggestions
    )
    
    # ── Save to history ──
    save_analysis(selected_role, final_score, grade, matched_skills, missing_skills)
    print("\n  💾  Analysis saved to history.")


def handle_view_history():
    """Option [5]: Displays past analysis records."""
    history = load_analysis_history()
    print_history(history)


def handle_view_roles(roles):
    """
    Option [6]: Displays all available roles with details.
    
    Args:
        roles (dict): Dictionary of available job roles.
    """
    if not roles:
        print("\n  ❌  No roles available.")
        return
    
    print_roles_list(roles)
    
    # Ask if user wants to see skills for a specific role
    print(f"\n  Enter role number to see required skills (or 0 to go back): ", end="")
    try:
        choice = input().strip()
    except EOFError:
        return
    
    try:
        choice_num = int(choice)
        role_names = list(roles.keys())
        
        if choice_num == 0:
            return
        elif 1 <= choice_num <= len(role_names):
            role = role_names[choice_num - 1]
            skills = roles[role].get("required_skills", [])
            exp_keys = roles[role].get("experience_keywords", [])
            
            print(f"\n  📋  Skills for {role}:")
            print(f"  {'─' * 40}")
            print(f"\n  Required Skills ({len(skills)}):")
            for i in range(0, len(skills), 4):
                row = skills[i:i + 4]
                formatted = "  |  ".join(row)
                print(f"    {formatted}")
            
            if exp_keys:
                print(f"\n  Experience Keywords ({len(exp_keys)}):")
                for i in range(0, len(exp_keys), 3):
                    row = exp_keys[i:i + 3]
                    formatted = "  |  ".join(row)
                    print(f"    {formatted}")
        else:
            print("\n  ⚠️  Invalid choice.")
    except ValueError:
        print("\n  ⚠️  Invalid input.")


# ─────────────────────────────────────────────
#  Main Application Loop
# ─────────────────────────────────────────────

def main():
    """
    Main entry point of the Resume Screening System.
    
    Runs the interactive CLI menu loop that handles user
    input and dispatches to the appropriate handler function.
    """
    global resume_text, selected_role
    
    # Display application header
    print_header()
    
    # Load job roles from JSON
    roles = load_roles()
    if not roles:
        print("\n  ❌  FATAL: Could not load job roles. Exiting.")
        sys.exit(1)
    
    print(f"  ✅  Loaded {len(roles)} job roles from database.")
    
    # ── Main Menu Loop ──
    while True:
        # Show current status
        print(f"\n  {'─' * 40}")
        resume_status = "✅ Loaded" if resume_text else "❌ Not loaded"
        role_status = f"✅ {selected_role}" if selected_role else "❌ Not selected"
        print(f"  Resume: {resume_status}  |  Role: {role_status}")
        
        # Display menu
        print_menu()
        
        # Get user choice
        try:
            choice = input("  Enter your choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  👋  Goodbye! Thank you for using Resume Screening System.")
            break
        
        # ── Route to handler ──
        if choice == "1":
            handle_paste_resume()
        
        elif choice == "2":
            handle_load_file()
        
        elif choice == "3":
            handle_select_role(roles)
        
        elif choice == "4":
            handle_analyze(roles)
        
        elif choice == "5":
            handle_view_history()
        
        elif choice == "6":
            handle_view_roles(roles)
        
        elif choice == "7":
            print_help()
        
        elif choice == "0":
            print("\n  👋  Goodbye! Thank you for using Resume Screening System.")
            print("  📄  Your analysis history has been saved.\n")
            break
        
        else:
            print(f"\n  ⚠️  Invalid choice: '{choice}'")
            print("  Please enter a number between 0 and 7.")


# ─────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    main()
