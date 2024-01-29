import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import shutil
import random

# Anzahl der Participants und Tage
num_participants = 25
num_days = 7


# Funktion, um eine zufällige Uhrzeit mit einem maximalen 5-Minuten-Intervall zu generieren
def random_5m_time(start_time):
    start_time = start_time[:5]
    start_time = f"{start_time}:00"
    start_datetime = datetime.strptime(start_time, '%H:%M:%S')
    start_hour = start_datetime.hour
    start_minute = start_datetime.minute
    start_second = start_datetime.second

    minutes_offset = random.randint(1, 4)
    seconds_offset = random.randint(0, 59)
    total_seconds_offset = start_second + seconds_offset
    if total_seconds_offset >= 60:
        minutes_offset = minutes_offset + 1
        seconds_offset = total_seconds_offset % 60

    random_datetime = start_datetime + timedelta(minutes=minutes_offset, seconds=seconds_offset)
    random_time = random_datetime.strftime('%H:%M:%S')

    return random_time


# ein Monat einem gegebenen Datum hinzufügen
def add_month_to_date(firstdate):
    given_date = datetime.strptime(firstdate, '%Y-%m-%d')
    new_date = given_date + relativedelta(months=1)
    new_date = new_date.strftime('%Y-%m-%d')

    return new_date


# Generierung von random time in der form "hh:mm"
def random_24_hour_time():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    formatted_time = f"{hour:02d}:{minute:02d}"

    return formatted_time


# Generierung von random date
def random_date():
    year = 2024
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    formatted_date = f"{year:04d}-{month:02d}-{day:02d}"

    return formatted_date


# random entry für Form Spalte
def random_entry():
    options = ["Initial", "EMA", "Missing"]
    zahl = random.randint(1, 10)
    if zahl == 10:
        selected_entry = options[0]
    selected_entry = random.choice(options)

    return selected_entry


# Standorte und Visiten
locations = ["BE", "GE", "SK", "SK_Kosice", "UK"]
visits = ["T0", "T1", "T2", "T3"]
moods = ["happy", "bored", "insecure", "angry", "sad", "irritated", "content", "relaxed", "anxious", "enthusiastic"]
# activitys = ["activityvalence","activityskill","activitychallenge"]
activities = ["EMA_activityvalence", "EMA_activityskill", "EMA_activitychallenge"]
socials = ["alone_ratherothers", "withothers_ratheralone", "social_satisfaction"]
events = ["eventunpleasant", "qol", "disturbance"]
optional = ["participant_id", "period", "site", "start_time", "end_time"]
columns = ["Participant", "Trigger", "Trigger_date", "Trigger_time", "Trigger_counter", "Form", "Form_start_date",
           "Form_start_time", "Form_finish_date", "Form_finish_time", "Form_upload_date", "Form_upload_time", "Missing",
           "item_815"]
for mood in moods: columns.append("EMA_" + mood)
columns.append("EMA_location")
for i in range(1, 12): columns.append("EMA_activity_" + str(i))
for act in activities: columns.append(act)
for i in range(1, 9): columns.append("EMA_social_" + str(i))
for soc in socials: columns.append("EMA_" + soc)
columns.append("EMA_event")
for event in events: columns.append("EMA_" + event)
columns.extend(optional)

# Erstelle leere Listen für die Daten
data = []

# Schleife durch alle Standorte und Visiten
# for location in locations:
Trigger_possibilites = ["Initial", "Button Pressed: Start form", "Random Time:"]

