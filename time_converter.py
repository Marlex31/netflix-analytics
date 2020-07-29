import datetime

class watchTime(object):
	"""docstring for watchTime"""

	def __init__(self, time_input):
		super(watchTime, self).__init__()
		
		self.time_input = time_input
		self.convert(self.time_input)

	def convert(self, time_input):

		if len(self.time_input) == 5:
			pattern = "%Mmin"
		else:
			pattern = "%Hh %Mmin"

		formatted = datetime.datetime.strptime(self.time_input, pattern).time()
		self.total = datetime.timedelta(hours=formatted.hour, minutes=formatted.minute)



show_1 = watchTime("2h 30min")
show_2 =  watchTime("58min")

print(show_1.total + show_2.total)