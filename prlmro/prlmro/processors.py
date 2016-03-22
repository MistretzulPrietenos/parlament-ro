import string
import time, re
from w3lib.html import remove_tags


RO_DATE_DICT = dict([(' ',''),('n.',''),
			   ('ian.', '/01/'),
			   ('feb.', '/02/'),
			   ('mar.', '/03/'),
			   ('apr.', '/04/'),
			   ('mai' , '/05/'),
			   ('iun.', '/06/'),
			   ('iul.', '/07/'),
			   ('aug.', '/08/'),
			   ('sep.', '/09/'),
			   ('oct.', '/10/'),
			   ('noi.', '/11/'),
			   ('dec.',  '/12/'),
			   ('ianuarie', '/01/'),
			   ('februarie', '/02/'),
			   ('martie', '/03/'),
			   ('aprilie', '/04/'),
			   ('iunie', '/06/'),
			   ('iulie', '/07/'),
			   ('august', '/08/'),
			   ('septembrie', '/09/'),
			   ('octombrie', '/10/'),
			   ('noiembrie', '/11/'),
			   ('decembrie',  '/12/'),
			   ])


pattern = re.compile('|'.join(re.escape(key) for key in RO_DATE_DICT.keys()))


class ParseDate(object):

	def to_date(self, str):
		return pattern.sub(lambda x: RO_DATE_DICT[x.group()], str)
		

	def __call__(self, values):
		date = None
		if len(values) > 1:
			date = self.to_date(values[1])
		elif len(values) == 1:
			date = self.to_date(values[0])
		return date



class ParseName(object):
	
	def __init__(self, separator=u'<br>'):
		self.separator = separator

	def __call__(self, values):
		name = None
		if len(values) > 1:
			name = values[0].strip()
		return name
