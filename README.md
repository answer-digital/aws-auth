## Installation
### Clone the repo
    git clone git@github.com:answer-digital/aws-auth.git
     
    # or if you have to specify your ssh key
    git clone git@github.com:answer-digital/aws-auth.git --config core.sshCommand="ssh -i ~/.ssh/specific_ssh_file"

### Create your venv
`python -m venv venv`

### Activate the venv
    # Windows cmd.exe
    venv/Scripts/activate.bat

    # Windows Powershell
    venv/Scripts/Activate.ps1

    # Mac/Ubuntu
    source venv/bin/activate

### Install the required packages
`pip install -r requirements.txt`

### Deactivate the venv
`deactivate`


## Running
    # Windows
    ./venv/Scripts/python.exe main.py

    # Mac/Ubuntu
    ./venv/bin/python main.py