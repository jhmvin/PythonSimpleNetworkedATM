'''
Created on Jul 26, 2017

@author: Jhon Melvin
'''
from datetime import datetime,tzinfo,timedelta

class Zone(tzinfo):
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name
    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)
    def dst(self, dt):
            return timedelta(hours=1) if self.isdst else timedelta(0)
    def tzname(self,dt):
         return self.name
    pass #end of zone

class Time():
    
    ''' get the current time '''
    @staticmethod
    def now():
        GMT = Zone(8,False,'GMT') # +8 GMT ASIA TAIPEI
        return datetime.now(GMT).strftime('%m/%d/%Y %I:%M:%S %p')
        pass #end method
    
    pass #end class