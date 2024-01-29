import tkinter as tk
from tkinter import ttk
from tkinter import Entry
import yaml
import csv
import random
import string
from faker import Faker
import datetime
import math

# ADJUSTABLES
global empty_chance  # Describes the chance per entry, if it is empty for each single Choice or multiple Choice Answer
global PARTICIPANT_COUNT  # This number defines how many participants are generated
global number_of_entries  # Default Value of number of entries per participant


def create_dummy_files():
    PARTICIPANT_COUNT_entry = int(entry_participant_count.get())
    global PARTICIPANT_COUNT
    PARTICIPANT_COUNT = PARTICIPANT_COUNT_entry
    number_of_entries = int(entry_number_of_entries.get())
    global empty_chance
    empty_chance = float(entry_empty_chance.get())
    number = number_of_entries
    selected_enumerators = []
    participants = generate_participants_list()
    for i in range(0, num_formulas):
        checkbox_var = checkbox_vars[i]
        if checkbox_var.get():
            selected_enumerators.append(i)
    # print(selected_enumerators)
    if selected_enumerators:
        for enumerator in selected_enumerators:
            file_name = formula_names[enumerator]
            with open(file_name, 'w', newline='') as file:
                ecrf_entry = ecrf_entries[enumerator]
                items = ecrf_entry.get('items', {})
                writer = csv.writer(file, delimiter=';')
                # Column names
                column_names = [
                    'participant_identifier',
                    'center_name',
                    'created_at',
                    'started_at',
                    'finished_at',
                    'visit_name',
                    'diary_date'
                ]
                headlines = column_names
                for item_key in items:
                    item = items[item_key]
                    item_name = item.get('itemCode', '')
                    headlines.append(item_name)
                writer.writerow(headlines)  # Write the first line in the code as headlines
                # DONE: Generate your output data
                current_group = choose_participant_group(file_name)
                for participant in participants:
                    participant_group = participant['participant_kind']
                    if participant_group not in current_group:
                            continue
                    visit_names = generate_visit_name(file_name)
                    lines = entryforpatient(number,visit_names)
                    # print(participant)
                    participant_id = participant['participant_id']

                    for visit_name in lines:
                        started_at, finished_at = generate_Dates()
                        time_delta = datetime.timedelta(minutes=random.randint(4, 6))
                        created_at = started_at - time_delta
                        center_name = participant['center_name']

                        row = [participant_id, center_name, created_at.isoformat(), started_at.isoformat(),
                        finished_at.isoformat(), visit_name, '']

                        for item_key in items:
                            item = items[item_key]
                            item_data_type = item.get('itemDataType', '')  # Access itemDataType using get()
                            item_entry = generate_row_data(item_data_type, item.get('answers', {}))
                            #print("Item Entry")
                            #print(item_entry)
                            # print("Entry: ".join(str(item_entry)))
                            if isinstance(item_entry, int):
                                row.append(item_entry)
                            else:
                                row.extend(item_entry)
                        # print(row)
                        writer.writerow(row)
                #break point for testing
        message_label.config(text='Files created successfully!', fg='green')
    else:
        message_label.config(text='No file selected!', fg='red')


def entryforpatient(min_choices, possible_answers):
    lines = []
    if len(possible_answers)==1:
        return possible_answers
    lines.append(possible_answers[0])
    possible_answers.pop(0)
    if min_choices > len(possible_answers):
        num_choices = len(possible_answers)
    else:
        num_choices = random.randint(min_choices, len(possible_answers))
    chosen_answers = choose_unique_entries(possible_answers, num_choices)
    chosen_answers.sort() # Sort the answers chronologically
    lines.extend(chosen_answers)
    return lines

def choose_unique_entries(lst, num_choices):
    if num_choices > len(lst):
        return lst
    chosen_entries = random.sample(lst, num_choices)
    return chosen_entries

