import threading


## Assumptions & Constraints
# 1. Writing & Reading are happening from two different threads, but only one thread will write and only one thread will read.
# 2. You may only write or read one byte at a time


## TODO: allocate and free the buffers as needed.. change write0

class buf:
    def __init__(self, len):
        self.buf = [0] * len
        self.dataToRead = False

class DBuf:
    def __init__(self, len, nrBuffers):
        self.bufcnt = nrBuffers
        self.buf = [buf(len) for i in range(self.bufcnt)]
        self.wtIdx = -1
        self.rdIdx = -1

    def startWrite(self):
        self.wtIdx = -1
        for i in range(self.bufcnt):
            if not self.buf[i].dataToRead:
                self.wtIdx = i
                break
        return self.wtIdx != -1

    def write(self, byte, index):
        ret = False
        if self.wtIdx != -1:
            self.buf[self.wtIdx].buf[index] = byte
            ret = True
        return ret

    def writeDone(self):
        self.buf[self.wtIdx].dataToRead = True
        self.wtIdx = -1

    def startRead(self):
        self.rdIdx = -1
        for i in range(self.bufcnt):
            if self.buf[i].dataToRead:
                self.rdIdx = i
                break
        return self.rdIdx != -1

    def read(self, index):
        if self.rdIdx != -1:
            return self.buf[self.rdIdx].buf[index]
        else:
            return 0xFF

    def readDone(self):
        self.buf[self.rdIdx].dataToRead = False
        self.rdIdx = -1
    
    def getLen(self):
        return len(self.buf[0].buf)