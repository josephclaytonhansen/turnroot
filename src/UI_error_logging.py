import inspect, datetime
reset = False
def errorLog(e):
    filename = inspect.stack()[1].filename 
    with open("src/errors.txt", "a") as f:
        f.write("Error from caller '" + filename + "' using function '"+ inspect.stack()[1].function+"': '"+str(e)+"'\n")
        
def resetEl():
    global reset
    if reset == False:
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open("src/errors.txt", "w") as f:
            f.truncate()
            f.write("==========Turnroot instance started at "+now+"==========\n")
        reset = True
