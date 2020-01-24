import random 


class Packet:
    brokenSymbolCount = 0
    def __init__(self,eachPacketSize,symbolErrorRate):
        self.packet = [0] * eachPacketSize
        for i in range (0,eachPacketSize):
            if(random.randrange(1,101,1) < symbolErrorRate):
                self.packet[i]=1
                self.brokenSymbolCount +=1

        
def examination(NumberOfPackets,symbolErrorRate,eachPacketSize,symbolSize): 
    # here we need to control all examinations
    # expected Number of packet needed can be replace with Number of packets
    
    L = [0] * 
    for i in range (0,NumberOfPackets):


    a = 1
    return a

def GeneralExamination():
    # general examination here

    a = examination()


if __name__ == "__main__":

    print "Welcome to HL Blancer."
    print "This program generates a result folder."
    print "_______________________________________\n"

    # generation Size = number of raw symbols
    generationSize = int(raw_input("Generation Size (W): "))
    redundancySize = int(raw_input("Redundancy (R): "))

    eachPacketSize = generationSize + redundancySize

    print "Packet Size (K+R): " + str(eachPacketSize)

    limitedThreshold = generationSize
    print "Max Fixing Threshold : " + str(limitedThreshold)

    symbolErrorRate = int(raw_input("Symbol Error Rate: "))

    numberOfExams = int(raw_input("Examination Iteration: "))

    print "_______________________________________\n"

