try:
    x = 10/0
except:
    print("Division by zero.")
finally:
    print("This always runs at the end.")


try:
    answer = input("Enter a number to divide 10 by: ")
    num = int(answer)
    print(10/num)
except ZeroDivisionError as e:
    print("Division by zero.")
    print(e)
except ValueError as e:
    print("Invalid number.")
    print(e)