#!/usr/bin/python

import glob

html = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
	<title>Robots</title>
</head>
<body><ul>'''

for egg in glob.glob('*egg'):
    html = html + '<li><a href="%s">%s</a></li>' % ( egg, egg )

html = html + '</ul></body></html>'

print html