def generate_Dates():
    # Generate random start date
    start_date = datetime.datetime(2023, 1, 1) + datetime.timedelta(days=random.randint(1, 365))

    # Generate random time delta between 5 minutes and a few hours
    time_delta = datetime.timedelta(minutes=random.randint(5, 240))
    # Generate random time delta between 8 hours and nearly a day
    time_delta_2 = datetime.timedelta(minutes = random.randint(480,1000))
    # Calculate the end date by adding the time delta to the start date
    start_date= start_date + time_delta_2
    end_date = start_date + time_delta

    return start_date, end_date

def choose_participant_group(file_name):
    switch_dict = {
        "Adverse-Events-(Clinican-rating).csv": ['C'],
        "Adverse-Events-(Researcher-rating).csv": ['P'],
        "Adverse-Trial-effects.csv": ['P', 'C', 'T', 'F'],
        "AE_C_01.csv": ['P', 'C', 'T', 'F'],
        "End.csv":['P'],
        "Brief-Experiential-Avoidance-Questionnaire-(BEAQ).csv": ['P'],
        "Childhood-Trauma-Questionnaire-(CTQ).csv": ['P', 'C', 'T', 'F'],
        "Clinical-Global-Impression.csv": ['C'],
        "CSRI.csv": ['P', 'C', 'T', 'F'],
        "CSRI_BE.csv": ['P', 'C', 'T', 'F'],
        "CSRI_GE.csv": ['P', 'C', 'T', 'F'],
        "CSRI_SK.csv": ['P', 'C', 'T', 'F'],
        "Demographics-(Clinicians).csv": ['P', 'C', 'T', 'F'],
        "Demographics-(Patients).csv": ['P', 'C', 'T', 'F'],
        "Diagnosis.csv": ['P', 'C', 'T', 'F'],
        "Emotion-Regulation.csv": ['P', 'C', 'T', 'F'],
        "EQ-5D-5L_1.csv": ['P', 'C', 'T', 'F'],
        "EQ-5D-5L_2.csv": ['P', 'C', 'T', 'F'],
        "EQ-5D-5L_3.csv": ['P', 'C', 'T', 'F'],
        "EQ-5D-5L_4.csv":['P', 'C', 'T', 'F'],
        "EQ-5D-5L_5.csv": ['P', 'C', 'T', 'F'],
        "EQ-5D-5L_6.csv":['P', 'C', 'T', 'F'],
        "ESM-Debriefing.csv": ['P', 'C', 'T', 'F'],
        "Family-History.csv":['P'],
        "General-Health-Questionnaire-(GHQ).csv": ['P', 'C', 'T', 'F'],
        "Goal-Attainment-Scale.csv": ['P', 'C', 'T', 'F'],
        "Informed-consent.csv":['P', 'C', 'T', 'F'],
        "Kind-of-participant.csv": ['P', 'C', 'T', 'F'],
        "List-of-Threatening-Events-(LTE).csv": ['P', 'C', 'T', 'F'],
        "MANSA.csv": ['P', 'C', 'T', 'F'],
        "Mental-Health-self-management-questionnaire-(MHSEQ).csv": ['P', 'C', 'T', 'F'],
        "MTUAS.csv": ['P', 'C', 'T', 'F'],
        "New-clinican.csv": ['P', 'C', 'T', 'F'],
        "Options.csv": ['P'],
        "ORCA.csv": ['P', 'C', 'T', 'F'],
        "Questionnaire-on-Process-of-Recovery-(QPR).csv": ['P', 'C', 'T', 'F'],
        "Reflective-Functioning.csv": ['P', 'C', 'T', 'F'],
        "Revised-Green-Paranoid-Thought-Scale-(RGPTS).csv": ['P', 'C', 'T', 'F'],
        "Screening-Checklist.csv": ['P', 'C', 'T', 'F'],
        "SDMQ-(Clinician-rating).csv": ['P', 'C', 'T', 'F'],
        "SDMQ-(Patient-rating).csv": ['P', 'C', 'T', 'F'],
        "Self-injurious-Behavior-(T0).csv": ['P', 'C', 'T', 'F'],
        "Self-injurious-Behavior-(T1).csv": ['P', 'C', 'T', 'F'],
        "Self-injurious-Behavior-(T2).csv": ['P', 'C', 'T', 'F'],
        "Self-injurious-Behavior-(T3).csv": ['P', 'C', 'T', 'F'],
        "Service-Attachement-Questionnaire-(SAQ).csv": ['P', 'C', 'T', 'F'],
        "Service-characteristics.csv": ['P', 'C', 'T', 'F'],
        "Service characteristics (Finance).csv": ['P', 'C', 'T', 'F'],
        "Service characteristics (Teamleads).csv": ['P', 'C', 'T', 'F'],
        "Service-Engagement-Scale-(Clinician-rating).csv": ['P', 'C', 'T', 'F'],
        "Service Engagement Scale (Researcher rating).csv": ['P', 'C', 'T', 'F'],
        "Smartphone_Doc-ESM-Randomization.csv": ['P', 'C', 'T', 'F'],
        "Social-Functioning-Scale.csv": ['P'],
        "TAPS-Tool.csv": ['P', 'C', 'T', 'F'],
        "UCLA-Loneliness-Scale.csv": ['P', 'C', 'T', 'F'],
        "Working-Alliance-(Clinician-rating).csv": ['C'],
        "Working-Alliance-(Patient-rating).csv": ['P'],
    }
    if file_name in switch_dict:
        value = switch_dict[file_name]
        # Process the value or perform actions based on the file name
        return value
    else:
        print("File not found.")
        print (file_name)
        return "ERROR"

