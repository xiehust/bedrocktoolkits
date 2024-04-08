#create a funtion to generate random Id with format as "id-xxxx"
import random
def generate_id():
    id = "id-"+str(random.randint(1000,9999))
    return id

#get the current time
import datetime
def get_current_time():
    current_time = datetime.datetime.now()
    return current_time