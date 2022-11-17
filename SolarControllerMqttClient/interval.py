def readInterval():
    try: 
        f=open("interval.txt","r") # opens a file for writing.
        interval = int(f.read())
        f.close()
        print(f"read interval: {interval}")
        return interval
    except:
        interval = 20
        print("Creating default interval file")
        storeInterval(interval)
        return interval


def storeInterval(interval):
    f=open("interval.txt","w") # opens a file for writing.
    f.write(str(interval))
    f.close()
    print(f"stored interval: {interval}")