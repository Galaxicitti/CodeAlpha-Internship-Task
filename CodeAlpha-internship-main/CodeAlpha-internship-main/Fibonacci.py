def fibonacci(n):
    numbers = [0, 1]

    while len(numbers) < n:
        next_number = numbers[-1] + numbers[-2]
        numbers.append(next_number)

    return numbers[:n]

# lets generate the first 12 numbers 
n = 12
sequence = fibonacci(n)
print("Fibonacci sequence up to {n} numbers:", sequence)
