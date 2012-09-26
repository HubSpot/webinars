import hashlib
from utils.dict import mget
from sanetime import time
from django.db import models as djmodels


class Event(object):

    @property
    def hub(self): return self.account.hub

    @property
    def starts_at(self): return self._starts_at or self._started_at
    @starts_at.setter
    def starts_at(self, starts_at): self._starts_at = starts_at
    
    @property
    def ends_at(self): return self._ends_at or self._ended_at
    @ends_at.setter
    def ends_at(self, ends_at): self._ends_at = ends_at

    @property
    def started_at(self): return self._started_at or self._starts_at
    @started_at.setter
    def started_at(self, started_at): self._started_at = started_at

    @property
    def ended_at(self): return self._ended_at or self._ends_at
    @ended_at.setter
    def ended_at(self, ended_at): self._ended_at = ended_at

    @property
    def duration_short_string(self):
        if self.duration.m <= 90: return "%sm" % self.duration.m
        return "%.1fh" % self.duration.fh

    @property
    def scheduled_duration(self): return self.starts_at and self.ends_at and (self.ends_at-self.starts_at)
    @scheduled_duration.setter
    def scheduled_duration(self, delta): 
        if self.starts_at: self.ends_at = self.starts_at + delta

    @property
    def actual_duration(self): return self.started_at and self.ended_at and (self.ended_at-self.started_at)
    @actual_duration.setter
    def actual_duration(self, delta): 
        if self.started_at: self.ended_at = self.started_at + delta

    @property
    def duration(self): return self.scheduled_duration
    @duration.setter
    def duration(self, delta): self.scheduled_duration = delta


    @property
    def _starts_at(self): return self._time_starts_at and self._timezone and time(self._time_starts_at.us, self._timezone)
    @_starts_at.setter
    def _starts_at(self, starts_at): 
        if starts_at is None:
            self._time_starts_at = None
        else:
            self._time_starts_at = time(starts_at.us)
            self._timezone = starts_at.tz_name

    @property
    def _ends_at(self): return self._time_ends_at and self._timezone and time(self._time_ends_at.us, self._timezone)
    @_ends_at.setter
    def _ends_at(self, ends_at): 
        if ends_at is None:
            self._time_ends_at = None
        else:
            self._time_ends_at = time(ends_at.us)
            self._timezone = ends_at.tz_name

    @property
    def _started_at(self): return self._time_started_at and self._timezone and time(self._time_started_at.us, self._timezone)
    @_started_at.setter
    def _started_at(self, started_at): 
        if started_at is None:
            self._time_started_at = None
        else:
            self._time_started_at = time(started_at.us)
            self._timezone = started_at.tz_name

    @property
    def _ended_at(self): return self._time_ended_at and self._timezone and time(self._time_ended_at.us, self._timezone)
    @_ended_at.setter
    def _ended_at(self, ended_at): 
        if ended_at is None:
            self._time_ended_at = None
        else:
            self._time_ended_at = time(ended_at.us)
            self._timezone = ended_at.tz_name

    @classmethod
    def calc_hashcode(kls, **kwargs):
        key = mget(kwargs,'remote_id', 'session_key', 'universal_key')
        if key: 
            source = key
        else:
            title = mget(kwargs,'title','subject')
            us_starts_at = kwargs.get('_time_starts_at',kwargs.get('starts_at',time(0)).us)
            us_ends_at = kwargs.get('_time_ends_at',kwargs.get('ends_at',time(0)).us)
            source = '%s|%s|%s'%(title,us_starts_at,us_ends_at)
        return int(int(hashlib.md5(source).hexdigest(),16)%2**31)

    def ensure_hashcode(self):
        self.hashcode = self.__class__.calc_hashcode(**self.__dict__)
