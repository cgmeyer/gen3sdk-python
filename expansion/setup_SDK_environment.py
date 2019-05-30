### RUN IN JUPYTER
# # Install gen3sdk via pip
!pip install --force --upgrade gen3 --ignore-installed certifi
#
# Import some Python packages
import requests, json, fnmatch, os, os.path, sys, subprocess, glob, ntpath, copy, re
import pandas as pd
from pandas.io.json import json_normalize
from collections import Counter

import gen3
from gen3.auth import Gen3Auth
from gen3.submission import Gen3Submission
from gen3.file import Gen3File

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Create the gen3sdk objects for authentication and submission
api = 'https://datacommons.org'
profile = 'prof'
client = '/home/jovyan/.gen3/gen3-client'
creds = '/home/jovyan/pd/my-credentials.json'

auth = Gen3Auth(api, refresh_file=creds)
sub = Gen3Submission(api, auth)
file = Gen3File(api, auth)

# Download and configure gen3-client in Jupyter Notebook
!curl https://api.github.com/repos/uc-cdis/cdis-data-client/releases/latest | grep browser_download_url.*linux |  cut -d '"' -f 4 | wget -qi -
!unzip dataclient_linux.zip
!mkdir /home/jovyan/.gen3
!mv gen3-client /home/jovyan/.gen3
!rm dataclient_linux.zip
#!/home/jovyan/.gen3/gen3-client configure --profile=bpa --apiendpoint=https://data.bloodpac.org --cred=/home/jovyan/pd/bpa-credentials.json
cmd = client +' configure --profile='+profile+' --apiendpoint='+api+' --cred='+creds
try:
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode('UTF-8')
except Exception as e:
    output = e.output.decode('UTF-8')
    print("ERROR:" + output)
print(subprocess.check_output(client).decode('UTF-8')) #check that installation is complete


### Run Locally:
## Import some Python packages
import requests, json, fnmatch, os, os.path, sys, subprocess, glob, ntpath
import pandas as pd
from pandas.io.json import json_normalize
from collections import Counter

import gen3
from gen3.auth import Gen3Auth
from gen3.submission import Gen3Submission
from gen3.file import Gen3File

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

## Download and configure gen3-client in Jupyter Notebook

profile = 'bpa'
api = 'https://data.bloodpac.org/' # BloodPAC
creds = '/Users/christopher/Downloads/bpa-credentials.json'

profile = 'bc'
api = 'https://data.braincommons.org/' # BRAIN Commons
creds = '/Users/christopher/Downloads/bc-credentials.json'

# api = 'https://nci-crdc-demo.datacommons.io/' # DCF  SAndbox Commons
# profile = 'dcf'
# creds = '/Users/christopher/Downloads/dcf-credentials.json'

#api = 'https://dcf-interop.kidsfirstdrc.org/' #Kids First

#profile = 'stage'
#api = 'https://gen3.datastage.io/' # STAGE (old "DCP")
#creds = '/Users/christopher/Downloads/stage-credentials.json'

api = 'https://vpodc.org/' # VA
profile = 'vpodc'
creds = '/Users/christopher/Downloads/vpodc-credentials.json'


client = 'gen3-client'

auth = Gen3Auth(api, refresh_file=creds)

#load /Users/christopher/Documents/GitHub/cgmeyer/gen3sdk-python/gen3/submission.py
load /Users/christopher/Documents/GitHub/uc-cdis/gen3sdk-python/gen3/submission.py

sub = Gen3Submission(api, auth)


cmd = client +' configure --profile='+profile+' --apiendpoint='+api+' --cred='+creds
try:
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode('UTF-8')
except Exception as e:
    output = e.output.decode('UTF-8')
    print("ERROR:" + output)
print(subprocess.check_output(client).decode('UTF-8')) #check that installation is complete
