# Setup and installation

## Downloading Locally

In CMD(Command Prompt) go to a folder you want to download the files in then do the following command
git clone <https://github.com/noob-hash/Yantra_Swarmonoid-trainingMaterial.git>
![image](https://github.com/noob-hash/Yantra_Swarmonoid-trainingMaterial/assets/80933227/56562768-7bbc-47cf-8b24-d7366e4dfee2)
After the folder has been downloaded you can use VScode to open the downloaded folder.

You may have seen the .env environment in the code you can try to use the same environment but if it doesn't work delete that folder and create your environment.

## Creating environment

If you need to create a virtual environment you can do so in vs code or through the command prompt just ensure you have installed Python before.
The virtual environment ensures that all packages are bundled up and not mixed with another project meaning isolation.

Then use the following command to create a virtual environment

>Recommended to use Git Bash

```bash
 python -m venv <<environment_name>> 
 ```

e.g.

```bash
python -m venv env
```

## Using an environment

To use the created environment you just need to execute the activate file inside the environment simplest way to do it is:

```bash
.\<<environment_name>>\Scripts\activate.ps1
```

e.g.

>In Powershell

```bash
 .\env\Scripts\activate.ps1 
 ```

 >In git bash

 ```bash
 ./env/Scripts/ativate
 ```

If you get the following error
![image](https://github.com/noob-hash/Yantra_Swarmonoid-trainingMaterial/assets/80933227/6e6c6ec2-c5de-4244-9711-11a15b294f87)
Run PowerShell as administrator, you can find it by searching on the search bar
Then on PowerShell run the following command:

>In Powershell (in windows)

```bash
Set-ExecutionPolicy Unrestricted -Force
```

This will allow the running of scripts in the system.

## Installing Libaries

You need to install a few libraries to run these commands which are listed in the requirements.txt file. You can install all of them using the following command:

>In Powershell

```bash
pip install -r .\requirements.txt
```

>In git bash

```bash
pip install -r ./requirements.txt
```

Make sure the path to requirements.txt is correct.

## Other Errors

If you find an error when trying to run the Python code such as:
![image](https://github.com/noob-hash/Yantra_Swarmonoid-trainingMaterial/assets/80933227/dcd78b40-2c25-4600-ac60-2c2e30097289)

It means that you have not selected your environment's Python interpreter to select it you need to do the following:
In VS code press and hold: Ctrl + Shift + P
Here search for a Python interpreter like so:

![image](https://github.com/noob-hash/Yantra_Swarmonoid-trainingMaterial/assets/80933227/2919460d-7ccb-4c8a-bb5c-d36c43da883b)

There select the interpreter in your environment

![image](https://github.com/noob-hash/Yantra_Swarmonoid-trainingMaterial/assets/80933227/e52617a3-f859-4ed4-b019-d4b27a9bbc11)