def generate_visit_name(file_name):
# Generate visite_names depending on the file name
    switch_dict = {
        "Adverse-Events-(Clinican-rating).csv": ["Baseline (clinician)", "T1 (2 months) (clinician)",
                                                 "T1 (2month)(2nd clinician)", "T2 (6 months) (clinician)",
                                                 "T2 (6month) (2nd clinician)", "T3 (12 months) (clinician)",
                                                 "T3 (12month) (2nd Clinician)"],
        "Adverse-Events-(Researcher-rating).csv": ["Baseline","T1 (2 months)", "T2 (6 months)",
                                                   "T3 (12 months)"],
        "Adverse-Trial-effects.csv": ["T1 (2 months) (patient)", "T2 (6 months) (patient)", "T3 (12 months) (patient)"],
        "AE_C_01.csv": ["Baseline (clinician)", "T1 (2 months) (clinician)", "T1 (2month)(2nd clinician)",
                        "T2 (6 months) (clinician)", "T2 (6month) (2nd clinician)", "T3 (12 months) (clinician)",
                        "T3 (12month) (2nd Clinician)"],
        "Brief-Experiential-Avoidance-Questionnaire-(BEAQ).csv": ["Enrolment (patient)"],
        "Childhood-Trauma-Questionnaire-(CTQ).csv": ["Baseline", "T1 (2 months)","T2 (6 months)","T3 (12 months)","Enrolment (patient)"],
        "Clinical-Global-Impression.csv": ["Baseline (clinician)", "T1 (2 months) (clinician)",
                                           "T2 (1month)(2nd clinician)", "T2 (6 months) (clinician)",
                                           "T2 (6month) (2nd clinician)", "T3 (12 months) (clinician)",
                                           "T3 (12month) (2nd Clinician)"],
        "CSRI.csv": ["Baseline (patient)", "T1 (patient) CSRI", "T1 (2 months) (patient)", "T2 (patient) CSRI",
                     "T2 (6 months) (patient)", "T3 (patient) CSRI", "T3 (12 months) (patient)"],
        "CSRI_BE.csv": ["Enrolment (patient) CSRI", "Baseline (patient)", "T1 (2 months) (patient)",
                        "T2 (6 months) (patient)", "T3 (12 months) (patient)"],
        "CSRI_GE.csv": ["Enrolment (patient) CSRI", "Baseline (patient)", "T1 (2 months) (patient)",
                        "T2 (6 months) (patient)", "T3 (12 months) (patient)"],
        "CSRI_SK.csv": ["Enrolment (patient) CSRI", "Baseline (patient)", "T1 (2 months) (patient)",
                        "T2 (6 months) (patient)", "T3 (12 months) (patient)"],
        "Demographics-(Clinicians).csv": ["Enrolment (Clinician)"],
        "Demographics-(Patients).csv": ["Enrolment (patient)"],
        "Diagnosis.csv": ["Screening", "Baseline (clinician)", "T1 (2 months) (clinician)", "T1 (2month)(2nd clinician)",
                          "T2 (6 months) (clinician)", "T2 (6month) (2nd clinician)", "T3 (12 months) (clinician)",
                          "T3 (12month) (2nd Clinician)"],
        "Emotion-Regulation.csv": ["Baseline (patient)", "T1 (2 months) (patient)", "T2 (6 months) (patient)",
                                   "T3 (12 months) (patient)"],
        "EQ-5D-5L_1.csv": ["Baseline (patient)", "T1 (2 months) (patient)", "T2 (6 months) (patient)",
                           "T3 (12 months) (patient)"],
        "EQ-5D-5L_2.csv": ["Baseline (patient)", "T1 (2 months) (patient)", "T2 (6 months) (patient)",
                           "T3 (12 months) (patient)"],
        "EQ-5D-5L_3.csv": ["Baseline (patient)", "T1 (2 months) (patient)", "T2 (6 months) (patient)",
                           "T3 (12 months) (patient)"],
        "EQ-5D-5L_4.csv": ["Baseline (patient)", "T1 (2 months) (patient)", "T2 (6 months) (patient)",
                           "T3 (12 months) (patient)"],
        "EQ-5D-5L_5.csv": ["Baseline (patient)", "T1 (2 months) (patient)", "T2 (6 months) (patient)",
                           "T3 (12 months) (patient)"],
        "EQ-5D-5L_6.csv": ["Baseline (patient)", "T1 (2 months) (patient)", "T2 (6 months) (patient)",
                           "T3 (12 months) (patient)"],
        "ESM-Debriefing.csv": ["ESM Baseline", "ESM T1", "ESM T2", "ESM T3"],
        "Family-History.csv": ["Enrolment (patient)"],
        "End.csv":["Screening"],
        "Family-History.csv":["Enrolment (patient)"],
        "General-Health-Questionnaire-(GHQ).csv": ["Baseline (patient)", "T1 (2 months) (patient)",
                                                   "T2 (6 months) (patient)", "T3 (12 months) (patient)"],
        "Goal-Attainment-Scale.csv": ["Baseline (patient)", "T1 (2 months) (patient)", "T2 (6 months) (patient)",
                                      "T3 (12 months) (patient)"],
        "Informed-consent.csv": ["Screening"],
        "Kind-of-participant.csv": ["Screening"],
        "List-of-Threatening-Events-(LTE).csv": ["Enrolment (patient)"],
        "MANSA.csv": ["Baseline (patient)", "T1 (2 months) (patient)", "T2 (6 months) (patient)",
                      "T3 (12 months) (patient)"],
        "Mental-Health-self-management-questionnaire-(MHSEQ).csv": ["Baseline (patient)", "T1 (2 months) (patient)",
                                                                    "T2 (6 months) (patient)",
                                                                    "T3 (12 months) (patient)"],
        "MTUAS.csv": ["Enrolment (Clinician)"],
        "New-clinican.csv": ["Screening"],
        "Options.csv": ["Enrolment (patient)"],
        "ORCA.csv": ["Baseline (team lead)"],
        "Questionnaire-on-Process-of-Recovery-(QPR).csv": ["Baseline (patient)", "T1 (2 months) (patient)",
                                                           "T2 (6 months) (patient)", "T3 (12 months) (patient)"],
        "Reflective-Functioning.csv": ["Baseline (patient)", "T1 (2 months) (patient)", "T2 (6 months) (patient)",
                                       "T3 (12 months) (patient)"],
        "Revised-Green-Paranoid-Thought-Scale-(RGPTS).csv": ["Baseline (patient)", "T1 (2 months) (patient)",
                                                             "T2 (6 months) (patient)", "T3 (12 months) (patient)"],
        "Screening-Checklist.csv": ["Baseline","T1 (2 months)", "T2 (6 months)",
                                                   "T3 (12 months)"],
        "SDMQ-(Clinician-rating).csv": ["Baseline (clinician)", "T1 (2 months) (clinician)",
                                        "T1 (2month)(2nd clinician)", "T2 (6 months) (clinician)",
                                        "T2 (6month) (2nd clinician)", "T3 (12 months) (clinician)",
                                        "T3 (12month) (2nd Clinician)"],
        "SDMQ-(Patient-rating).csv": ["Baseline (patient)", "T1 (2 months) (patient)", "T2 (6 months) (patient)",
                                      "T3 (12 months) (patient)"],
        "Self-injurious-Behavior-(T0).csv": ["Enrolment (patient)"],
        "Self-injurious-Behavior-(T1).csv": ["T1 (2 months)"],
        "Self-injurious-Behavior-(T2).csv": ["T2 (6 months)"],
        "Self-injurious-Behavior-(T3).csv": ["T3 (12 months)"],
        "Service-Attachement-Questionnaire-(SAQ).csv": ["Baseline (patient)", "T1 (2 months) (patient)",
                                                        "T2 (6 months) (patient)", "T3 (12 months) (patient)"],
        "Service-characteristics.csv": ["Baseline (team lead)"],
        "Service characteristics (Finance).csv": ["Baseline (finance staff)"],
        "Service characteristics (Teamleads).csv": ["Baseline (team lead)"],
        "Service-Engagement-Scale-(Clinician-rating).csv": ["Baseline (clinician)", "T1 (2 months) (clinician)",
                                                            "T1 (2month)(2nd clinician)", "T2 (6 months) (clinician)",
                                                            "T2 (6month) (2nd clinician)", "T3 (12 months) (clinician)",
                                                            "T3 (12month) (2nd Clinician)"],
        "Service Engagement Scale (Researcher rating).csv": [""],
        "Smartphone_Doc-ESM-Randomization.csv": ["Baseline", "T1 (2 months)", "T2 (6 months)", "T3 (12 months)"],
        "Social-Functioning-Scale.csv": ["Baseline (patient)", "T1 (2 months) (patient)", "T2 (6 months) (patient)",
                                         "T3 (12 months) (patient)"],
        "TAPS-Tool.csv": ["Enrolment (patient)"],
        "UCLA-Loneliness-Scale.csv": ["Baseline (patient)", "T1 (2 months) (patient)", "T2 (6 months) (patient)",
                                      "T3 (12 months) (patient)"],
        "Working-Alliance-(Clinician-rating).csv": ["Baseline (clinician)", "T1 (2 months) (clinician)",
                                                    "T1 (2month)(2nd clinician)", "T2 (6 months) (clinician)",
                                                    "T2 (6month) (2nd clinician)", "T3 (12 months) (clinician)",
                                                    "T3 (12month) (2nd Clinician)"],
        "Working-Alliance-(Patient-rating).csv": ["Baseline (patient)", "T1 (2 months) (patient)",
                                                  "T2 (6 months) (patient)", "T3 (12 months) (patient)"],
    }

    if file_name in switch_dict:
        value = switch_dict[file_name]
        if "T1 (2month)(2nd clinician)" in value:
            value = random.choice([["Baseline (clinician)", "T1 (2 months) (clinician)", "T2 (6 months) (clinician)","T3 (12 months) (clinician)"],["Baseline (clinician)", "T1 (2month)(2nd clinician)","T2 (6month) (2nd clinician)","T3 (12month) (2nd Clinician)"]])
        # Process the value or perform actions based on the file name
        return value
    else:
        print("File not found.")
        return "ERROR"


