import time
def wakeup(minutes, seconds):
    if not minutes == "" and not seconds == "":
        print("both")
        hm = 0
        hm = minutes * 60 + seconds
        #print(hm)
        time.sleep(hm)
        print("hello")
    elif minutes == "" and not seconds == "":
        print("seconds")
        hm = 0
        hm = seconds
        #print(hm)
        time.sleep(hm)
        print("hello")
    elif not minutes == "" and seconds == "":
        print("minutes")
        hm = 0
        hm = minutes * 60
        #print(hm)
        time.sleep(hm)
        print("hello")
    else:   print(2)