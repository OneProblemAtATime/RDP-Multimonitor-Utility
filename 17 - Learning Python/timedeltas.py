from datetime import date, time, datetime, timedelta

def main():
    print(timedelta(days=365, hours=5, minutes=1))
    now = datetime.now()
    print("One year from now it will be", str(now+timedelta(days=365*4)))
    print(str(now + timedelta(weeks=3, days=3)))
    t = datetime.now() - timedelta(weeks=1)
    s = t.strftime("%A %B %d, %Y")
    print(s)

    today = date.today()
    afd = date(today.year, 4, 1)
    if afd < today:
        print(str((today-afd).days))
        afd = afd.replace(year = today.year+1)

    time_to_afd = afd-today
    print(time_to_afd)



if __name__ == '__main__':
    main()