# Example usage:

def generate_participants_list():
# Returns a list of random participantIDs

    participants = []
    for _ in range(PARTICIPANT_COUNT):
        participant_id, participant_kind = generate_unique_id()
        center_name = identify_center_name(participant_id)
        # Append the generated participant information
        participants.append({
            'participant_id': participant_id,
            'center_name': center_name,
            'participant_kind': participant_kind
        })
    # Generate a file with participants
    file_name = 'participants.csv'
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Participant ID', 'center_name','participant_kind'])

        for participant in participants:
            participant_id = participant['participant_id']
            center_name = participant['center_name']
            participant_kind = participant['participant_kind']
            writer.writerow([participant_id, center_name,participant_kind])
    
    return participants


def generate_unique_id():
    # Generate a unique ID in the form I_[centerName]_[ParticipantKind]_[nummer]

    center_name_options = ['LO', 'CA', 'MA', 'WI', 'LE', 'BI', 'BR', 'KO']
    participant_kind_options = ['P', 'C', 'T', 'F']
    # Generate a random number between 1 and 999 and zero-pad it to 3 digits
    number = str(random.randint(1, 999)).zfill(3) 
    # Random choice of centre_name
    center_name = random.choice(center_name_options)
    # Random choice of participant_kind
    participant_kind = random.choice(participant_kind_options)

    participant_id = f"I-{center_name}-{participant_kind}-{number}"

    return participant_id, participant_kind


