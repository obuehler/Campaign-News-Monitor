_author = "Owen Buehler"
""" I've added a bunch of comments to ease code and syntax
comprehension """

import re
import urllib
import smtplib

# Class in puthon
class Spider():
    def __init__(self, site):
        self.site = site
        
    
    def phpsearch(self, query):
        """Tries to execute a PHP search of site for query, returns None on failure"""
        try:
            return urllib.urlopen("http://www." + self.site + "/Search?q=" + query)
        except:
            print "PHP search error"
            return None

# Query site for raw HTML
spider = Spider("bendbulletin.com")
searchterms = ["term1", "term2"] # etc....
pages = {}
for term in searchterms:
    pages[term] = spider.phpsearch(term).read()

# Compile and find all matches for legitimate link regexes
# Regexes are finite automata that parse a string looking for a pattern
# In this case I used regexes to find links im looking for
regexes = []
regexes.append(re.compile(r"www.bendbulletin.com/localstate/.{10,140}\?"))
regexes.append(re.compile(r"www.bendbulletin.com/opinion/.{10,140}\?"))
regexes.append(re.compile(r"www.bendbulletin.com/business/.{10,140}\?"))
regexes.append(re.compile(r"www.bendbulletin.com/health/.{10,140}\?"))


msg = "" # msg to email
linkstrings = []
# For each page in the dictionary of  pages
for key in pages.keys():
    html = pages[key]
    # Print search term
    msg += "\n\nArticles about " + key + ":"
    for regex in regexes:
        links = regex.findall(html)
        #  Remove duplicates (fancy trick)
        links = set(links) 
        links = list(links)
        # Print links returned
        for link in links:
            # \n means newline in strings
            msg += "\n" + link[:link.__len__()-1]
        print links


# E-mail results
print 1
server = smtplib.SMTP('smtp.gmail.com', 587) # 587 for TLS, 465 for SSL 
print 2
server.ehlo() # Identify self to server
server.starttls()
print 3
server.ehlo() # Identify again on encrypted connection (tls only)
server.login("buehlerowen@gmail.com", "PASSWORDREDACTED")
print 4
server.sendmail("buehlerowen@gmail.com", ["otb6@cornell.edu", "pbuehler@bendbroadband.com"], msg)

print "Done"



