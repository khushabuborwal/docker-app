import os
import collections
import socket
import nltk
import re

# Ensure necessary resources are available
nltk.download("punkt")

# File paths
file1_path = "/home/data/IF-1.txt"
file2_path = "/home/data/AlwaysRememberUsThisWay-1.txt"
output_path = "/home/data/output/result.txt"

# Contractions dictionary
CONTRACTIONS = {
    "i'm": ["i", "am"], "can't": ["can", "not"], "don't": ["do", "not"],
    "it's": ["it", "is"], "you're": ["you", "are"], "you'll": ["you", "will"],
    "you've": ["you", "have"], "that's": ["that", "is"], "couldn't": ["could", "not"],
    "won't": ["will", "not"], "i'll": ["i", "will"], "didn't": ["did", "not"],
    "doesn't": ["does", "not"], "shouldn't": ["should", "not"], "isn't": ["is", "not"]
}

# Normalize apostrophes in text
def normalize_apostrophes(text):
    return text.replace("’", "'")

# Expand contractions
def expand_contractions(text):
    words = text.split()
    expanded_words = []
    for word in words:
        word_lower = word.lower()
        if word_lower in CONTRACTIONS:
            # print(f"Expanding contraction: {word_lower} -> {CONTRACTIONS[word_lower]}")  # DEBUG
            expanded_words.extend(CONTRACTIONS[word_lower])
        else:
            expanded_words.append(word_lower)
    return " ".join(expanded_words)

# Read and tokenize words
def count_words(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().lower()
        # print(f"Original Text from {file_path}:\n{text}\n")  # DEBUG
        
        # Normalize apostrophes
        text = normalize_apostrophes(text)
        # print(f"After Normalizing Apostrophes:\n{text}\n")  # DEBUG
        
        # Expand contractions
        text = expand_contractions(text)
        # print(f"After Expanding Contractions:\n{text}\n")  # DEBUG
        
        # Use regex to split text into words, handling em dashes and apostrophes
        words = re.findall(r"\b[\w'-]+\b|—", text)
        # Split words separated by em dashes
        split_words = []
        for word in words:
            if "—" in word:
                # Split by em dash and filter out empty strings
                split_words.extend([w for w in word.split("—") if w])
            else:
                split_words.append(word)
        # print(f"Tokenized Words (Before Expanding Contractions):\n{split_words}\n")  # DEBUG
        
        # Expand contractions in the split words
        expanded_split_words = []
        for word in split_words:
            word_lower = word.lower()
            if word_lower in CONTRACTIONS:
                # print(f"Expanding contraction: {word_lower} -> {CONTRACTIONS[word_lower]}")  # DEBUG
                expanded_split_words.extend(CONTRACTIONS[word_lower])
            else:
                expanded_split_words.append(word_lower)
        # print(f"Tokenized Words (After Expanding Contractions):\n{expanded_split_words}\n")  # DEBUG
        
        # Count occurrences of "you"
        you_count = expanded_split_words.count("you")
        # print(f"Occurrences of 'you': {you_count}\n")  # DEBUG

    return expanded_split_words, len(expanded_split_words)

# Get top N words
def top_words(words, n=3):
    counter = collections.Counter(words)
    return counter.most_common(n)

# Get IP Address
def get_ip_address():
    return socket.gethostbyname(socket.gethostname())

# Process files
words1, count1 = count_words(file1_path)
words2, count2 = count_words(file2_path)

# Grand total
grand_total = count1 + count2

# Top 3 words
top3_if1 = top_words(words1)
top3_always = top_words(words2)  # No need to re-expand contractions

# Get IP
ip_address = get_ip_address()

# Write results
os.makedirs("/home/data/output", exist_ok=True)
with open(output_path, "w") as output_file:
    output_file.write(f"Word count in IF-1.txt: {count1}\n")
    output_file.write(f"Word count in AlwaysRememberUsThisWay-1.txt: {count2}\n")
    output_file.write(f"Grand Total Word Count: {grand_total}\n")
    output_file.write(f"Top 3 words in IF-1.txt: {top3_if1}\n")
    output_file.write(f"Top 3 words in AlwaysRememberUsThisWay-1.txt: {top3_always}\n")
    output_file.write(f"Container IP Address: {ip_address}\n")

# Print results
with open(output_path, "r") as output_file:
    print(output_file.read())