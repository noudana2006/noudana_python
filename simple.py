a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

print("1. Add\n2. Subtract\n3. Multiply\n4. Divide")
choice = input("Choose operation (1/2/3/4): ")

if choice == "1":
    print("Result:", a + b)
elif choice == "2":
    print("Result:", a - b)
elif choice == "3":
    print("Result:", a * b)
elif choice == "4":
    print("Result:", a / b)
else:
    print("Invalid choice")