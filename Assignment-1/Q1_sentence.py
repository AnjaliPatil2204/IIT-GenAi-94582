#Q1:Write a Python program that takes a sentence from the user and prints:
# Number of characters 
# Number of words
#Number of vowels
#Hint: Use split(), loops, and vowel checking.
def analyze_sentence(sentence):
    # Number of characters
    num_characters = len(sentence)

    # Number of words
    words = sentence.split()
    num_words = len(words)

    # Number of vowels
    vowels = 'aeiouAEIOU'
    num_vowels = sum(1 for char in sentence if char in vowels)

    return num_characters, num_words, num_vowels
# Taking input from the user
user_input = input("Please enter a sentence: ")
characters, words, vowels = analyze_sentence(user_input)
print(f"Number of characters: {characters}")
print(f"Number of words: {words}")
print(f"Number of vowels: {vowels}")
