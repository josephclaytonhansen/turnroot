import inspect, datetime, platform, os, sys
reset = False
sys.stdout = open("src/errors.txt", 'a')
def errorLog(e):
    filename = inspect.stack()[1].filename 
    with open("src/errors.txt", "a") as f:
        f.write("Error from caller '" + filename + "' using function '"+ inspect.stack()[1].function+"': '"+str(e)+"'\n")
        
def resetEl():
    global reset
    if reset == False:
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        size = os.path.getsize("src/errors.txt")
        print(size)
        if size > 12640:
            with open("src/errors.txt", "w") as f:
                f.truncate()
                f.write("==========Turnroot instance at "+now+"==========\n=========="+platform.platform()+"==========\n")
        else:
            with open("src/errors.txt", "a") as f:
                f.write("\n\n\n==========Turnroot instance at "+now+"==========\n=========="+platform.platform()+"==========\n")
        reset = True