for participant_id in range(1, num_participants + 1):
    lastday = ""
    count = 1

    for day in range(num_days):

        if lastday == "":
            lastday = random_date()  # Generiert ein random date
        else:  # TODO ein Tag hinzufügen, um der Tag vom nächsten gefolgt wird
            lastday = lastday
            original_date = datetime.strptime(lastday, "%Y-%m-%d")
            new_date = original_date + timedelta(days=1)
            lastday = new_date.strftime("%Y-%m-%d")

        for trigger_num in range(0, 10):  # trigger_num = Zeile pro Participant
            num_cells_to_fill = random.randint(20, 50)
            col_num = 0
            # initial und Button Pressed überspringen wenn day!=0
            if (trigger_num == 0 or trigger_num == 1) and day != 0: continue
            row_data = []
            Form_entry = ""
            Missing_entry = ""
            # miss_num=0

            for column in columns:
                col_num += 1
                # TODO To Add the correct Time Entries for Formstart date.
                if column == "Participant":
                    row_data.append(participant_id)

                elif column == "Trigger":
                    if trigger_num <= 1:
                        row_data.append(Trigger_possibilites[trigger_num])
                    else:
                        row_data.append(Trigger_possibilites[2] + str(random_24_hour_time()))

                elif column == "Trigger_date":
                    row_data.append(lastday)

                elif column == "Trigger_time":
                    timearr = ["07:30", "07:35", "08:00", "09:30", "11:00", "12:30", "14:00", "15:30", "17:00", "18:30"]
                    row_data.append(timearr[trigger_num])

                elif "counter" in column:
                    row_data.append(count)
                    count = count + 1

                elif "date" in column:
                    if column == "Form_upload_date" and Form_entry == "Missing":
                        row_data.append(add_month_to_date(lastday))
                    else:
                        row_data.append(lastday)

                elif column == "Form_start_time":
                    time = timearr[trigger_num]
                    forum_start = random_5m_time(time)
                    row_data.append(forum_start)

                elif column == "Form_finish_time":
                    if Form_entry == "Missing":
                        row_data.append(forum_start)
                    else:
                        forum_finish = random_5m_time(forum_start)
                        row_data.append(forum_finish)


                elif column == "Form_upload_time":

                    if Form_entry == "Missing":
                        row_data.append(forum_start)
                    else:
                        forum_upload = random_5m_time(forum_finish)
                        row_data.append(forum_upload)


                elif column == "Form":
                    if trigger_num == 0:
                        row_data.append("Initial")
                        Form_entry = "Initial"
                    else:
                        # 5% Wahscheinlichkeit, dass Form_entry auf "Missing" gesetzt wird
                        zahl = random.randint(0, 20)
                        if zahl == 20:
                            Form_entry = "Missing"
                        else:
                            Form_entry = "EMA"
                        row_data.append(Form_entry)

                elif column == "item_815" or column == "EMA_event":
                    row_data.append("")

                elif column == "Missing":
                    if Form_entry == "Missing":
                        possibs = ["Dismissed", "Ignored", "Incomplete"]
                        Missing_entry = random.choice(possibs)
                        row_data.append(Missing_entry)
                    else:
                        row_data.append("")
                        Missing_entry = ""

                elif "social" in column or "activity" in column and column not in activities:
                    if trigger_num == 0 and day == 0:
                        row_data.append("")
                    elif (Missing_entry == "Dismissed" or Missing_entry == "Ignored") and Form_entry == "Missing":
                        row_data.append("")
                    elif Missing_entry == "Incomplete" and Form_entry == "Missing":
                        if col_num <= num_cells_to_fill:
                            # 5% Chance for an empty entry.
                            number5 = random.randint(1, 20)
                            if number5 <= 2:
                                row_data.append("")
                            else:
                                row_data.append(random.randint(0, 1))
                        else:
                            row_data.append("")

                    else:
                        row_data.append(random.randint(0, 1))

                elif column == "EMA_location":
                    if trigger_num == 0 and day == 0:
                        row_data.append("")
                    elif (Missing_entry == "Dismissed" or Missing_entry == "Ignored") and Form_entry == "Missing":
                        row_data.append("")
                    elif Form_entry == "Missing" and Missing_entry == "Incomplete":
                        if col_num <= num_cells_to_fill:
                            # 5% Chance for an empty entry.
                            number5= random.randint(1,20)
                            if number5 <= 2:
                                row_data.append("")
                            else:
                                row_data.append(random.randint(1, 8))
                        else:
                            row_data.append("")
                    else:
                        row_data.append(random.randint(1, 8))

                elif column in optional:
                    if trigger_num == 0:
                        if column == "participant_id":
                            row_data.append(participant_id)
                        elif column == "period":
                            row_data.append(random.randint(0, 3))
                        elif column == "site":
                            row_data.append(random.randint(0, 1))
                        elif column == "start_time":
                            row_data.append("07:30:00")
                        elif column == "end_time":
                            row_data.append("22:30:00")
                        else:
                            print("BIG ERROR: " + column)

                    else:
                        row_data.append("")

                else:  # TODO Optionen für moods, events, socials und activities
                    found = False
                    for field in moods:
                        if field in column:
                            found = True
                            break
                    for field in events:
                        if field in column:
                            found = True
                            break
                    for field in socials:
                        if field in column:
                            found = True
                            break
                    for field in activities:
                        if field in column:
                            found = True
                            break
                    if found:

                        if trigger_num == 0 and day == 0:
                            row_data.append("")
                        elif (Missing_entry == "Dismissed" or Missing_entry == "Ignored") and Form_entry == "Missing":
                            row_data.append("")
                        elif Missing_entry == "Incomplete" and Form_entry == "Missing":
                            if col_num <= num_cells_to_fill:
                                row_data.append(random.randint(1, 7))
                            else:
                                row_data.append("")
                        else:
                            row_data.append(random.randint(1, 7))
                    else:
                        print("BIG ERROR_DOWN :" + column)
            data.append(row_data)

# Erstelle DataFrame aus den generierten Daten
df = pd.DataFrame(data, columns=columns)

# Speichere die DataFrame in eine Excel-Datei
df.to_excel("DummyData.xlsx", index=False)
for loc in locations:
    for vis in visits:
        shutil.copy("DummyData.xlsx", "IMMERSE_" + vis + "_" + loc + ".xlsx")

print("Dummy-Daten wurden erfolgreich erstellt und gespeichert.")

