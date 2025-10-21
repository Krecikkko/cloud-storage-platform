# import time

# from typing import Annotated, Optional

# from fastapi import BackgroundTasks, Depends, FastAPI
# from fastapi.security import OAuth2PasswordBearer
# from pydantic import BaseModel

# app = FastAPI()

# timer = time.time()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# class User(BaseModel):
#     username: str
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     disabled: Optional[bool] = None

# def fake_decode_token(token):
#     return User(
#         username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
#     )

# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     if not token:
#         return None

#     user = fake_decode_token(token)
#     return user    

# def write_log(message: str):
#     with open("log.txt", "w") as file:
#         file.write(message + "\n")
#         file.close()

# def user_log(token: str, timer: float):
#     with open("log.txt", "w") as file:
#         if not get_current_user(token) == None:
#             User = get_current_user(token)
#             file.write("User: " + User + " logged in:" + timer + "\n")
#             file.close()
#         else: 
#             file.close()



