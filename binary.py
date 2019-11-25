class WAL:
    def __init__(self, binary_wal):
        self.res = []
        #self.start = 0
        self.binary_wal = raw_data
    
    def parseTime(self,start, raw_data):
        time = str(int.from_bytes(raw_data[start:8], byteorder='big'))
        return time
        
    def getKeylength(self,start, raw_data):
        key_length = int.from_bytes(raw_data[start:start+2], byteorder='big') 
        return key_length

    def getKeyString(self,start, raw_data,key_length):
        keystring = raw_data[start:start+key_length].decode('latin-1')
        return keystring

    def getValueLegnth(self,start, raw_data):
        value_length = int.from_bytes(raw_data[start:start+2], byteorder='big') 
        return value_length
    
    def getValue(self,start,raw_data,value_length):
        value = raw_data[start:start+value_length].decode('latin-1')
        return value
    
    def messageName(self,start,raw_data):
        m_type = str(int.from_bytes(raw_data[start:start+1], byteorder='big'))
        return m_type
        
    def get_events(self):
        while self.binary_wal:
            start = 0
            time  = self.parseTime(start, self.binary_wal)
            start += 8 
            m_type = self.messageName(start, self.binary_wal)
            start += 1
            key_length = self.getKeylength(start, self.binary_wal)
            start += 2
            keystring = self.getKeyString(start,self.binary_wal,key_length)
            start += key_length
            if m_type == "0" :
                value_length = self.getValueLegnth(start, self.binary_wal)
                start += 2
                value = self.getValue(start, self.binary_wal,value_length)
                start += value_length
                self.res.append(time+"|"+"INSERT"+"|"+keystring+"|"+value)
            if m_type == "1" :
                value_length = self.getValueLegnth(start, self.binary_wal)
                start += 2
                value = self.getValue(start, self.binary_wal,value_length)
                start += value_length
                self.res.append(time+"|"+"UPSERT"+"|"+keystring+"|"+value)
            if m_type == "2":
                self.res.append(time+'|'+ 'DELETE'+'|'+keystring)
            self.binary_wal = self.binary_wal[start:]
        return self.res  
        
        
if __name__ == '__main__':    
    raw_data = bytes.fromhex(''.join([x.strip() for x in '0000016c052dcf4102000f746573745f6b65795f3132333839370000016c052dcf4100000e746573745f6b65795f30393831320010746573745f76616c75655f31323837360000016c052dcf4101000d746573745f6b65795f313233340012746573745f76616c75655f31323339393038']))
    #print(raw_data)
    wal = WAL(raw_data)
    print('Events')
    for event in wal.get_events():
        print(event)
