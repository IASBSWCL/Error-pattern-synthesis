import random


if __name__ == "__main__":

    print "Welcome to HL Blancer."
    print "This program generates a result folder."
    print "_______________________________________\n"

    generationSize = int(raw_input("Generation Size (W): "))
    redundancySize = int(raw_input("Redundancy (R): "))

    eachPacketSize = generationSize + redundancySize

    print "Packet Size (K+R): " + str(eachPacketSize)

    limitedThreshold = generationSize
    print "Max Fixing Threshold : " + limitedThreshold

    symbolErrorRate = int(raw_input("Symbol Error Rate: "))

    numberOfExams = int(raw_input("Examination Iteration: "))

