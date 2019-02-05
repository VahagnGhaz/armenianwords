with open("letter_2.txt", "rb") as f:
    a = f.read().decode().split()
    a = list(set(a))
print(len(a))
