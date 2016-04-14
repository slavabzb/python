#!/usr/bin/python

"""
    @brief Reads istream, calculates averages and put them to ostream
    @param istream input file
    @param ostream output file
"""
def process_file(istream, ostream):
    open_sum    = 0
    close_sum   = 0
    max_sum     = 0
    min_sum     = 0
    size        = 0    
    
    with open(istream, "r") as src:
        import csv
        reader = csv.DictReader(src)
        for irow in reader:
            open_sum    += float(irow["Open"])
            close_sum   += float(irow["Close"])
            max_sum     += float(irow["High"])
            min_sum     += float(irow["Low"])
            size        += 1
    
    import json
    json.dump({"open ave":  open_sum / size},   ostream)
    json.dump({"close ave": close_sum / size},  ostream)
    json.dump({"max ave":   max_sum / size},    ostream)
    json.dump({"min ave":   min_sum / size},    ostream)

if __name__ == "__main__":
    print("Data processor 0.0")
    print("")
    
    import sys
    
    try:
        istream = sys.argv[1]
    except IndexError:
        istream = raw_input("source file: ")
    
    try:
        ostream = open(sys.argv[2], "w")
    except IndexError:
        print("redirecting to stdout")
        ostream = sys.stdout

    try:
        print("processing {}".format(istream))
        process_file(istream, ostream)
        print("")
        print("done")
    except IOError:
        print("can't open file '{}'".format(istream))
    except:
        print("bad thing happened")        
        
    ostream.close()

