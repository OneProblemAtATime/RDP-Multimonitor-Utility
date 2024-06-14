if 1 == 1:
    print("1 is in fact 1")
else:
    pass

numstr = "one"
match numstr:
    case "one":
        result = 1
    case "two" | "three":
        result = (2, 3)
    case _:
        result = "Not an expected case."

print(result)
