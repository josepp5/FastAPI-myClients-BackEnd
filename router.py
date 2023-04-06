from fastapi import APIRouter,Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from jwt_auth_users import oauth2
from schemas import RequestCustomer,Response
import crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
########################### CUSTOMER CRUD ##########################

@router.post('/customer/create')
async def create(request:RequestCustomer,db:Session=Depends(get_db),token: str = Depends(oauth2)):
    crud.create_customer(db,request.parameter)
    return Response(code=200,status="Ok",message="Customer created successfully").dict(exclude_none=True)

@router.get('/customer')
async def get_customer(db:Session=Depends(get_db),token: str = Depends(oauth2)):
    _customerlist = crud.get_customers(db,0,100)
    return Response(code=200,status="Ok",message="Success Fecth all data", result=_customerlist).dict(exclude_none=True)

@router.get('/customer/{cus_id}')
async def get_by_id(cus_id:int,db:Session=Depends(get_db),token: str = Depends(oauth2)):
    _customer = crud.get_customer_by_id(db,cus_id,False)
    return Response(code=200,status="Ok",message="Success get data", result=_customer).dict(exclude_none=True)

@router.put("/customer/{cus_id}")
async def update_customers(cus_id:int,request:RequestCustomer,db:Session=Depends(get_db),token: str = Depends(oauth2)):
    _customer = crud.update_customer(
        db,
        cus_id=cus_id,
        cus_corporatename=request.parameter.cus_corporatename,
        cus_commercialname=request.parameter.cus_commercialname,
        cca_cus_fk=request.parameter.cca_cus_fk,
        cus_entity=request.parameter.cus_entity,    
        cus_alias=request.parameter.cus_alias,
        cus_unknown=request.parameter.cus_unknown,
        cus_country=request.parameter.cus_country,
        cus_taxid=request.parameter.cus_taxid,
        cus_taxidtype=request.parameter.cus_taxidtype,
        cur_cus_fk=request.parameter.cur_cus_fk,
        tas_cus_fk=request.parameter.tas_cus_fk,
        pam_cus_fk=request.parameter.pam_cus_fk,
        )
    return Response(code=200,status="Ok",message="Success update data", result=_customer)

@router.delete("/customer/{cus_id}")
async def get_by_id(cus_id:int,db:Session=Depends(get_db),token: str = Depends(oauth2)):
    crud.remove_customer(db,cus_id)
    return Response(code=200,status="Ok",message="Success delete data").dict(exclude_none=True)

@router.get("/customer/clienteImg/{cliente_id}")
async def obtener_cliente(cliente_id: int,db:Session=Depends(get_db)):
    # Obtener el cliente de la base de datos
    _customer = crud.get_customer_by_id(db,cliente_id,False)
    
    # Devolver la imagen en formato bytea
    return _customer.cus_logo


@router.get('/customer_by_corporatename/{cus_corporatename}')
async def get_by_corporatename(cus_corporatename:str,db:Session=Depends(get_db),token: str = Depends(oauth2)):
    _customer = crud.get_customer_by_corporatename(db,cus_corporatename,False)
    return Response(code=200,status="Ok",message="Success get data", result=_customer).dict(exclude_none=True)
    
############################ GET COUNTRIES ####################### 

@router.get('/countries')
async def get_country(db:Session=Depends(get_db),token: str = Depends(oauth2)):
    _countries = crud.get_countries(db,0,250)
    return Response(code=200,status="Ok",message="Success Fecth all data", result=_countries).dict(exclude_none=True)

############################ GET TAX SYSTEMS ######################

@router.get('/taxsystems')
async def get_taxsystem(db:Session=Depends(get_db),token: str = Depends(oauth2)):
    _taxsystem = crud.get_taxsystems(db,0,100)
    return Response(code=200,status="Ok",message="Success Fecth all data", result=_taxsystem).dict(exclude_none=True)

########################### GET #################################

@router.get('/paymentMethods')
async def get_paymentmethod(db:Session=Depends(get_db),token: str = Depends(oauth2)):
    _paymentMethods = crud.get_paymentMethods(db,0,100)
    return Response(code=200,status="Ok",message="Success Fecth all data", result=_paymentMethods).dict(exclude_none=True)

######################## GraphQL ############################