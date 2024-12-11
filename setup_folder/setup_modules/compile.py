import os
import subprocess
import webbrowser
import pathlib

def check_python_existing() -> bool | dict:
    
    try:
        
        output = subprocess.run(['python','--version'])
        
        return True
        
    except FileNotFoundError as err:
        
        return {False:'Файл не найден'}
    
def install_python() -> None:

    try:
        
        webbrowser.open('https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe')

    except Exception as err:
        
        pass
    
def create_venv(path) -> None:
    
    try:
        
        os.chdir(path)
        
        output = subprocess.run(['python','-m','venv', '.venv'], check=True)
    
        return True
        
    except Exception as err:
        
        return False
    
def install_reqs(path_f: str) -> None:
    
    try:
        
        os.chdir(path_f)
        
        venv_path = pathlib.Path(path_f) / '.venv' / 'scripts' / 'activate'
        
        project_path = pathlib.Path(path_f) / 'CourseWork' / 'app_folder'
        
        requirements_file = project_path / 'requirements.txt'
    
        command = f"{venv_path} && pip install -r {requirements_file}"
        result = subprocess.run(
            command, shell=True, check=True
        )
        
        return True
        
    except Exception as err:
        
        return False
    
def compile_proj(path_f: str) -> None:
    
    try:
        
        os.chdir(path_f)
        
        venv_path = pathlib.Path(path_f) / '.venv' / 'scripts' / 'activate'
        
        project_path = pathlib.Path(path_f) / 'CourseWork' / 'app_folder'
        
        requirements_file = project_path / 'requirements.txt'
        
        main_file = project_path / 'startup.py'
    
        command = f"{venv_path} && pyinstaller --onefile {main_file}"
        result = subprocess.run(
            command, shell=True, check=True
        )
        
        return True
        
    except Exception as err:
        
        return False