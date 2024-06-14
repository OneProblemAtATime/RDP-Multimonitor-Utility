from datetime import datetime

def main():
    now = datetime.now()

    print(now.strftime("The current year is %Y"))

    print(now.strftime("%a, %d %B, %y"))

    print(now.strftime("%c, %x, %X"))

    print(now.strftime("%I:%M:%S %p - %H:%M"))

if __name__ == "__main__":
    main()