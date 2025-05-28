print("Hello, World!")

age = input("Enter you age: ") # age is string
print(f"You are {age} years old.")
age = int(age)
if age < 18: 
    print("You are a minor.")
else:
    print("You are an adult.")
