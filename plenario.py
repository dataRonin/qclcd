import requests
import json
import datetime
import dateutil.parser
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

class Plenario:

	def __init__(self, url):
	""" See below for example URLs from Nashville, TN"""
		r = requests.get(url)

		if r.status_code == 200 or r.status_code == '200':
			response = r.text
			response = json.loads(r.text)
		else:
			response = {}

		self.data = response
		self.meta = {}
		self.this = {}
		self.sky = {}
		self.wthr = {}
		self.attribute=' temperature'


	def getDryBulbFahrenheit(self):
		a = {x['datetime']:x['drybulb_fahrenheit'] for x in self.data['objects'][0]['observations']}
		dts = {dateutil.parser.parse(x): a[x] for x in a.keys()}
		self.this = dts
		return dts

	def getPrecip(self):
		a = {x['datetime']:x['hourly_precip'] for x in self.data['objects'][0]['observations']}
		dts = {dateutil.parser.parse(x): a[x] for x in a.keys()}
		self.this = dts
		return dts

	def getWindSpeed(self):
		a = {x['datetime']:x['wind_speed'] for x in self.data['objects'][0]['observations']}
		dts = {dateutil.parser.parse(x): a[x] for x in a.keys()}
		self.this = dts
		return dts

	def getWindDirection(self):
		a = {x['datetime']:x['wind_direction'] for x in self.data['objects'][0]['observations']}
		dts = {dateutil.parser.parse(x): a[x] for x in a.keys()}
		self.this = dts
		return dts

	def getPressure(self):
		a = {x['datetime']:x['sealevel_pressure'] for x in self.data['objects'][0]['observations']}
		dts = {dateutil.parser.parse(x): a[x] for x in a.keys()}
		self.this = dts
		return dts

	def getWetBulbFahrenheit(self):
		a = {x['datetime']:x['wetbulb_fahrenheit'] for x in self.data['objects'][0]['observations']}
		dts = {dateutil.parser.parse(x): a[x] for x in a.keys()}
		self.this = dts
		return dts

	def getSkyCondition(self):
		a = {x['datetime']:x['sky_condition'] for x in self.data['objects'][0]['observations']}
		dts = {dateutil.parser.parse(x): a[x] for x in a.keys()}
		self.sky = dts
		return dts

	def getWeatherCondition(self):
		a = {x['datetime']:x['weather_types'] for x in self.data['objects'][0]['observations']}
		dts = {dateutil.parser.parse(x): a[x] for x in a.keys()}
		self.wthr = dts
		return dts

	def stationInfo(self):
		self.meta = self.data['objects'][0]['station_info']
		return self.data['objects'][0]['station_info']


class Semivariogram:
  """ Note, this section IS NOT complete. Please fill in with a correct semivariogram if needed. Still testing various distance metrics."""
	def __init__(self, PlenarioObjs):
    
		self.datasets = PlenarioObjs
		self.this = {'lags': [], 'diffs': [], 'var': [], 'raw': [], 'dts': []}
		# defaults to the attribute of the first object
		self.attribute = PlenarioObjs[0].attribute
	
	def lags(self):
		""" compute all the lag distances"""
		ordered = []

		# each individual data set
		for eachitem in self.datasets:
			minkey = min(eachitem.this.keys())

			for eachday in eachitem.this.keys():
				diffkey = eachday - minkey

				ordered.append((diffkey, eachitem.this[eachday]))

		ordered = sorted(ordered, key=lambda x:x[0])
		# difference between subsequent values
		diff = [t - s for s, t in zip([x[1] for x in ordered], [x[1] for x in ordered[1:]])]
		self.this['lags'] = [x[0] for x in ordered][1:]
		self.this['diffs'] = diff
		self.this['var'] = [np.power(np.power(x,2),0.5) for x in diff]
		self.this['raw'] = [x[1] for x in ordered][1:]
		self.this['dts'] = [x[0] for x in ordered][1:]
		return self.this['lags'], self.this['diffs'], self.this['var'], self.this['raw'], self.this['dts']

	def plotLags(self):

		if self.this['lags'] == []:
			return
		else:
			# number of days
			dates = [x.total_seconds()/86164. for x in self.this['lags']]
			values = self.this['raw']
			fig, ax = plt.subplots()
			ax.scatter(dates, values)
			ax.set_xlabel('lag time (days)')
			ax.set_ylabel('normalized difference in' + self.attribute)
			plt.show()

	def getLagsAsDates(self):
		return [x.total_seconds()/86164. for x in self.this['lags']]


