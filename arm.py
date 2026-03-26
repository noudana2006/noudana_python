num = int(input("Enter a number: "))
power = len(str(num))
temp = num
sum = 0

while temp > 0:
    digit = temp % 10
    sum += digit ** power
    temp //= 10

if sum == num:
    print("Armstrong number")
else:
    print("Not Armstrong")