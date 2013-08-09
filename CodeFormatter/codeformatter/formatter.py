# @author 		Avtandil Kikabidze
# @copyright 		Copyright (c) 2008-2013, Avtandil Kikabidze (akalongman@gmail.com)
# @link 			http://long.ge
# @license 		GNU General Public License version 2 or later;

import sublime
import re

try:
	# Python 3
	from .phpformatter import PhpFormatter
	from .jsformatter import JsFormatter
	from .htmlformatter import HtmlFormatter
	from .cssformatter import CssFormatter
	from .pyformatter import PyFormatter

except (ValueError):
	# Python 2
	from phpformatter import PhpFormatter
	from jsformatter import JsFormatter
	from htmlformatter import HtmlFormatter
	from cssformatter import CssFormatter
	from pyformatter import PyFormatter


class Formatter:
	def __init__(self, view=False, file_name=False):
		self.platform = sublime.platform()
		self.classmap = {
			'php': PhpFormatter,
			'javascript': JsFormatter,
			'json': JsFormatter,
			'html': HtmlFormatter,
			'css': CssFormatter,
			'python': PyFormatter
		}


		self.syntax_file = view.settings().get('syntax')
		self.syntax = self.getSyntax()
		self.file_name = file_name
		self.settings = sublime.load_settings('CodeFormatter.sublime-settings')
		self.packages_path = sublime.packages_path()

	def format(self, text):
		try:
			formatter = self.classmap[self.syntax](self)
		except Exception as e:
			stdout = ""
			stderr = "Formatter for "+self.syntax+" files not supported."
			return self.clean(stdout), self.clean(stderr)

		try:
			stdout, stderr = formatter.format(text)
		except Exception as e:
			stdout = ""
			stderr = str(e)

		return self.clean(stdout), self.clean(stderr)


	def exists(self):
		if self.syntax in self.classmap:
			return True
		else:
			return False

	def getSyntax(self):
		pattern = re.compile(r"Packages/(.+?)/.+?\.tmLanguage")
		m = pattern.search(self.syntax_file)
		found = ""
		if (m):
			for s in m.groups():
				found = s
				break
		return found.lower()

	def clean(self, string):
		return re.sub(r'\r\n|\r', '\n', string.decode('utf-8'))