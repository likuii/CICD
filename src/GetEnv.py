# Get
import os



if(os.environ["USER"]):
    user = os.environ["USER"]
    print(user)
if(os.environ["PASSWORD"]):
    password = os.environ["PASSWORD"]
if(os.environ["HOST"]):
    host = os.environ["HOST"]
