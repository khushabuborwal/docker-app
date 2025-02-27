import os
import re
import collections
import socket
import nltk

# Ensure necessary resources are available
nltk.download("punkt")

# File paths
file1_path = "/home/data/IF-1.txt"
file2_path = "/home/data/AlwaysRememberUsThisWay-1.txt"
output_path = "/home/data/output/result.txt"

# Function to read and count words
def count_words(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().lower()
        words = nltk.word_tokenize(text)
        words = [word for word in words if word.isalpha()]  # Keep only alphabetic words
        # words = nltk.word_tokenize(file.read().lower())
    return words, len(words)

# Function to find the top 3 most frequent words
def top_words(words, n=3):
    words = [word.lower() for word in words]
    counter = collections.Counter(words)
    return counter.most_common(n)

# Function to handle contractions
def handle_contractions(words):
    contractions = {
        "i'm": ["i", "am"], "can't": ["can", "not"], "don't": ["do", "not"],
        "it's": ["it", "is"], "you're": ["you", "are"], "you’ll": ["you", "will"],
        "you’ve": ["you", "have"], "that’s": ["that", "is"], "couldn't": ["could", "not"],
        "won't": ["will", "not"], "i'll": ["i", "will"]
    }
    expanded_words = []
    for word in words:
        expanded_words.extend(contractions.get(word.lower(), [word.lower()]))  # Case insensitive
    return expanded_words

# Get the machine's IP address
def get_ip_address():
    return socket.gethostbyname(socket.gethostname())

# Process the files
words1, count1 = count_words(file1_path)
words2, count2 = count_words(file2_path)

# Grand total word count
grand_total = count1 + count2

# Top 3 words in IF-1.txt
top3_if1 = top_words(words1)

# Process contractions in AlwaysRememberUsThisWay-1.txt
words2_expanded = handle_contractions(words2)
top3_always = top_words(words2_expanded)

# Get IP Address
ip_address = get_ip_address()

# Write results to output file
os.makedirs("/home/data/output", exist_ok=True)
with open(output_path, "w") as output_file:
    output_file.write(f"Word count in IF-1.txt: {count1}\n")
    output_file.write(f"Word count in AlwaysRememberUsThisWay-1.txt: {count2}\n")
    output_file.write(f"Grand Total Word Count: {grand_total}\n")
    output_file.write(f"Top 3 words in IF-1.txt: {top3_if1}\n")
    output_file.write(f"Top 3 words in AlwaysRememberUsThisWay-1.txt: {top3_always}\n")
    output_file.write(f"Container IP Address: {ip_address}\n")

# Print the result to console
with open(output_path, "r") as output_file:
    print(output_file.read())
