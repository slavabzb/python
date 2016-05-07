#!/usr/bin/python

def process_file(istream, ostream, year):
    import json
    import csv
    import time

    values = {"open": 0, "close": 0, "max": 0, "min": 0}
                    
    with open(istream, "r") as src:
        reader = csv.DictReader(src)

        size = 0
        
        for irow in reader:
            date = time.strptime(irow["Date"], "%Y-%m-%d")
            if str(date.tm_year) == year:
                values["open"] += float(irow["Open"])
                values["close"] += float(irow["Close"])
                values["max"] += float(irow["High"])
                values["min"] += float(irow["Low"])
                size += 1

    if size != 0:
        for (key, value) in values.items():
            values[key] /= size

    json.dump(values, ostream)

def process_network(symbol, year, ostream):
    import datetime
    import time
    import json
    import csv
    from urllib2 import urlopen
    from urllib2 import quote
    
    start = datetime.date(int(year), 1, 1)
    end = datetime.date(int(year), 12, 31)
    url = "http://www.google.com/finance/historical?q={0}&startdate={1}&enddate={2}&output=csv"
    url = url.format(symbol.upper(), quote(start.strftime('%b %d, %Y')), quote(end.strftime('%b %d, %Y')))
    data = urlopen(url).readlines()
        
    values = {"open": 0, "close": 0, "max": 0, "min": 0}
    size = 0
    
    reader = csv.DictReader(data)
        
    for irow in reader:
        for key in irow.keys():
            newkey = str(key).decode("utf-8-sig").encode("utf-8")
            irow[newkey] = irow.pop(key)
        
        date = time.strptime(irow["Date"], "%d-%b-%y")
        if str(date.tm_year) == year:
            values["open"] += float(irow["Open"])
            values["close"] += float(irow["Close"])
            values["max"] += float(irow["High"])
            values["min"] += float(irow["Low"])
            size += 1

    if size != 0:
        for (key, value) in values.items():
            values[key] /= size

    json.dump(values, ostream)

if __name__ == "__main__":
    print("Data processor 0.1\n")
    
    import sys
    import argparse
    import logging
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--symbol", help="stock symbol")
    argparser.add_argument("--file", help="file to process by program")
    argparser.add_argument("--out", help="output file")
    argparser.add_argument("--logfile", help="log file")
    argparser.add_argument("--log", help="log level")
    argparser.add_argument("--year", help="year")
    args = argparser.parse_args()
    
    if args.log:
        numeric_level = getattr(logging, args.log.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % args.log)
        
        logging.basicConfig(filename=args.logfile, level=numeric_level)
        
    try:
        if args.file:
            istream = args.file
            
            if args.out:
                ostream = open(args.out, "w")
            else:
                ostream = sys.stdout
            
            logging.info("processing {}".format(istream))
            process_file(istream, ostream, args.year)
        elif args.symbol:
            if args.out:
                ostream = open(args.out, "w")
            else:
                ostream = sys.stdout

            logging.info("process network")
            if args.year:            
                process_network(args.symbol, args.year, ostream)
            else:
                logging.error("year is not specified")
    
    except IOError:
        logging.error("can't open file")
    except:
        logging.error("bad thing happened")        
        
    ostream.close()    

