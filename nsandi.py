# coding=UTF-8
import urllib
import urllib2
import argparse
import re
import datetime

# I got fed up with tapping these out on the web form every month for the index-linked certs.
# So reverse-engineered the form submission and ended up with this simple script. 
# It seems like it could be extended to other products with the manipulation of productID.

# TODO: productid is always 55 with index-linked certs - could this be extended to other products?
parser = argparse.ArgumentParser(description='Get latest NS&I index-linked certs')
parser.add_argument('--amount', nargs=1, help='amount of investment in pounds, eg 1000', type=int, required=True)
parser.add_argument('--year', nargs=1, help='year of purchase, eg 2001', type=int, required=True)
parser.add_argument('--month', nargs=1, help='month of purchase, eg 1 (for January) or 12 for December', type=int, required=True)
parser.add_argument('--day', nargs=1, help='day of purchase, eg 1, 2, 30', type=int, required=True)
parser.add_argument('--term', nargs=1, help='term of investment in months',type=int, required=True)

args = parser.parse_args()

# Constants
product_id = 55
# The form submission has two stages on the real page (validation, and real); we skip the first and assume the validation is correct.
url = 'http://www.nsandi.com/ilsc/calculation'
today      = datetime.date.today()
# TODO: format to remove leading zeroes
today_formatted = today.strftime("%d/%m/%Y")

amount     = str(args.amount[0])
term       = str(args.term[0])
day        = str(args.day[0])
month      = str(args.month[0])
year       = str(args.year[0])

values = {'invest_amnt' : amount, 'selectTerm' : term, 'selectDay' : day, 'selectMonth' : month, 'investYear' : year, 'productID' : product_id}

# We need to urlencode.
data = urllib.urlencode(values)
# Set up request object.
req = urllib2.Request(url,data)
# Make request.
response = urllib2.urlopen(req)
# Get 'page' content.
the_page = response.read()

# Get money.
pattern = re.compile("pound;([^ ]*)")
match_obj = re.search(pattern,the_page)

# Print message.
print "As of: " + today_formatted + " the value of your investment of £" + amount + " purchased on " + day + "/" + month + "/" + year + " is now: £" + match_obj.group(1)
