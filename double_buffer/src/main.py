from dbuf import DBuf
import threading, time, signal, sys
from datetime import datetime

## LOGGING OPTIONS
DEBUGLOG   = 'OFF'
INFOLOG    = 'ON'
##################

BUF_LEN = 10
NR_BUFFERS = 2

WRITE_DELAY_SEC = 1
READ_DELAY_SEC  = 1

MESSAGES = ['HELLO JACK',
            'HI JOHN =]']

shouldExit = False

def debugPrint(msg):
    global DEBUGLOG
    if DEBUGLOG == 'ON':
        print(msg)

def infoPrint(msg):
    global INFOLOG
    if INFOLOG == 'ON':
        now = datetime.now()
        print('[' + now.strftime("%H:%M:%S") + ']' + ' ' + str(msg))

def sigHandler(signum, frame):
    global shouldExit
    debugPrint("Exiting Application")
    shouldExit = True

def writeThread(dbuf):
    global shouldExit, MESSAGES
    index = 0
    msgIdx = 0
    writing = False
    while True:
        if shouldExit:
            break

        if not writing:
            if index == 0:
                writing = dbuf.startWrite()

        if writing:
            dbuf.write(list(MESSAGES[msgIdx])[index], index)
            index += 1

            if index == dbuf.getLen():
                debugPrint("write done")
                dbuf.writeDone()
                writing = False
                index = 0
                if msgIdx == 0:
                    msgIdx = 1
                else:
                    msgIdx = 0

        time.sleep(WRITE_DELAY_SEC / BUF_LEN)

def readThread(dbuf):
    global shouldExit
    index = 0
    outbuf = []
    reading = False
    while True:
        if shouldExit:
            break

        if not reading:
            if dbuf.startRead():
                reading = True
                debugPrint("start read")

        if reading:
            outbuf.append(dbuf.read(index))
            index += 1

            if index == dbuf.getLen():
                debugPrint("read done")
                dbuf.readDone()
                reading = False
                infoPrint(''.join(outbuf))
                outbuf = []
                index = 0

        time.sleep(READ_DELAY_SEC / BUF_LEN)

def main(argv):
    global shouldExit
    dbuf = DBuf(BUF_LEN, NR_BUFFERS)

    signal.signal(signal.SIGINT, sigHandler)

    wtThread = threading.Thread(target=writeThread, args=(dbuf,))
    wtThread.start()

    rdThread = threading.Thread(target=readThread, args=(dbuf,))
    rdThread.start()

    while True:
        if shouldExit:
            break
        else:
            time.sleep(0.1)

    wtThread.join()
    rdThread.join()


if __name__ == '__main__':
    main(sys.argv[1:])
