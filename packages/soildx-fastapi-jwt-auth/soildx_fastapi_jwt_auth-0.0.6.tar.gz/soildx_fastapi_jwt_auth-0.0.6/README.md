
# soildx-jwt-auth

This is a fastapi jwt simple authentication.

## Installation
* Here are some prerequisites for installing **soildx-fastapi-jwt-auth** packages:
    ```
    pip install python-jose[cryptography]
    ```
    ```
    pip install passlib[bcrypt]
    ```

* Install with **pip**:
    ```
	    pip install soildx-fastapi-jwt-auth
    ```

## Usage

##### * Endpoint for generating a token
```
from  fastapi  import  APIRouter, Depends, Request, status, HTTPException

#soildx_fastapi_jwt_auth package import
from  soildx_fastapi_jwt_auth.jwt_auth  import  create_token, check_access_token, get_hashed_password, verify_password

# Endpoint for generating a token
@router.post("/auth_token")
async  def  login(info: Request):
    req_info = await  info.json()
    email = req_info.get('email')
    password = req_info.get('password')
    #check if user and password match in db in Authenticate function
    user = await  Authenticate(email, password)
    if  user  is  None:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return {"access_token": create_token(user), "token_type": "Bearer token"}
```
##### *  test auth view
```
#test auth view. You need to pass headers = {"Authorization": f"Bearer {token}"}
@router.get("/test_auth_view", dependencies=[Depends(check_access_token)])
async  def  test():
	return {"Granted": True}
```
##### * Authenticate function
```
async  def  Authenticate(email:str, password:str) -> dict:
	SQL = f"SELECT email FROM users WHERE email = :email AND password = :password;"
	res = await  db_get('db_name', SQL, {"email":email, "password":password})
	rows = [r._mapping  for  r  in  res]
	return  rows[0]['email'] if  rows  else  None
```
    


#### What Am I Working Next?
I will be working on the issues below. Anyone is welcome to contribute.

> -   hash password.
 
 