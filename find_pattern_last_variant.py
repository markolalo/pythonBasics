# from bakery import assert_equal

# def find_last_question(words: list[str])-> str:
#     result = "Missing"
#     for word in words:
#         if word[-1] == "?":
#             result = word
    
#     return result

# some_words = ["Hi?", "Oh.", "Uh?"]
# assert_equal(find_last_question(some_words), "Uh?")
words = ["Oh", "Hi", "There!", "Okay", "Bye!"]
taking = True
first_words = []

for word in words:
    if word[-1] == "!":
        taking = False
    elif taking:
        first_words.append(word)

print(first_words)