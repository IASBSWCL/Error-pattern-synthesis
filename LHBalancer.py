import random 
import os
import math
import operator as op
from functools import reduce


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom

def proposedFormulaNew(generationSize,redundancySize,symbolErrorRate ,limitedThreshold):
    # I've changed k = generationSize to k= generationSize + redundancySize because in ACR we don't have any redundancy 
    # if we want to compute it in this process we have to consider that
    k = generationSize + redundancySize
    r = redundancySize

    # convert percent (0 - 100) to rate (0.0 - 1.0) 
    e = float(symbolErrorRate) / float(100)

    T = limitedThreshold
    sum = 0                                                                                
    s=0    

    for i in range (T +1, k +1):                                                                    
        s+= (ncr(k, i)*((e)**i))* ((1-e)**(k-i))                                                   
                                                                                                
    for i in range (T +1, k+1):                                                                     
        sum = sum + (float(ncr(k,i) * (e**i)  * ((1-e)**(k -i)))/s ) * float(i)/k                  
        a = (float(ncr(k,i) * (e**i)  * ((1-e)**(k-i)))/ s ) * float(i)/k                        
    
    return sum*100


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
    
    def getErrorProbability(self):
        
        if (self.totalSymbol == 0 ):
            print "No Examination"
        else :
            return (float(self.totalBroken)/float(self.totalSymbol)) * 100
     
class Packet:
    brokenSymbolCount = 0
    def __init__(self,eachPacketSize,symbolErrorRate):
        self.packet = [0] * eachPacketSize
        for i in range (0,eachPacketSize):
    
            # ************* we should change error synthesis also because of this randrange
            if(random.randrange(1,101,1) <= symbolErrorRate):
                self.packet[i]=1
                self.brokenSymbolCount +=1

    def getBrokenSymbolNumber(self):
        return self.brokenSymbolCount

class deterministicPacket:
    brokenSymbolCount = 0
    def __init__(self,eachPacketSize,numberOfError):
        self.packet = [0] * eachPacketSize
        for i in range (0,eachPacketSize):
            if(i<numberOfError):
                self.packet[i]=1
                self.brokenSymbolCount +=1

    def getBrokenSymbolNumber(self):
        return self.brokenSymbolCount


def makeOutput(limited , hinted , totallyBroken,  FullHealthy , errorProbabilityAfterLimited , computedErrorRate,generationSize,redundancySize,symbolErrorRate):
    '''
    Generation size (K) : G
    Redundancy: R
    Symbol Error: E
    Folder Name : G-12-R-5
    File Name:  E-3-G-12-R-5 / E-3-Folder Name
    FIG Name: PACKET_ANALYSIS_G-12-R-5-E-3
    FIG Name: FORMULA_ACCURACY-G-12-R-E-3
    '''
    
    folderPath = "./Result/G-" + str(generationSize) + "-R-"+str(redundancySize)

    
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)


    filePath = folderPath + "/E-"+ str(symbolErrorRate) + "-G-"+ str(generationSize) + "-R-"+ str(redundancySize)+".txt"
    f = open(filePath,"w+")
    f.write("Initial theoretical error:"+ str(symbolErrorRate) +'\n')
    f.write("Computed Error:" + str(computedErrorRate) +'\n')
    
    for i in range(0,redundancySize+1):
        formulaE = proposedFormulaNew(generationSize,redundancySize,symbolErrorRate,i)
        f.write("Threshold:"+str(i)+" , e'(T):"+str(errorProbabilityAfterLimited[i].getErrorProbability())+ " , Fe(t): "+ str(formulaE) )
        f.write (' , LB: %(LB)f  , HB: %(HB)f  , TB: %(TB)f  , H: %(H)f \n' % {'LB': limited[i], 'HB': hinted[i], 'TB': totallyBroken[i], 'H': FullHealthy})
        

    return 




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
    #  convert 1 to 2 ******
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
        # tempPacket = deterministicPacket(eachPacketSize,i)

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

    computedErrorRate = (float(totalNumberOfSymbolErrors)/float(totalNumberOfSymbols))*100 

    #  convert Totally broken , limited , hinted, fullHealthy to percentage
    for i in range ( 0, maxThreshold):
        limited[i] = (float(limited[i]) /float(NumberOfPackets))*100
        hinted[i] = (float(hinted[i]) / float(NumberOfPackets))*100
        totallyBroken[i] = (float(totallyBroken[i])/ float(NumberOfPackets))*100
    
    FullHealthy = (float(FullHealthy) / float(NumberOfPackets))*100

    return  limited , hinted , totallyBroken,  FullHealthy , errorProbabilityAfterLimited , computedErrorRate

#  def GeneralExamination(NumberOfPackets,symbolErrorRate,eachPacketSize,generationSize ,numberOfExams):

    #  general examination here
    # limited,hinted,FullHealthy = examination(NumberOfPackets,symbolErrorRate,eachPacketSize,generationSize)


if __name__ == "__main__":



    # proposedFormulaEdited(5,5,50,3)

    print "Welcome to HL Blancer."
    print "This program generates a result folder."
    print "_______________________________________\n"

    # generation Size = number of raw symbols
    generationSize = int(raw_input("Generation Size (W): "))
    redundancySize = int(raw_input("Redundancy (R): "))

    eachPacketSize = generationSize + redundancySize

    print "Packet Size (K+R): " + str(eachPacketSize)

    limitedThreshold = redundancySize
    print "Max Fixing Threshold : " + str(limitedThreshold)

    numberOfExams = int(raw_input("Examination Iteration: "))

    print "_______________________________________\n" 
    for symbolErrorRate in range (2,30,4):
        print str(symbolErrorRate) + "  Cycle finished ::::: "
        # SIMULATION OUTPUT
        limited , hinted , totallyBroken,  FullHealthy , errorProbabilityAfterLimited , computedErrorRate = examination(numberOfExams,symbolErrorRate,eachPacketSize,generationSize)
        # FORMULA OUTPUT 

        # PRINTING FUNCTION
        makeOutput(limited , hinted , totallyBroken,  FullHealthy , errorProbabilityAfterLimited , computedErrorRate,generationSize,redundancySize,symbolErrorRate)