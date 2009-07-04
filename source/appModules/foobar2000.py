import _default
import api
import ui
import time
import calendar

def getFormat(s):
	s=s.split(":")
	if len(s) ==1:
		return "%S"
	elif len(s)==2:
		return "%M:%S"
	else: return "%H:%M:%S"

def getOutputFormat(t):
	if t<60:
		return "%S"
	elif t<3600:
		return "%M:%S"
	else: 
		return "%H:%M:%S"

class AppModule(_default.AppModule):
	statusBar=None

	def event_gainFocus(self, obj, nextHandler):
		if not self.statusBar: self.statusBar=api.getStatusBar()
		nextHandler()

	def getElapsedAndTotal(self):
		if not self.statusBar: return None
		text = api.getStatusBarText(self.statusBar)
		try:
			ltime = text.split("|")[4].split(" / ")
		except IndexError:
			return None
		elapsedTime = calendar.timegm(time.strptime(ltime[0].strip(),getFormat(ltime[0])))
		totalTime = calendar.timegm(time.strptime(ltime[1].strip(),getFormat(ltime[1])))
		return elapsedTime,totalTime

	def script_reportRemainingTime(self,keyPress):
		times=self.getElapsedAndTotal()
		if times is None:
			ui.message(_("No track playing"))
			return
		elapsedTime,totalTime = times
		remainingTime = totalTime-elapsedTime
		msg = time.strftime(getOutputFormat(remainingTime),time.gmtime(remainingTime))
		ui.message(msg)
	script_reportRemainingTime.__doc__ = _("Reports the remaining time of the currently playing track, if any")