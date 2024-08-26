import math
import requests
import re
#source https://www.perplexity.ai
#prompt: can you write me a password entropy checker. 
# That uses online free dictionaries to help check dictionary words  and scores a password quality with 0 - 100 score ?

# Description: 
# This script does the following:
# Fetches a dictionary of English words from a GitHub repository.
# Calculates the entropy of the password based on its length and character set.
# Reduces the entropy if dictionary words are found in the password.
#Assigns a base score based on the calculated entropy.
#Adjusts the score based on additional factors like password length, character variety, and use of different character types.
# Returns a final score between 0 and 100.
# Mathematic formula used: E = log2(RL)

#To use this script:
#    Install the requests library if you haven't already: pip install requests
#    Run the script and enter a password when prompted.
#    The script will output a score from 0 to 100, indicating the password's strength.

def fetch_dictionary():
    url = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
    response = requests.get(url)
    return set(response.text.splitlines())

def calculate_entropy(password, dictionary):
    length = len(password)
    lowercase = sum(1 for c in password if c.islower())
    uppercase = sum(1 for c in password if c.isupper())
    digits = sum(1 for c in password if c.isdigit())
    special = length - lowercase - uppercase - digits
    
    char_set_size = 0
    if lowercase: char_set_size += 26
    if uppercase: char_set_size += 26
    if digits: char_set_size += 10
    if special: char_set_size += 32
    
    entropy = length * math.log2(char_set_size)
    
    # Check for dictionary words
    words = re.findall(r'\b\w+\b', password.lower())
    for word in words:
        if word in dictionary:
            entropy *= 0.75  # Reduce entropy for dictionary words
    
    return entropy

def score_password(password):
    dictionary = fetch_dictionary()
    entropy = calculate_entropy(password, dictionary)
    
    # Score based on entropy
    if entropy < 28:
        base_score = 0
    elif entropy < 36:
        base_score = 20
    elif entropy < 60:
        base_score = 40
    elif entropy < 128:
        base_score = 60
    else:
        base_score = 80
    
    # Adjust score based on additional factors
    if len(password) < 8:
        base_score -= 10
    if len(set(password)) < len(password) * 0.75:
        base_score -= 10  # Penalize repetitive characters
    if not any(c.isupper() for c in password):
        base_score -= 5
    if not any(c.islower() for c in password):
        base_score -= 5
    if not any(c.isdigit() for c in password):
        base_score -= 5
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        base_score -= 5
    
    return max(0, min(100, base_score))

# Example usage
password = input("Enter a password to check: ")
score = score_password(password)
print(f"Password strength score: {score}/100")

