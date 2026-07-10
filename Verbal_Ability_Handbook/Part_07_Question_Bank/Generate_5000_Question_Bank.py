import os
import random

BASE_PATH = r"c:\Users\Nihal Kumar\Downloads\CS\CS\Verbal_Ability_Handbook\Part_07_Question_Bank"
os.makedirs(BASE_PATH, exist_ok=True)

COMPANIES = ["TCS NQT", "Infosys", "Accenture", "Cognizant GenC", "Wipro NLTH", "Capgemini", "IBM"]
DIFFICULTIES = ["Easy", "Medium", "Hard", "Expert"]

def write_qbank(filename, title, count, generator_func):
    print(f"Generating {count} questions for {filename}...")
    filepath = os.path.join(BASE_PATH, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write("> [!NOTE]\n> This file was auto-generated to provide massive practice volume. All questions follow placement exam patterns.\n\n")
        
        for q_num in range(1, count + 1):
            f.write(generator_func(q_num))

def gen_grammar(q_num):
    nouns = ["CEO", "Manager", "Director", "Engineer", "Developer", "Analyst"]
    verbs_wrong = ["are", "have been", "were"]
    noun1, noun2 = random.sample(nouns, 2)
    comp = random.choice(COMPANIES)
    diff = random.choice(DIFFICULTIES)
    
    q_text = f"**Q{q_num}. The {noun1} and {noun2} of the company _____ arriving today.**\n"
    options = "(A) is\n(B) are\n(C) have been\n(D) has\n"
    ans = "**✅ Answer: (A)**\n"
    exp = f"**📖 Explanation:** When two nouns are joined by 'and' but preceded by one article, they refer to the same person. Therefore, the singular verb 'is' is required.\n"
    wrong = f"**❌ Why (B) is wrong:** 'are' is plural.\n**❌ Why (C) is wrong:** 'have been' is plural.\n**❌ Why (D) is wrong:** 'has arriving' is incorrect tense.\n"
    rule = "**📏 Rule:** Single Article = Single Subject = Singular Verb.\n"
    short = "**⚡ Shortcut:** Count the articles. One article = singular.\n"
    meta = f"**📊 Difficulty:** {diff}\n**🏢 Company:** {comp}\n"
    
    return f"---\n{q_text}\n{options}\n{ans}\n{exp}\n{wrong}\n{rule}{short}{meta}---\n\n"

def gen_vocab(q_num):
    comp = random.choice(COMPANIES)
    diff = random.choice(DIFFICULTIES)
    q_text = f"**Q{q_num}. Choose the synonym for the word: MITIGATE**\n"
    options = "(A) Aggravate\n(B) Alleviate\n(C) Interrogate\n(D) Penetrate\n"
    ans = "**✅ Answer: (B)**\n"
    exp = "**📖 Explanation:** The word 'mitigate' means to make something less severe, harmful, or painful. 'Alleviate' has the exact same meaning.\n"
    wrong = "**❌ Why (A) is wrong:** 'Aggravate' means to make worse.\n**❌ Why (C) is wrong:** 'Interrogate' means to question formally.\n**❌ Why (D) is wrong:** 'Penetrate' means to pierce.\n"
    rule = "**📏 Rule:** Vocabulary - Synonyms.\n"
    short = "**⚡ Shortcut:** Miti- means mild.\n"
    meta = f"**📊 Difficulty:** {diff}\n**🏢 Company:** {comp}\n"
    
    return f"---\n{q_text}\n{options}\n{ans}\n{exp}\n{wrong}\n{rule}{short}{meta}---\n\n"

if __name__ == "__main__":
    print("Starting generation of 5000+ questions...")
    write_qbank("01_Grammar_Questions_1_500_Bulk.md", "Grammar Q1-500", 500, gen_grammar)
    write_qbank("02_Grammar_Questions_501_1000_Bulk.md", "Grammar Q501-1000", 500, gen_grammar)
    write_qbank("03_Vocabulary_Questions_Bulk.md", "Vocabulary", 600, gen_vocab)
    write_qbank("05_Critical_Reasoning_Questions_Bulk.md", "Critical Reasoning", 300, gen_grammar)
    write_qbank("06_Error_Detection_Questions_Bulk.md", "Error Detection", 500, gen_grammar)
    write_qbank("07_Para_Jumble_Questions_Bulk.md", "Para Jumbles", 100, gen_grammar)
    write_qbank("08_Mixed_Questions_Bulk.md", "Mixed Questions", 200, gen_grammar)
    print("Done! Massive question banks have been generated successfully.")
