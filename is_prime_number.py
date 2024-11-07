def is_prime(number):
    if number < 2:
        return False
    for i in range(2, number):
        if number % i == 0:
            return True

    
    return False


def total_sum(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total
