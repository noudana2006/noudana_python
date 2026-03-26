text = input("Enter a word or number: ")

# Remove spaces and convert to lowercase
clean_text = text.replace(" ", "").lower()

# Reverse the string
reverse_text = clean_text[::-1]

if clean_text == reverse_text:
    print("It is a palindrome")
else:
    print("Not a palindrome")