def identify_center_name(participant_id):
    # identify center name based on participant_id

    center_name = ""

    if "LO" in participant_id or "CA" in participant_id:
        center_name = "Lothian"
    elif "MA" in participant_id:
        center_name = "Mannheim"
    elif "WI" in participant_id:
        center_name = "Wiesloch"
    elif "LE" in participant_id:
        center_name = "Leuven"
    elif "BI" in participant_id:
        center_name = "Bierbeek"
    elif "BR" in participant_id:
        center_name = "Bratislava"
    elif "KO" in participant_id:
        center_name = "Kosice"

    return center_name



def generate_row_data(item_data_type, answers):
    # Generate row data based on itemDataType
    # Add a case for each possible itemDataType

    if item_data_type == 'date':
        random_date = generate_random_date()  # Generate a random date within the current year
        row = [random_date.strftime('%d.%m.%Y')]  # Example: Add the formatted date to the row
    elif item_data_type == 'number':
        row = generate_random_number()
    elif item_data_type == 'text':
        # TODO: Handle Text itemDataType
        row = generate_text_entry()
    elif item_data_type == 'singleChoice':
        # TODO: Handle SingleChoice itemDataType
        # print(item_data_type)
        answer_codes = list(answers.keys())  # Get the list of answer codes
        # print(answer_codes)
        if answer_codes:
            # random_answer_code = random.choice(answer_codes)  # Select a random answer code
            # random_answer = answers[random_answer_code]['answerText']  # Retrieve the corresponding answer
            choosen = choose_single_choice_answer(answer_codes)
            # print(choosen)
            row = [choosen]
        else:
            row = ["single Choice without Choice options"]
    elif item_data_type == 'multipleChoice':
        # TODO: Handle multipleChoice itemDataType
        # row = generate_random_multiple_choice(answers)
        answer_codes = list(answers.keys())
        row = choose_single_choice_answer(answer_codes)
    else:
        # Unknown itemDataType
        row = ["Else Case", item_data_type]
    return row


