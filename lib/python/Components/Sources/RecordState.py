from Source import Source
from Components.Element import cached
from enigma import iRecordableService
from Components.SystemInfo import SystemInfo

class RecordState(Source):
	def __init__(self, session):
		Source.__init__(self)
		self.records_running = 0
		self.session = session
		session.nav.record_event.append(self.gotRecordEvent)
		self.gotRecordEvent(None, None) # get initial state

	def gotRecordEvent(self, service, event):
		prev_records = self.records_running
		if event in (iRecordableService.evEnd, iRecordableService.evStart, None):
			recs = self.session.nav.getRecordings()
			if SystemInfo["LCDsymbol_circle_recording"]:
				with open(SystemInfo["LCDsymbol_circle_recording"], "w") as fp:
					fp.write(recs and "1" or "0")
			self.records_running = len(recs)
			if self.records_running != prev_records:
				self.changed((self.CHANGED_ALL,))

	def destroy(self):
		self.session.nav.record_event.remove(self.gotRecordEvent)
		Source.destroy(self)

	@cached
	def getBoolean(self):
		return self.records_running and True or False
	boolean = property(getBoolean)

	@cached
	def getValue(self):
		return self.records_running
	value = property(getValue)
