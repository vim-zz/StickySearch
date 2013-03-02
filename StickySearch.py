import sublime, sublime_plugin

#view.run_command("stickysearch")
class StickysearchCommand(sublime_plugin.TextCommand):
	def run(self, edit, op):
		# keep sticky per window (each window has its own set)
		view = self.view
		key = "StickySearch"

		if 'add' in op:
			regions = self.find_all_under_cursor(self.view) + view.get_regions(key)
			self.mark(key, view, regions)	
		if 'clear' in op:
			view.erase_regions(key)
		if 'set' in op:
			regions = self.find_all_under_cursor(self.view)
			self.mark(key, view, regions)
		
	def mark(self, key, view, regions):
		# optional icon name, if given, will draw the named icons in the gutter next to each region. 
		# The icon will be tinted using the color associated with the scope. 
		# Valid icon names are dot, circle, bookmark and cross
		view.add_regions(key, regions, "marker", "dot", sublime.PERSISTENT | sublime.DRAW_OUTLINED)

	def find_all_under_cursor(self, view):
		# view.window().run_command('find_all_under')
		the_cursor = view.sel()[0]
		# if no selection then expand to word under cursor and find all using word boundaries
		if(the_cursor.a == the_cursor.b):
			the_word_region = view.word(the_cursor)
			the_word = "\\b" + view.substr(the_word_region) + "\\b"
		# if there is visual selection, just use it to find all without word boundaries
		else:
			the_word_region = the_cursor
			the_word = view.substr(the_word_region)
		all_word_regions = view.find_all(the_word)			
		return all_word_regions
