import datetime
import calendar


def get_upcoming_years(num_years):
    current_year = datetime.datetime.now().year
    upcoming_years = [current_year + i for i in range(num_years)]
    return upcoming_years


# num_years = 3  # You can change this to any number of upcoming years you want
# upcoming_years = get_upcoming_years(num_years)
# print(upcoming_years)


def get_enumerated_months_in_following_year(chosen_year, current_month):
    current_year = datetime.datetime.now().year

    if current_year < chosen_year:
        return list(enumerate([
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ], start=1))
    elif current_year == chosen_year:
        return list(enumerate([
            month.strftime("%B") for month in
            (datetime.datetime(current_year, i + 1, 1) for i in range(current_month - 1, 12))
        ], start=current_month))
    else:
        return []


# chosen_year = 2028
# current_month = datetime.datetime.now().month

# months = get_months_in_following_year(chosen_year, current_month)
# print(months)


def get_days_in_following_month(current_year, current_month):
    _, last_day = calendar.monthrange(current_year, current_month)

    days = ["*" if day < datetime.datetime.now().day and current_year == datetime.datetime.now().year and current_month ==
            datetime.datetime.now().month else str(day) for day in range(1, last_day + 1)]
    return days


# current_year = 2023
# current_month = 9

# days_in_following_month = get_days_in_following_month(current_year, current_month)
# print(days_in_following_month)
