import sublime, sublime_plugin

#view.run_command("stickysearch")
class StickysearchCommand(sublime_plugin.TextCommand):
	def run(self, edit, op):
		# keep sticky per window (each window has its own set)
		view = self.view
		key = "StickySearch"
		view.window().run_command('find_all_under')
		
		if 'add' in op:
			self.add(key, view)
		if 'clear' in op:
			self.clear(key, view)
		if 'set' in op:
			self.set(key, view)			
		
		self.clear_selection(view)

	def set(self, key, view):
		self.mark(key, view, [])	

	def add(self, key, view):
		self.mark(key, view, view.get_regions(key))	
		
	def mark(self, key, view, regions):
		for s in view.sel():
			regions.append(sublime.Region(s.begin(), s.end()))
		# optional icon name, if given, will draw the named icons in the gutter next to each region. 
		# The icon will be tinted using the color associated with the scope. 
		# Valid icon names are dot, circle, bookmark 
		view.add_regions(key, regions, "marker", "dot", sublime.PERSISTENT+sublime.DRAW_OUTLINED)

	def clear(self, key, view):
		view.erase_regions(key)   

	def clear_selection(self, view):
		view.sel().clear()
