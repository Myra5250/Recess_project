import sys
import os

#Path to my project
project_home = os.path.dirname(os.path.dirname(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

#  Import your factory and create the app
from app import create_app
application = create_app() #Passenger needs this application