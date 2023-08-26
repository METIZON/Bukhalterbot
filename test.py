# from datetime import datetime, timedelta


# def save_10min_periods(periods):
#     result = []

#     for period in periods:
#         start = period[0]
#         end = period[1]

#         current_time = start
#         while current_time < end:
#             next_time = current_time + timedelta(minutes=10)
#             if next_time > end:
#                 next_time = end

#             result.append([current_time, next_time])
#             current_time = next_time

#     return result


# def extract_hours(periods):
#     hour_set = set()

#     for period in periods:
#         start_time = period[0]
#         hour_set.add(start_time.hour)

#     return hour_set


# def get_time_periods_by_hour(hour, periods):
#     selected_periods = []

#     for start, end in periods:
#         if start.hour == hour:
#             selected_periods.append([start, end])

#     return selected_periods


# # Example array of datetime periods
# periods = [
#     [datetime(2023, 8, 23, 8, 0), datetime(2023, 8, 23, 13, 30)],
#     [datetime(2023, 8, 23, 16, 0), datetime(2023, 8, 23, 18, 0)]
# ]

# # Call the function with the example array
# result_periods = save_10min_periods(periods)

# # Print the resulting array of 10-minute periods
# print(result_periods)
# for period in result_periods:
#     print(period[0].time(), '-', period[1].time())

# hour_set = extract_hours(result_periods)

# # Print the set of unique hours
# print(hour_set)

# free_per = get_time_periods_by_hour(10, result_periods)
# print(free_per)
# for per in free_per:
#     print(per[0].time(), '-', per[1].time())


# import datetime


# def get_enumerated_months_in_following_year(chosen_year, current_month):
#     current_year = datetime.datetime.now().year

#     if current_year < chosen_year:
#         return list(enumerate([
#             "January", "February", "March", "April", "May", "June",
#             "July", "August", "September", "October", "November", "December"
#         ], start=1))
#     elif current_year == chosen_year:
#         return list(enumerate([
#             month.strftime("%B") for month in
#             (datetime.datetime(current_year, i + 1, 1) for i in range(current_month, 12))
#         ], start=current_month + 1))
#     else:
#         return []


# chosen_year = 2028
# current_month = datetime.datetime.now().month

# months = get_enumerated_months_in_following_year(chosen_year, current_month)
# print(months)

# import calendar
# import datetime


# def get_days_in_following_month(current_year, current_month):
#     _, last_day = calendar.monthrange(current_year, current_month)

#     days = ["*" if day < datetime.datetime.now().day and current_year == datetime.datetime.now().year and current_month ==
#             datetime.datetime.now().month else str(day) for day in range(1, last_day + 1)]
#     return days


# current_year = 2023
# current_month = 9

# days_in_following_month = get_days_in_following_month(current_year, current_month)
# print(days_in_following_month)


# import datetime

# # veteran_acceptDate_2024_2_25_consultation

# target_date = datetime.date('2024', '2', '25')

# a = [[1], [2]]
# b = [[3], [4]]

# b += a

# print(b)

import requests

url = 'https://api.monobank.ua/personal/client-info'

headers = {
    'X-Token': "ulOHtlSM9Fdjybk5MlD_-kujufLCx8i-Ay_aPYlQ-A24"
}

print(requests.get(url, headers=headers).text)

# {"token": "ya29.a0AfB_byByMe0JB5pPAOQ4xORTbwO6L82JAKiAR07AnNvZ2XCI_cag2fLTZm4EdrWgK3WtlJNewKWmYP8YnNOlFp_uE1TQkk1wAPXPZJ3oTfTQDFzLS2FmENzJ8Sgy3pPZ7aCI4xOd7gjxkMj1vp4S0-EPRGN71DpNpppSAfeCuQaCgYKAZoSARISFQHsvYlsu28VQmysf6DOeXO6WyuvZA0177", "refresh_token": "1//0ckox5gdOabWOCgYIARAAGAwSNwF-L9Irog5_XJc71QIE-pVCROCfN4mpZBUJwl7thQIijbX3WjQVz4u8WAeLWmOMjmdjZ1L5hkg", "token_uri": "https://oauth2.googleapis.com/token", "client_id": "82361057406-3older3jikdoam44pk266hduqbmqeg2j.apps.googleusercontent.com", "client_secret": "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", "scopes": ["https://www.googleapis.com/auth/calendar"], "expiry": "2023-08-26T19:33:33.196964Z"}
# {"token": "ya29.a0AfB_byAUpA-cQz09wBYaPYqVvNZ320rVRs3skBa47-b2RNGviCKde6la2VAivztEcJGiFanGROHwo5V5CbolclVeOQFd51nJQ8CraJTOBtAvW6JltY0qriRv9gXCylOiGOi76M9aReSLQQn2VEoXJwFMQS3OVjAh1ZUt2K3R1AaCgYKAVASARISFQHsvYlsRlllI4uOSHI1CIGfnpy96w0177", "refresh_token": "1//0ckox5gdOabWOCgYIARAAGAwSNwF-L9Irog5_XJc71QIE-pVCROCfN4mpZBUJwl7thQIijbX3WjQVz4u8WAeLWmOMjmdjZ1L5hkg", "token_uri": "https://oauth2.googleapis.com/token", "client_id": "82361057406-3older3jikdoam44pk266hduqbmqeg2j.apps.googleusercontent.com", "client_secret": "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", "scopes": ["https://www.googleapis.com/auth/calendar"], "expiry": "2023-08-26T20:16:24.060196Z"}
