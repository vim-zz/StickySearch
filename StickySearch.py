import re
import sublime, sublime_plugin

#view.run_command("stickysearch")
class StickysearchCommand(sublime_plugin.TextCommand):
	_scopes = [
		"region.yellowish", 
		"region.bluish",
		"region.redish", 
		"region.orangish", 
		"region.greenish", 
		"region.cyanish", 
		"region.purplish", 
		"region.pinkish",
	]
	_keys = []
	_keybase = "StickySearch"

	def run(self, edit, op):
		# keep sticky per window (each window has its own set)
		if 'add' in op:
			self.op_add(self.view)
		if 'clear' in op:
			self.op_clear(self.view)
		if 'set' in op:
			self.op_clear(self.view)
			self.op_add(self.view)

	def op_add(self, view):
		selection = self.find_all_under_cursor(view)
		regions = view.find_all(selection)
		key = self._keybase + str(len(self._keys))
		self.mark(key, view, regions)
		self._keys.append(key)

	def op_clear(self, view):
		for key in self._keys:
			view.erase_regions(key)
		self._keys = []

	def mark(self, key, view, regions):
		settings = sublime.load_settings("StickySearch.sublime-settings")
		flags = sublime.PERSISTENT
		if not settings.get("fill", False):
			flags |= sublime.DRAW_NO_FILL
		if not settings.get("outline", True):
			flags |= sublime.DRAW_NO_OUTLINE
		
		# optional icon name, if given, will draw the named icons in the gutter next to each region.
		# The icon will be tinted using the color associated with the scope.
		# Valid icon names are dot, circle, bookmark and cross
		icon_name = settings.get("icon", "dot")

		# optional string used to source a color to draw the regions in. The scope is matched 
		# against the color scheme.
		next_marker_index = len(self._keys)
		num_of_available_scopes = len(self._scopes)
		if settings.get("rainbow", True):
			scope = self._scopes[next_marker_index % num_of_available_scopes]
		else:
			scope = "region.yellowish"
		view.add_regions(key, regions, scope, icon_name, flags)

	def find_all_under_cursor(self, view):
		# view.window().run_command('find_all_under')
		sel = view.sel()[0]
		# if there is visual selection, just use it to find all without word boundaries
		# if no selection then expand to word under cursor and find all using word boundaries
		has_selection = sel.a != sel.b
		if has_selection:
			the_word_region = sel
			selected_txt = view.substr(the_word_region)
			# support special charecters 
			selected_word = re.escape(selected_txt)
		else:
			the_word_region = view.word(sel)
			selected_word = "\\b" + view.substr(the_word_region) + "\\b"
		
		return selected_word

