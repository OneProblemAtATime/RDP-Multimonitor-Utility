import datetime

def main():
    today = datetime.date.today()
    print(today)

    print("Date componenets: ", today.day, today.month, today.year)

    print("Today's weekday # is: ", today.weekday()) #Monday is 0 and Sunday is 6

    today = datetime.datetime.now()
    print(today)

    t = datetime.datetime.time(datetime.datetime.now())
    print(t)


if __name__ == '__main__':
    main()