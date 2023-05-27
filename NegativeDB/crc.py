class CRC:
    """
        Cyclic Redundancy Check
        Reference: https://en.wikipedia.org/wiki/Cyclic_redundancy_check
    """
    def __init__(self, polyBin = "011010111100000011110101"):
        self.polyBin = polyBin

    def crcRemainder(self, inputBin, pad = '0'):
        """Calculate the CRC remainder of a string of bits using a chosen polynomial.
        pad should be '1' or '0'.
        """
        self.polyBin = self.polyBin.lstrip('0')
        lenInput = len(inputBin)
        initialPadding = (len(self.polyBin) - 1) * pad
        inputPaddedArray = list(inputBin + initialPadding)
        while '1' in inputPaddedArray[:lenInput]:
            curShift = inputPaddedArray.index('1')
            for i in range(len(self.polyBin)):
                inputPaddedArray[curShift + i] \
                = str(int(self.polyBin[i] != inputPaddedArray[curShift + i]))

        return ''.join(inputPaddedArray)[lenInput:]

    def crcCheck(self, inputBin, checkVal):
        """Calculate the CRC check of a string of bits using a chosen polynomial."""
        self.polyBin = self.polyBin.lstrip('0')
        lenInput = len(inputBin)
        initialPadding = checkVal
        inputPaddedArray = list(inputBin + initialPadding)
        while '1' in inputPaddedArray[:lenInput]:
            curShift = inputPaddedArray.index('1')
            for i in range(len(self.polyBin)):
                inputPaddedArray[curShift + i] \
                = str(int(self.polyBin[i] != inputPaddedArray[curShift + i]))

        return ('1' not in ''.join(inputPaddedArray)[lenInput:])

if __name__ == '__main__':
    crc = CRC()
    inputBin = "1101" * 256
    remainder = crc.crcRemainder(inputBin)
    print ("remainder: {}".format (remainder))
    status = crc.crcCheck(inputBin, remainder)
    print ("status: {}".format(status))
    print ("==================================")

    crc = CRC()
    inputBin = "1101" * 250
    remainder = crc.crcRemainder(inputBin)
    #remainder = remainder.zfill(24)
    print ("remainder: {}".format (remainder))

    #remainder = remainder.lstrip('0')
    status = crc.crcCheck(inputBin, remainder)
    print ("status: {}".format(status))

    print ("==================================")

    crc = CRC()
    inputBin = "0100" * 250
    remainder = crc.crcRemainder(inputBin)
    #remainder = remainder.zfill(24)
    print ("remainder: {}".format (remainder))

    #remainder = remainder.lstrip('0')
    status = crc.crcCheck(inputBin, remainder)
    print ("status: {}".format(status))



