nums = list(map(int, input("Enter numbers: ").split()))

largest = nums[0]

for n in nums:
    if n > largest:
        largest = n

print("Largest number:", largest)