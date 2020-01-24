# Run with python version 2 

import random


HEX_FIELD = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

if __name__ == "__main__":
    # receive 3 parameters

    symbols = raw_input("How many patterns do you want to generate ?  ")
    symbols = int(symbols,10)
    symbolSize = raw_input("Enter Symbol size in bytes:  ")
    symbolSize = int(symbolSize,10)
    print  'Up to this moment, we just support Hex representation (field is fixed to 8)'


    packetErrorRate = raw_input("Packets error rate(%):  ")

    packetErrorRate = int(packetErrorRate,10)
    symbolErrorRate = raw_input("Symbols error rate(%): ")
    symbolErrorRate = int(symbolErrorRate,10)

    fileName = "pktErr-"
    fileName += str(packetErrorRate)
    fileName +="-symErr-"
    fileName += str(symbolErrorRate)
    fileName += ".txt"
    file= open(fileName,"w+")
    originalPacketList = []
    OriginalPacket = ''
    # two hex representation can be seen as a byte 
    for i in range (0,symbolSize):
        tempA = HEX_FIELD[random.randrange(0,16,1)]
        tempB = HEX_FIELD[random.randrange(0,16,1)]
        tempSymbol = tempA + tempB
        OriginalPacket += tempSymbol
        originalPacketList.append(tempSymbol)

        
    print "The original Packet: ", OriginalPacket

    for i in range(0,symbols):
        # write error pattern into a file
        packetErrorChance = random.randrange(1,101,1)
        if(packetErrorChance<packetErrorRate):
            # we should change the symbol

            errorPattern =''
            for j in range (0 , symbolSize):
                symbolErrorChance = random.randrange(1,101,1)
                if(symbolErrorChance > symbolErrorRate ):
                    error = ''
                    firstRandHex =  HEX_FIELD[random.randrange(0,16,1)] 
                    secondRandHex = HEX_FIELD[random.randrange(0,16,1)]
                    error = firstRandHex + secondRandHex
                    errorPattern +=error
                else:
                    errorPattern +=originalPacketList[j]
            file.write(errorPattern+"\n")
        else: 
            file.write(OriginalPacket+"\n")

         

    