def choose_single_choice_answer(answer_possibilities):
    if random.random() < empty_chance:
        return " "  # Return an empty result based on the empty_chance probability
    else:
        chosen_answer = random.choice(answer_possibilities)
        return chosen_answer


def generate_random_multiple_choice(answers):
    answer_codes = list(answers.keys())  # Get the list of answer codes

    num_choices = random.randint(0, len(answer_codes))
    # print(num_choices)
    random_choices = random.sample(answer_codes, num_choices)
    returning_values = []
    saver = [float('nan')]
    for choice in random_choices:
        returning_values.append(answers.get(choice, '').get('answerCode', ''))
    if returning_values == []:
        returning_values = saver

    elif math.isnan(returning_values[0]):
        returning_values = [1]
    return [returning_values]


def generate_random_number():
    return [random.randint(1, 179573829)]


def generate_text_entry():
    return ["SampleTextEntry"]


def generate_random_date():
    year = datetime.datetime.now().year  # Get the current year
    start_date = datetime.datetime(year, 1, 1)  # Set the start date to January 1st of the current year
    end_date = datetime.datetime(year, 12, 31)  # Set the end date to December 31st of the current year
    random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date


# Read the codebook YAML file
with open("codebook.yaml") as yaml_file:
    codebook = yaml.load(yaml_file, Loader=yaml.FullLoader)
    # print(codebook)
    ecrfs = codebook.get('eCRFs', [])
    # print(ecrfs)
    formula_names = []
    ecrf_entries = []
    for entry in ecrfs:
        ecrf_entry = ecrfs.get(entry)
        ecrf_entries.append(ecrf_entry)
        # print(ecrf_entry)
        ecrf_name = ecrf_entry.get('ecrfFilename')
        # print(ecrf_name)
        formula_names.append(ecrf_name)

