import fileinput
import datetime
class HashTable:
    def __init__(self, rawEvent):
        if rawEvent == None:
            return 
        self.rawEvent = rawEvent
        self.dic = dict()
        #global water_mark
        
    @property
    def table(self):
        global water_mark
        water_mark = -1
        for event in self.rawEvent:
            new_event = event.split("|")
            water_mark= new_event[0]
            #HashTable.update(self, self.water_mark)
            #print ("self.water_mark",self.water_mark)
            if new_event[1] == "INSERT":
                if new_event[2] not in self.dic:
                    self.dic[new_event[2]] = new_event[3]
            elif new_event[1] == "UPSERT":
                self.dic[new_event[2]] = new_event[3]
            elif new_event[1] ==  "DELETE":
                if new_event[2] in self.dic:
                    self.dic[new_event[2]] = None
        return self.dic

    @property
    def high_watermark(self):
        #print ("self.water_mark",water_mark)
        if water_mark == -1:
            return datetime.datetime.utcnow()
        else:
            return datetime.datetime.utcfromtimestamp(water_mark/1000.0)

def print_report(snapshot):
    #print (f'High Watermark: {snapshot.high_watermark.strftime("%Y-%m-%dT%H:%M:S.%f")[:-3]z')
    print (snapshot.high_watermark.strftime("%Y-%m-%dT%H:%M:S.%f")[:-3])
    print ('\nTable State:')
    table = snapshot.table
    #print (table)
    for key in sorted(table.keys()):
        #print(f'\t{key}:{table[key]}')
        print ("\t"+key+":"+str(table[key]))
    
if __name__ == '__main__':
    rawEvent = ["1563454984001|INSERT|test|123", "1563454984002|UPSERT|test|456", "1563454984003|DELETE|test"]
    #rawEvent = ["1563454984001|DELETE|test|", "1563454984002|UPSERT|test|456", "1563454984003|INSERT|test|123"]
    #rawEvent = []
    table = HashTable(rawEvent)
    print_report(table)
