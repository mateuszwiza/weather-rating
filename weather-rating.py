import pandas as pd


def process_input(path):
    # Load a text file from https://www.knmi.nl/nederland-nu/klimatologie/daggegevens
    file = open(path)
    output = []
    start = False

    # Delete the header of the file containing description and leave only data
    for line in file:
        if start:
            output.append(line)
        else:
            if "#" in line:
                output.append(line)

            # Set the start date for data (WARNING: older records tend to have missing data)
            if "20170101" in line:
                start = True
                output.append(line)

    file.close()

    f = open('weather.csv', 'w')
    f.writelines(output)
    f.close()


# Function for calculating weather rating as described on: http://www.meteovista.co.uk/weather-rating/2971/0
def weather_rating(row):
    # Initialize Rating at 10
    rating = 10

    sun = row['   SP']  # SP = Percentage of the longest possible sunshine duration;
    rain = row['   DR']  # DR = Duration of precipitation (in 0.1 hours);
    wind = row['   FG']  # FG = 24-hour average wind speed (in 0.1 m / s);
    clouds = row[
        '   NG']  # NG = 24-hour average cloud cover (degree of cover of the upper air in eighths, 9 = upper air invisible);

    if clouds < 2:
        rating -= 0
    elif clouds < 6:
        rating -= 1
    elif clouds < 8:
        rating -= 2
    else:
        rating -= 3

    if sun < 20:
        rating -= 2
    elif sun < 50:
        rating -= 1
    else:
        rating -= 0

    if rain > 83:
        rating -= 4
    elif rain > 50:
        rating -= 3
    elif rain > 15:
        rating -= 2
    elif rain > 1:
        rating -= 1
    else:
        rating -= 0

    if wind < 110:
        rating -= 0
    elif wind < 190:
        rating -= 1
    elif wind < 380:
        rating -= 2
    else:
        rating -= 3

    if rating < 1:
        rating = 1

    return rating


process_input('raw_data.txt')
data = pd.read_csv("weather.csv", sep=",")
data['Weather Rating'] = data.apply(lambda row: weather_rating(row), axis=1)
