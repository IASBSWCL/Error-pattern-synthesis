import random 

class symbolErrorProbability():

    totalBroken = 0
    totalSymbol = 0
    
    def increase(self,total , broken):
        self.totalSymbol +=total
        self.totalBroken +=broken
    
    def getTotalSymbol(self):
        return self.totalSymbol
    
    def getTotalBroken(self):
        return self.totalBroken
    
    def errorProbability(self):
        
        if (self.totalSymbol == 0 ):
            print "No Examination"
        else :
            return self.totalBroken/self.totalSymbol
     
class Packet:
    brokenSymbolCount = 0
    def __init__(self,eachPacketSize,symbolErrorRate):
        self.packet = [0] * eachPacketSize
        for i in range (0,eachPacketSize):
            if(random.randrange(1,101,1) < symbolErrorRate):
                self.packet[i]=1
                self.brokenSymbolCount +=1

    def getBrokenSymbolNumber(self):
        return self.brokenSymbolCount


        
def examination(NumberOfPackets,symbolErrorRate,eachPacketSize,generationSize): 
    # here we need to control all examinations
    # expected Number of packet needed can be replace with Number of packets

    ''' 
    each packet size = k + r 
    limited[i]: Shows when the threshold is "i" How many of "PACKETS" can be fixed in LimitedDecoder
    hinted[i]: Shows when the threshold is "i" How many of "PACKETS" can be fixed JUST in HintedDecoder
    Full healthy: Number of packets with no errors
    errorProbabilityAfterLimited[i]: records symbol errors and total symbols when the threshold is "i"
    '''

    # 
    theoreticalError = symbolErrorRate
    computedErrorRate = 0
    totalNumberOfSymbolErrors=0
    totalNumberOfSymbols = 0
    iterationNumber = NumberOfPackets

    # threshold can be equal to R at most , + 1 because it is starting from zero
    maxThreshold = (eachPacketSize - generationSize) + 1


    limited = [0] * maxThreshold
    hinted = [0] * maxThreshold
    totallyBroken = [0] * maxThreshold


    errorProbabilityAfterLimited = []



    for i in range (0,maxThreshold):
        errorProbabilityAfterLimited.append(symbolErrorProbability())

    # count all symbols and then divide number of broken by all symbols
    errorProbabilityInGeneral=0
    FullHealthy = 0
    redundancy = eachPacketSize - generationSize
    packetRepository = []

    for i in range (0,NumberOfPackets):

        tempPacket = Packet(eachPacketSize,symbolErrorRate)

        #  here we should conut lots of thing
        numberOfError = tempPacket.getBrokenSymbolNumber()

        if(numberOfError == 0 ):
            FullHealthy +=1

        totalNumberOfSymbolErrors +=numberOfError
        totalNumberOfSymbols += eachPacketSize

        for j in range(0,maxThreshold):
            # here j is our threshold
            # errors with less than j errors are going to be fixed so we shouldn't count them here 
            if(numberOfError<=j):
                limited[j] +=1
                
            else:
                errorProbabilityAfterLimited[j].increase(eachPacketSize,numberOfError)
                if(numberOfError<=redundancy):
                    hinted[j] +=1
                else:
                    totallyBroken[j] +=1

        packetRepository.append(tempPacket) 

    # we should count symbols error  after and before 

    computedErrorRate = float(totalNumberOfSymbolErrors)/float(totalNumberOfSymbols) 

    #  convert Totally broken , limited , hinted, fullHealthy to percentage
    for i in range ( 0, maxThreshold):
        limited[i] = float(limited[i]) /float(NumberOfPackets)
        hinted[i] = float(hinted[i]) / float(NumberOfPackets)
        totallyBroken[i] = float(totallyBroken[i])/ float(NumberOfPackets)
    
    FullHealthy = float(FullHealthy) / float(NumberOfPackets)

    return  limited , hinted , totallyBroken,  FullHealthy , errorProbabilityAfterLimited , computedErrorRate

#  def GeneralExamination(NumberOfPackets,symbolErrorRate,eachPacketSize,generationSize ,numberOfExams):


    #  general examination here

    # limited,hinted,FullHealthy = examination(NumberOfPackets,symbolErrorRate,eachPacketSize,generationSize)


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
    for symbolErrorRate in range (10,30,4):
        print str(symbolErrorRate) + "  Cycle finished ::::: "
        examination(6,symbolErrorRate,31,26)

