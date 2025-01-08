import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from collections import Counter
from typing import List
import sys
print(sys.path)  # This will print the list of directories where Python is searching for modules
# Ensure required NLTK data is downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Extract skills from job descriptions
def extract_job_skills(job_descriptions: List[str]):
    all_skills = []
    for desc in job_descriptions:
        tokens = word_tokenize(desc)
        tagged_tokens = pos_tag(tokens)
        # Extract tokens that are tagged as nouns (NN, NNP, NNS, NNPS)
        skills = [token for token, tag in tagged_tokens if tag in ["NN", "NNP", "NNS", "NNPS"]]
        all_skills.extend(skills)
    return [skill for skill, count in Counter(all_skills).most_common(10)]

# Parse resume for skills
def parse_resume(resume_text: str):
    tokens = word_tokenize(resume_text)
    tagged_tokens = pos_tag(tokens)
    # Extract tokens that are tagged as nouns (NN, NNP, NNS, NNPS)
    skills = [token for token, tag in tagged_tokens if tag in ["NN", "NNP", "NNS", "NNPS"]]
    return list(set(skills))

# Perform skill gap analysis
def skill_gap(job_skills: List[str], resume_skills: List[str]):
    job_set = set(job_skills)
    resume_set = set(resume_skills)
    missing_skills = job_set - resume_set
    return list(missing_skills)