if __name__ == "__main__":

	AS2014 = Plenario('http://plenar.io/v1/api/weather/hourly/?wban_code=13897&datetime__ge=2014-08-14&datetime__le=2014-09-14')
	SO2014 = Plenario('http://plenar.io/v1/api/weather/hourly/?wban_code=13897&datetime__ge=2014-09-14&datetime__le=2014-10-14')
	ON2014 = Plenario('http://plenar.io/v1/api/weather/hourly/?wban_code=13897&datetime__ge=2014-10-14&datetime__le=2014-11-14')

	ND2014 = Plenario('http://plenar.io/v1/api/weather/hourly/?wban_code=13897&datetime__ge=2014-11-14&datetime__le=2014-12-14')
	DJ2015 = Plenario('http://plenar.io/v1/api/weather/hourly/?wban_code=13897&datetime__ge=2014-12-14&datetime__le=2015-01-14')
	JF2015 = Plenario('http://plenar.io/v1/api/weather/hourly/?wban_code=13897&datetime__ge=2015-01-14&datetime__le=2015-02-14')

	FM2015 = Plenario('http://plenar.io/v1/api/weather/hourly/?wban_code=13897&datetime__ge=2015-02-14&datetime__le=2015-03-14')
	MA2015 = Plenario('http://plenar.io/v1/api/weather/hourly/?wban_code=13897&datetime__ge=2015-03-14&datetime__le=2015-04-14')
	AM2015 = Plenario('http://plenar.io/v1/api/weather/hourly/?wban_code=13897&datetime__ge=2015-04-14&datetime__le=2015-05-14')

	MJ2015 = Plenario('http://plenar.io/v1/api/weather/hourly/?wban_code=13897&datetime__ge=2015-05-14&datetime__le=2015-06-14')
	JJ2015 = Plenario('http://plenar.io/v1/api/weather/hourly/?wban_code=13897&datetime__ge=2015-06-14&datetime__le=2015-07-14')
	JA2015 = Plenario('http://plenar.io/v1/api/weather/hourly/?wban_code=13897&datetime__ge=2015-07-14&datetime__le=2015-08-14')

	AS2014.getDryBulbFahrenheit()
	SO2014.getDryBulbFahrenheit()
	ON2014.getDryBulbFahrenheit()

	ND2014.getDryBulbFahrenheit()
	DJ2015.getDryBulbFahrenheit()
	JF2015.getDryBulbFahrenheit()

	MJ2015.getDryBulbFahrenheit()
	JJ2015.getDryBulbFahrenheit()
	JA2015.getDryBulbFahrenheit()

	FM2015.getDryBulbFahrenheit()
	MA2015.getDryBulbFahrenheit()
	AM2015.getDryBulbFahrenheit()

  """ THESE SEMIVARIOGRAMS ARE NOT TECHNICALLY SEMIVARIOGRAMS. THEY ARE WHAT I NEEDED FOR A PARTICULAR ANALYSIS. PLEASE USE A CORRECT SEMIVARIOGRAM IF YOU NEED IT!"""

	FALL = Semivariogram([AS2014, SO2014, ON2014])
	FALL.lags()
	FALL.plotLags()

	WINTER = Semivariogram([ND2014, DJ2015, JF2015])
	WINTER.lags()
	WINTER.plotLags()

	SPRING = Semivariogram([FM2015, MA2015, AM2015])
	SPRING.lags()
	SPRING.plotLags()

	SUMMER = Semivariogram([MJ2015, JJ2015, JA2015])
	SUMMER.lags()
	SUMMER.plotLags()
