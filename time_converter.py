import datetime


def convert(time_input):

	if len(time_input) == 5:
		pattern = "%Mmin"
	else:
		pattern = "%Hh %Mmin"

	formatted = datetime.datetime.strptime(time_input, pattern).time()
	result = datetime.timedelta(hours=formatted.hour, minutes=formatted.minute)

	return result

print(convert("2h 30min"))
print(convert("58min"))
print(convert("2h 30min")+convert("58min"))
