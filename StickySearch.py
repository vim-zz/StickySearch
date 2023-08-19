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
			self.op_add()
		if 'clear' in op:
			self.op_clear()
		if 'set' in op:
			self.op_clear()
			self.op_add()

	def op_add(self):
		selected_region = self.view.sel()[0]
		selected_word = self.selection_under_cursor(selected_region)
		key = self.marker_key(selected_word)
		regions = self.view.find_all(selected_word)
		# Mark new selections, or jump to next resion on exsiting marks
		if key not in self._keys:
			self.mark(key, regions)
			self._keys.append(key)
		else:
			self.jump_to_next_match(selected_region, regions)

	def op_clear(self):
		selected_region = self.view.sel()[0]
		selected_word = self.selection_under_cursor(selected_region)
		marker_key = self.marker_key(selected_word)
		
		preserve_keys = []
		for key in self._keys:
			if key != marker_key:
				self.view.erase_regions(key)
			else:
				preserve_keys.append(marker_key)
		
		self._keys = preserve_keys

	def marker_key(self, uid):
		return f"{self._keybase}_{uid}"

	def jump_to_next_match(self, sel, regions):
		the_word_region = self.region_under_cursor(sel)
		for pos in regions:
			if pos.a > the_word_region.a:
				break
		else:
			# cycle back to first match
			pos = regions[0]

		pos.b = pos.a
		self.view.sel().clear() 
		self.view.sel().add(pos)
		self.view.show(pos)
		
	def mark(self, key, regions):
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
		
		self.view.add_regions(key, regions, scope, icon_name, flags)

	def selection_under_cursor(self, sel):
		# if there is visual selection, just use it to find all without word boundaries
		# if no selection then expand to word under cursor and find all using word boundaries
		has_selection = sel.a != sel.b
		if has_selection:
			the_word_region = sel
			selected_txt = self.view.substr(the_word_region)
			# support special charecters 
			selected_word = re.escape(selected_txt)
		else:
			the_word_region = self.view.word(sel)
			selected_word = "\\b" + self.view.substr(the_word_region) + "\\b"
		
		return selected_word

	def region_under_cursor(self, sel):
		# if there is visual selection, just use it to find all without word boundaries
		# if no selection then expand to word under cursor and find all using word boundaries
		has_selection = sel.a != sel.b
		if has_selection:
			the_word_region = sel
		else:
			the_word_region = self.view.word(sel)

		return the_word_region