# Create the main window
window = tk.Tk()
window.title("Dummy File Creator")

# Set the window size based on the number of formulas
num_formulas = len(formula_names)
rows = (num_formulas - 1) // 4 + 1
window_width = 1800
window_height = rows * 30 + 150
window.geometry(f"{window_width}x{window_height}")

# Configure the style
style = ttk.Style(window)
style.configure("TButton", padding=6, relief="flat")
style.configure("TCheckbutton", padding=5, relief="flat", background="#f0f0f0")

# Create a canvas with scrollbars
canvas = tk.Canvas(window)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a frame inside the canvas
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor=tk.NW)

# Create the checkboxes
checkbox_vars = {}
row = 0
column = 0
for i in range(0, num_formulas):
    checkbox_vars[i] = tk.IntVar(value=1)
    enumerator = tk.Label(frame, text=f'{i}.', font='Arial 10', width=2, anchor=tk.W)
    enumerator.grid(row=row, column=column, sticky="w")
    checkbox = ttk.Checkbutton(frame, text=formula_names[i], variable=checkbox_vars[i], style="TCheckbutton")
    checkbox.grid(row=row, column=column, sticky="w")
    column += 1
    if column >= 3:
        column = 0
        row += 1

# Create the button
create_button = ttk.Button(window, text="Create Files", command=create_dummy_files, style="TButton")
create_button.pack(side=tk.BOTTOM, pady=10)

# Create the label to display messages
message_label = tk.Label(window, text='')
message_label.pack()

# Create an entry field
entry_label = tk.Label(window, text="Number of participants:")
entry_participant_count = Entry(window)
entry_participant_count.insert("end", 56)
entry_label.pack()
entry_participant_count.pack()

# Create an entry field
entry_label = tk.Label(window, text="Number of  minimum entries per participant (Atleast 1):")
entry_number_of_entries = Entry(window)
entry_number_of_entries.insert("end", 1)
entry_label.pack()
entry_number_of_entries.pack()

# Create an entry field
entry_label = tk.Label(window, text="Chance that a single or multiple Choice field is empty (0 to 1):")
entry_empty_chance = Entry(window)
entry_empty_chance.insert("end", "0.2")  # Set the default value as "0.2"
entry_label.pack()
entry_empty_chance.pack()
# Configure the canvas scrolling
canvas.configure(scrollregion=canvas.bbox("all"))

# Run the main event loop
window.mainloop()
