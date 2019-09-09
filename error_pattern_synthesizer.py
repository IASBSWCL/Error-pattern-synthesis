# Run with python version 2 

import random


HEX_FIELD = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

if __name__ == "__main__":
    # receive 3 parameters

    symbols = raw_input("How many patterns do you want to generate ?  ")
    symbols = int(symbols,10)
    symbolSize = raw_input("Enter Symbol size in bytes:  ")
    symbolSize = int(symbolSize,10)
    print('/n at this moment we just support Hex representation')
    


    packetErrorRate = raw_input("Packets error rate(%):  ")

    packetErrorRate = int(packetErrorRate,10)
    symbolErrorRate = raw_input("Symbols error rate: ")
    symbolErrorRate = int(symbolErrorRate,10)

    fileName = "pktErr-"
    fileName += str(packetErrorRate)
    fileName +="-symErr-"
    fileName += str(symbolErrorRate)
    fileName += ".txt"
    file= open("filename","w+")

    OriginalPacket = ''
    # two hex representation can be seen as a byte 
    for i in range (0,symbolSize*2):
        OriginalPacket += HEX_FIELD[random.randrange(0,16,1)]
        
    print "The original Packet: ", OriginalPacket

    for i in range(0,symbols):
        # write error pattern into a file
         file.write(OriginalPacket +"\n")

    


