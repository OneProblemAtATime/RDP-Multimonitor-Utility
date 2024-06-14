test_words = ["Hello World!", "Radar", "Mama?", "Madam, I'm Adam.", "Race car!"]

def is_palindrome(test_str):
    test_str = test_str.lower()
    special_characters = [" ", "!", "'", "?", ",", "."]

    for character in special_characters:
        test_str = test_str.replace(character, "")

    for i in range(len(test_str)-1):
        if test_str[i] != test_str[-1*(i+1)]:
            return False
    
    return True

for word in test_words:
    print(is_palindrome(word))