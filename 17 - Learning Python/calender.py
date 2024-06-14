import calendar

def main():
    c = calendar.TextCalendar(calendar.SUNDAY)
    string = c.formatmonth(2024, 1, 0, 0)
    print(string)

    hc = calendar.HTMLCalendar(calendar.SUNDAY)
    string = hc.formatmonth(2024, 1)
    print(string)

    for i in c.itermonthdays(2024, 5):
        print(i)

    for name in calendar.month_name:
        print(name)
    
    for day in calendar.day_name:
        print(day)

    print("team meetings will be on: ")
    for m in range(1, 13):
        cal = calendar.monthcalendar(2024, m)
        weekone = cal[0]
        weektwo = cal[1]
        if weekone[calendar.FRIDAY] != 0:
            meetday = weekone[calendar.FRIDAY]
        else:
            meetday = weektwo[calendar.FRIDAY]

        print(calendar.month_name[m], meetday)

def count_days_old(year, month, day):
    count = 0
    for week in calendar.monthcalendar(year, month):
        if week[day] != 0:
            count+=1
    return count       

def count_days(year, month, day):
    return len([week[day] for week in calendar.monthcalendar(year, month)]) 

if __name__ == "__main__":
    main()
    print(count_days(2025, 12, 0))