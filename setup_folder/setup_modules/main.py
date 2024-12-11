import os
import subprocess
import webbrowser

def check_git() -> bool | dict:
    
    try:
        
        output = subprocess.run(['git','--version'])
        
        return True
        
    except FileNotFoundError as err:
        
        return {False:'Файл не найден'}
    

def check_internet_connection() -> bool | None:
    
    try:
        
        output = subprocess.Popen('ping google.com')
        
        if output.poll():
            
            return False
        
        else:
            
            return True
        
    except Exception as err:
        
        pass
    
def install_git() -> None:
    
    try:
        
        webbrowser.open('https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.1/Git-2.47.1-64-bit.exe')
    
    except Exception as err:
        
        pass

def project_install(path: str) -> bool:
    
    try:
        
        os.chdir(path)
        
        output = subprocess.run(['git', 'clone', 'https://github.com/Vanek1ch/CourseWork.git'])
        
        return True
        
    except Exception as err:
        
        return False