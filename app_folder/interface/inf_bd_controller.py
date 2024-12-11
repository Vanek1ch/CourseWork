import uuid
import hashlib
import datetime

from sqlmodel import SQLModel, Session, select
from sqlalchemy import create_engine
from interface.inf_bd_models import Users, Role
        
class Database:
    
    def __init__(self, db_path="interfacedb.db") -> None:
        self.predefined_roles: dict[str, int] = {'user':1,'admin':0,'other_role':2}
        sqlite_url = f"sqlite:///{db_path}"
        self.engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

    def get_session(self) -> Session:
        return Session(self.engine)

    def init_db(self) -> None:
        
        SQLModel.metadata.create_all(self.engine, checkfirst=True)
        
        session = self.get_session()
        
        try:
            
            for key, value in self.predefined_roles.items():
                existing_role = session.exec(select(Role).where(Role.id == value)).first()
                if not existing_role:
                    new_role = Role(id=value, name=key)
                    session.add(new_role)
            session.commit()
            
        except Exception as err:
            pass
        
def create_user(name: str, password: str) -> bool:
    controller = Database()
    controller.init_db()
    session = controller.get_session()

    try:
        user_get = session.exec(select(Users).where(Users.nickname == name)).first()
        if not user_get:
            dt = datetime.datetime.now()
            hashed_password = hashlib.sha256(password.encode('utf-8') + str(dt).encode('utf-8')).hexdigest()
            
            new_user = Users(
                id=uuid.uuid4(),
                nickname=name,
                password=hashed_password,
                created_at=dt,
                role_id=1
            )
            session.add(new_user)
            session.commit()
            
            return True
        else:
            return False
        
    except Exception as err:
        
        pass
    
    finally:
        
        session.close()
        
def login_user(name:str, password:str) -> dict[bool, str]:
    
    controller = Database()
    controller.init_db()
    session = controller.get_session()
    
    try:
    
        user_get = session.exec(select(Users).where(Users.nickname == name)).first()
        
        if not user_get:
            
            return {False:'Неверный логин или пароль!'}
        
        else:
            
            dt = user_get.created_at
            
            hashed_password = hashlib.sha256(password.encode('utf-8') + str(dt).encode('utf-8')).hexdigest()
            
            if user_get.password != hashed_password:
                
                return {False:'Неверный логин или пароль!'}
            
            else:
                
                return {True:'user_get.role'}
            
    except Exception as err:
        
        pass