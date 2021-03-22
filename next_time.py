def next_time(time):
    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    time[4] += 1
    if time[4] == 60:
        time[4] = 0
        time[3] += 1
    if time[3] == 24:
        time[3] = 0
        time[2] += 1
    if time[2] > days_in_months[time[1] - 1]:
        time[2] = 1
        time[1] += 1
    if time[1] == 13:
        time[1] = 1
        time[0] += 1
    return time

def to_utc(time):
    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    time[3] -= 3
    if time[3] < 0:
        time[3] += 24
        time[2] -= 1
    if time[2] <= 0:
        time[1] -= 1
        if time[1] == 0:
            time[0] -= 1
            time[1] = 12
        time[2] = days_in_months[time[1] - 1]
    return time

def to_msk(time):
    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    time[3] += 3
    if time[3] >= 24:
        time[3] -= 24
        time[2] += 1
    if time[2] > days_in_months[time[1] - 1]:
        time[2] = 1
        time[1] += 1
    if time[1] == 13:
        time[1] = 1
        time[0] += 1
    return time
