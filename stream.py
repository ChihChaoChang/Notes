import fileinput
import datetime
class HashTable:
    def __init__(self, rawEvent):
        self.rawEvent = rawEvent
        self.dic = dict()
        self.water_mark = -1
        self.key = ""
        self.m_type = ""
        self.value = 0
        
    @property
    def table(self):
        if self.rawEvent == None:
            return 
        for event in self.rawEvent:
            new_event = event.split("|")
            self.m_type = new_event[1]
            self.key = new_event[2]
            if self.m_type != "DELETE":
                self.value = new_event[3]
            if self.m_type == "INSERT":
                if self.key not in self.dic:
                    self.dic[self.key] = self.value
            if self.m_type == "UPSERT":
                self.dic[self.key] = self.value
            elif self.m_type ==  "DELETE":
                if self.key in self.dic:
                    self.dic[self.key] = None
        return self.dic
    

    @property
    def high_watermark(self):
        for event in self.rawEvent:
            new_event = event.split("|")
            self.water_mark = int(new_event[0])
        print ("self.water_mark",self.water_mark)
        if self.water_mark == -1:
            return datetime.datetime.utcnow()
        else:
            return datetime.datetime.utcfromtimestamp(self.water_mark/1000.0)


def print_report(snapshot):
    #print (f'High Watermark: {snapshot.high_watermark.strftime("%Y-%m-%dT%H:%M:S.%f")[:-3]z')
    print (snapshot.high_watermark.strftime("%Y-%m-%dT%H:%M:S.%f")[:-3])
    print ('\nTable State:')
    table = snapshot.table
    print (table)
    for key in sorted(table.keys()):
        #print(f'\t{key}:{table[key]}')
        print ("\t"+key+":"+str(table[key]))
    
if __name__ == '__main__':
    rawEvent = ["1563454984001|INSERT|test|123", "1563454984002|UPSERT|test|456", "1563454984003|DELETE|test"]
    #rawEvent = ["1563454984001|DELETE|test|", "1563454984002|UPSERT|test|456", "1563454984003|INSERT|test|123"]
    #rawEvent = []
    table = HashTable(rawEvent)
    print_report(table)
