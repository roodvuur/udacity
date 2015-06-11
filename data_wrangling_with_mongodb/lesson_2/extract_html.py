import requests

html = requests.get('http://www.transtats.bts.gov/Data_Elements.aspx?Data=2')
target = open('html_page.html', 'w')
target.write(html.text)