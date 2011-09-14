def pretty_date(time=False):
	"""
	Get a datetime object or a int() Epoch timestamp and return a
	pretty string like 'an hour ago', 'Yesterday', '3 months ago',
	'just now', etc
	"""
	
	from datetime import datetime
	now = datetime.now()
	if type(time) is int:
		diff = now - datetime.fromtimestamp(time)
	elif isinstance(time,datetime):
		diff = now - time 
	elif not time:
		diff = now - now
	second_diff = diff.seconds
	day_diff = diff.days

	if day_diff < 0:
		return ''

	if day_diff == 0:
		if second_diff < 10:
			return "just now"
		if second_diff < 60:
			return str(second_diff) + " seconds ago"
		if second_diff < 120:
			return  "1 minute ago"
		if second_diff < 3600:
			return str( second_diff / 60 ) + " minutes ago"
		if second_diff < 7200:
			return "1 hour ago"
		if second_diff < 86400:
			return str( second_diff / 3600 ) + " hours ago"
		if day_diff == 1:
			return "Yesterday"
			
	months=["January", "February", "March",
	"April", "May", "June", "July",
	"August", "September", "October", "November", "December"]
	if time.year==now.year:
		return months[time.month-1]+" "+str(time.day)
	else:
		return months[time.month-1]+" "+str(time.day)+", "+str(time.year)
"""
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
	num=day_diff/7
	if num==1:
		return "one week ago"
	else:
	    return str(num) + " weeks ago"
    if day_diff < 365:
	num=day_diff/30
	if num==1:
		return "one month ago"
	else:
		return str(num) + " months ago"
    if day_diff < 730:
	return "a year ago"
    return str(day_diff/365) + " years ago"
"""
