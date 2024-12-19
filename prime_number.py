def is_prime(number):
    if number < 2:
        return False
    for i in range(2, number):
        if number % i == 0:
            return False

    
    return True

print("hello world")
print("goodbye world")
print("hola mundo")
