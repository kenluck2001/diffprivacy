from collections import namedtuple
import random
from trie import Trie
from textProcessing import TEXTHANDLER
from crc import CRC

SEED = 2023


class NegativeDB:
    '''
        Hard-to-ReverseNegative Databases based on 3-SAT problem
        Reference: https://crypto.stanford.edu/portia/papers/HardNDBFinal.pdf

        The author the source code has made a design decision to restrict the 
        database is designed to only manipulate words or group of words limited 
        to 125 alphabetical characters only.

        we have delete and insert operations. At the moment, 
        update is a combination of delete and insert operations
    '''
    def __init__(self):
        self.txtHandler = TEXTHANDLER()
        self.crc = CRC()
        self.tree = Trie()
        Param = namedtuple('Param', ['l', 'r', 'k', 'q'])
        # Adding settings
        # 'l' is length of binary input without CRC bits, , 'r' is a value to manage superfluous solution, 'k' varies with r, 'q' is a probability for modifying the process
        self.settings = Param(1000, 5.5, 200, 0.5)
        #self.settings = Param(8, 1, 3, 0.5)

    def __generateHardToReverseRecords (self, sBin):
        '''
            Algorithm 3: Create hard to reverse records
            input:
                sBin with crc checksum bits in binary string
            output:
                list of hard-to-reverse records
        '''
        l = self.settings.l
        r = self.settings.r
        k = self.settings.k
        q = self.settings.q

        lenWithPaddedCRC = len(sBin)
        nLen = lenWithPaddedCRC * r
        #nLen = l * r
        nDBLst = []
        zlst = ["*"] * lenWithPaddedCRC

        negateBit = {
            '0': '1',
            '1': '0',
        }

        random.seed(SEED)

        while len(nDBLst) < nLen:
            gammaLst = [random.randint(0, lenWithPaddedCRC-1) for _ in range(k)]
            for ind in gammaLst:
                zlst[ind] = sBin[ind]

            prevzBin = "".join(zlst)
            curzBin = "".join(zlst)
            # check if any bit has changed
            while prevzBin == curzBin:
                for ind in gammaLst:
                    if q <= random.random():
                        zlst[ind] = negateBit[zlst[ind]] 
                curzBin = "".join(zlst)

            # add to store
            nDBLst.append (curzBin)
            # reset
            zlst = ["*"] * lenWithPaddedCRC

        # dedup
        nDBLst = set( nDBLst )

        return nDBLst

    def __verify(self, inputBin):
        '''
            input:
                inputBin has a combination of binary data concatenated with the CRC checksum
            output:
                boolean if error occured or not
        '''
        l = self.settings.l
        inBin = inputBin[:l]
        remainder = inputBin[l:]
        status = self.crc.crcCheck(inBin, remainder)

        return status

    def __prepInput (self, text):
        '''
            Convert alphabetical text (without CRC) to binary
            input:
                text (without CRC) in alphabet form
            output:
                padded text to specified length in binary string with CRC
        '''
        l = self.settings.l
        msgLen = len (text)
        if (msgLen > l // 8):
            raise Exception("Character size: {}, has exceed the database limit of {}".format (msgLen, l // 8))
        txtBin = self.txtHandler.ConvertAlphabetsToBinary(text)
        txtBinPadded = txtBin.zfill(l)
        remainder = self.crc.crcRemainder(txtBinPadded)
        processedWithCRCTxt = "{}{}".format(txtBinPadded, remainder)

        return processedWithCRCTxt

    def __insert (self, recordBin):
        '''
            Insert single records
            input:
                recordBin (with CRC) in binary
            output:
                return list of hard to reverse records
        '''
        # create hard to reverse record
        ndbRecords = self.__generateHardToReverseRecords (recordBin)
        # save records in a trie
        for record in ndbRecords:
            self.tree.insert(record)
            #self.tree.insert2(record)

        #@  TODO: SAVE TO DISK AFTER SAVING USING PICKLING LOGIC
        return ndbRecords

    def __find2 (self, recordBin):
        '''
            find a single records as a complement
            if the record is found in NDB, then it is not in DB

            input:
                recordBin (with CRC) in binary
            output:
                return true in data not in NDB, false otherwise


            This should have been the idea logic if we are able to save 1, 0 
            to replace * which is a wildcart matching. my attempt to create 
            binary while  exponential dimension as strings are compressed with *.
        '''

        # if db is empty
        if self.__isEmpty():
            # Unfortunately, an empty database contains the entireuniverse, but we want to avoid it until we have at least an entry.
            return False

        return not self.tree.find(recordBin)


    def __find (self, recordBin):
        '''
            find a single records as a complement
            if the record is found in NDB, then it is not in DB

            input:
                recordBin (with CRC) in binary
            output:
                return true in data not in NDB, false otherwise
        '''
        print ("find recordBin: {}".format(recordBin))

        print ("(find)result match *: {}".format(self.tree.query("*")) )
        print ("(find)result match 0: {}".format(self.tree.query("0")) )
        print ("(find)result match 1: {}".format(self.tree.query("1")) )

        # if db is empty
        if self.__isEmpty():
            # Unfortunately, an empty database contains the entireuniverse, but we want to avoid it until we have at least an entry.
            return False


        # create hard to reverse record
        ndbRecords = self.__generateHardToReverseRecords (recordBin)

        match = 0
        for record in ndbRecords:
            match += int(self.tree.find(record))

        matchRatio = float (match / len(ndbRecords))

        if matchRatio > 0.9:
            return True

        return False

    def __isEmpty (self):
        for val in ("*", "0", "1"):
            size = len (self.tree.query(val))
            if size > 0:
                return False

        return True

    def __delete (self, recordBin):
        '''
            delete single records
            input:
                recordBin (with CRC) in binary
            output:
                return list of hard to reverse records for the deleted item
        '''
        # create hard to reverse record
        ndbRecords = self.__generateHardToReverseRecords (recordBin)
        # delete records in a trie
        for record in ndbRecords:
            isDeleted = self.tree.remove(record)
            print ("isDeleted: {}".format(isDeleted))

        return ndbRecords

    def Insert (self, text):
        '''
            Insert single records
            input:
                text (without CRC) in alphabet form
            output:
                return list of hard to reverse records
        '''
        recordBin = self.__prepInput (text)
        ndbRecords = self.__insert (recordBin)

        return ndbRecords

    def Find (self, text):
        '''
            find a single records as a complement
            if the record is found in NDB, then it is not in DB

            input:
                text (without CRC) in alphabet
            output:
                return true in data not in NDB, false otherwise
        '''
        recordBin = self.__prepInput (text)
        status = self.__find (recordBin)

        return status

    def Delete (self, text):
        '''
            delete single records
            input:
                recordBin (with CRC) in binary
            output:
                return list of hard to reverse records for the deleted item
        '''
        recordBin = self.__prepInput (text)
        ndbRecords = self.__delete (recordBin)

        return ndbRecords

if __name__ == '__main__':
    ndb = NegativeDB()

    #self.settings = Param(8, 1, 3, 0.5)
    #text = 'a'
    #indbRecord = ndb.Insert (text)
    #print ("Inserted records: {}".format(indbRecord))

    #status = ndb.Find (text)
    #print ("========================================")
    #print ("========================================")
    #print ("is {} in DB: {}".format(text, status))

    #text = 'b'
    #status = ndb.Find (text)
    #print ("========================================")
    #print ("========================================")
    #print ("is {} in DB: {}".format(text, status))

    #text = 'a'
    #status = ndb.Find (text)
    #print ("========================================")
    #print ("========================================")
    #print ("is {} in DB: {}".format(text, status))


    text = 'Helloworldforengineersinthehouse'
    ndbRecord = ndb.Insert (text)
    status = ndb.Find (text)
    print ("========================================")
    print ("========================================")
    print ("is {} in DB: {}".format(text, status))

    text = 'pleasevisit'
    status = ndb.Find (text)
    print ("========================================")
    print ("========================================")
    print ("is {} in DB: {}".format(text, status))


    textlist = ['Helloworldforengineersinthehouse', 'cleanupthehouse', 'visitation', 'miraclousmedal']
    for text in textlist:
        ndbRecord = ndb.Insert (text)

    text = "notice"
    status = ndb.Find (text)
    print ("========================================")
    print ("========================================")
    print ("is {} in DB: {}".format(text, status))

    text = 'ken'
    ndbRecord = ndb.Insert (text)
    print ("========================================")
    print ("========================================")
    print ("Inserted records: {}".format(ndbRecord))

    print ("ndb.tree.root.counter: {}".format(ndb.tree.root.counter))
    status = ndb.Find (text)
    print ("========================================")
    print ("========================================")
    print ("is {} in DB: {}".format(text, status))
    print ("========================================")
    print ("========================================")
    ndbRecord = ndb.Delete (text)
    print ("is {} in DB: {}".format(text, status))


    text = 'jan'
    status = ndb.Find (text)
    print ("========================================")
    print ("========================================")
    print ("is {} in DB: {}".format(text, status))

