# Couch to 5 Kilometers (C25k) running assistant
# http://www.tombenninger.com/files/2011/09/VisualC25K.v1_0b.png

import json
import random
import datetime
import time
import threading
import sys
from threading import Timer
import re

class NewThread:
    id = 0
    idStop = False
    next_interval = 0
    idThread = threading.Thread

# Declare Variables
workout_mode = NewThread
interval_postion = 0
progress_week = 1
progress_day = 1


def load_file(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data



def get_workout_details(json_data, week_num, day_num):
    this_week = json_data["weeks"][week_num-1]
    this_day = this_week["day"][day_num-1]
    workout_duration = 0
    interval_count = len(this_day["intervals"]) - 2
    print(this_day)
    for each_interval in this_day["intervals"]:
        for interval_type in each_interval:
            workout_duration = workout_duration + each_interval[interval_type]
    workout_duration = int(workout_duration / 60)  # minutes
    print('Weeks: ' + str(len(json_data["weeks"])))

def set_next_interval_notice(this_interval_json, next_interval_json):
    for key in this_interval_json:
        this_key = key
        this_durration = this_interval_json[key]
    for key in next_interval_json:
        next_key = key
        next_durration = next_interval_json[key]
    Timer(this_durration-7, announce_next_interval, [next_key]).start()
    print(this_durration)
    print(datetime.datetime.now())


def announce_next_interval(interval_name):
    print(datetime.datetime.now())
    print("The next interval, " + interval_name + ", will begin in 7 seconds")

def call_motivation():
    motivate_file = open('motivator.lst', 'r')
    motivate_list = motivate_file.readlines()
    motivate_file.close()
    motivate = random.choice(motivate_list)
    print(motivate)


def create_random_sorted_list(num, start=1, end=100):
    arr = []
    tmp = random.randint(start, end)
    for x in range(num):
        while tmp in arr:
            tmp = random.randint(start, end)
        arr.append(tmp)
    arr.sort()
    return arr


def set_motivational_events(interval_time):
        print(create_random_sorted_list(4, 1, interval_time-7))


def end_of_interval():
    global interval_postion
    print('Interval Completed!')
    interval_postion += 1


def end_of_workout():
    print('Workout Ended!')
    # Todo workout completed housekeeping
    halt_workout_thread()


def countdown_sound(counts):  # this routine will play a notification countdown for x(counts) seconds
    for i in range(1, counts):
        print(str(i) + ' beep')
        time.sleep(1)
    print('beeeeeep')


def init_workout_thread():  # creates the workout thread
    workout_mode.idStop = False
    workout_mode.id = 101
    workout_mode.idThread = threading.Thread(target=do_workout_thread,
                                             args=(workout_mode.id,
                                                   lambda: workout_mode.idStop))
    workout_mode.idThread.start()


def do_workout_thread(my_id, terminate):  # This is an independant thread handling the workout
    print("Starting Workout with ID: " + str(my_id))
    active_schedule = load_file("schedule.json")
    this_week = active_schedule["weeks"][progress_week-1]

    this_day = this_week["day"][progress_day-1]
    all_intervals = this_day["intervals"]
    last_interval = len(all_intervals)
    print('Last Interval = ' + str(last_interval))
    interval_list = enumerate(all_intervals)
    try:
        for idex, value in interval_list:
            this_interval = json.dumps(all_intervals[idex])
            for key in all_intervals[idex]:
                this_durration = all_intervals[idex][key]
            print(this_durration)
            print("Workout underway at step: " + str(idex) + ", " + this_interval)
            notification_threads = []  #reset nofiication threads
            if idex == (last_interval - 1):  # Check for the last interval
                # Todo add Last interval threads here
                notification_threads.append(Timer(this_durration, end_of_workout))
                print('Last Interval workout almost completed!')
            else:
                # Todo add motivation threads here
                notification_threads.append(Timer(this_durration, end_of_interval))
            for each_thread in notification_threads:
                each_thread.start()
            print("waiting!")
            while (idex == interval_postion) and not terminate():  # wait while this interval completes
                dummyValue = 1
            if terminate():
                for each_thread in notification_threads:
                    each_thread.cancel()
                if idex != (last_interval - 1):
                    print('Workout has been terminated!')
                else:
                    print('Workout has been Completed!')
                break
        # Todo add workout canceled housekeeping here
    except Exception as e:
        print(Exception)# if there is an error attempting the workout then here....


def halt_workout_thread():  # requests an end to the workout
    workout_mode.id = 101
    workout_mode.idStop = True
    workout_mode.idThread.join()

def count_weeks():
    len(this_day["Intervals"])

def regex_test(mystring):
    voice_payload = str(mystring)
    matches = re.search(r'(?P<weeks>week \d+)', voice_payload)
    if matches:
        utt_week = re.findall("\d+", matches.group('weeks'))[0]
        print("Caught week: " + str(utt_week))
    else:
        print("no matches found")
    matches = re.search(r'(?P<days>day \d+)', voice_payload)
    if matches:
        utt_day = re.findall("\d+", matches.group('days'))[0]
        print("Caught day: " + str(utt_day))
    else:
        print("no matches found")

regex_test("change my workout")
# init_workout_thread()
# time.sleep(14)
# halt_workout_thread()
# countdown_sound(6)
# set_next_interval_notice(json.loads('{"Run": 60}'), json.loads('{"Cool-Down": 300}'))
# get_workout_details(load_file("schedule.json"), 1, 1)
# do_workout(load_file("schedule.json"), 6, 2)
# call_motivation()
# Timer(5, end_of_interval, ()).start()
