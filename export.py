from icalendar import Calendar, Event
from datetime import datetime
import pytz
import tempfile, os
from re import search, findall, S, I, M
import time
import datetime as dt
from pdb import set_trace

workouts = []
with open('workouts.txt', 'r') as f:
    text = f.read()

print text
daily_workout_match = findall(r'-------(\s*\w.*?)---', text, flags=S|I|M)

if not daily_workout_match:
  raise Exception('Could not find daily_workout_match!')

for daily_workout in daily_workout_match:
  daily_workout = daily_workout + "end"
  match = search(r'(\w+)\s(\w+)\s(\d+)\s(\d{4})\s*(.*)end', daily_workout, flags=S|I|M)
  if not match:
    raise Exception('Could not find match!')

  workout = match.group(5)

  if len(workout) < 20:
    if not search(r'Rest', workout, flags=S|I|M):
      raise Exception('This workout seems short on content...\n %s' % workout)

  workouts.append(workout)

current_date = datetime.now()
t1 = current_date.timetuple()
seconds = time.mktime(t1) + 86400.0

days_until_start = float(raw_input("How many days before your regiment starts? Please enter a number from 1 - 10: "))
date_to_start = datetime.utcfromtimestamp(seconds + days_until_start * 10000).date()

cal = Calendar()
workout_counter = 0
date = date_to_start

for workout in workouts:
  event = Event()
  date_start = date + dt.timedelta(days=workout_counter)
  date_end = date_start + dt.timedelta(hours=2)
  event.add('dtstart', date_start)
  event.add('dtend', date_end)
  event['summary'] = "Workout"
  event['description'] = workout
  workout_counter += 1
  cal.add_component(event)

directory = '/Users/BtLutz/Documents/WODCalendar/Calendars/'
f = open(os.path.join(directory, 'Catalyst Workouts.ics'), 'wb')
f.write(cal.to_ical())
set_trace()
f.close()
