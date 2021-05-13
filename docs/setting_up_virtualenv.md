# Setting up your Connectoma Virtual Environment
- Lets create a virtual environment that our application would work on.  We do this to avoid complications that could arise due to updates, version and package related issues that could arise due to differences in user's personal setup.

- Install the package **virtualenv** using the pip command

  ```powershell
     pip install virtualenv
  ```

- In our root directory, use the following command to create a virtual environment with the name **my-venv**

  ```powershell
  python3 -m venv my-venv
  ```

- Activate the environment by running the command

  ```powershell
  my-venv\Scripts\activate.bat #for windows terminal
  ```

  ```unix
  source my-venv/Scripts/activate #for unix
  ```

- Activating the virtual environment will change your shell’s prompt to show what virtual environment you’re using, and modify the environment so that running `python` will get you that particular version and installation of Python.

- You can identify that you are in the virtual environment by noticing the ```(my-venv)``` in the beginning of the terminal prompt

- Don't forget to deactivate the virtual environment by using the command

  ```python
  deactivate
  ```


## Installing relevant pip packages

- Install all packages we require to the virtual environment

- Freeze the package list to **requirements.txt **by running the following command

- ```python
  pip freeze > requirements.txt
  ```

#### Useful pip commands

```powershell
 pip search flask
 pip show flask
 pip list
 pip freeze > requirements.txt
```