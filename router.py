from fastapi import APIRouter,HTTPException, Path, Depends
from config import SessionLocal, Settings, Customer
from sqlalchemy.orm import Session
from schemas import RequestCustomer,Response #,CustomerSchema
import crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
       
@router.post('/create')
async def created(request:RequestCustomer,db:Session=Depends(get_db)):
    crud.create_customer(db,request.parameter)
    return Response(code=200,status="Ok",message="Customer created successfully").dict(exclude_none=True)

@router.get('/')
async def get(db:Session=Depends(get_db)):
    _customer = crud.get_customer(db,0,100)
    return Response(code=200,status="Ok",message="Success Fecth all data", result=_customer).dict(exclude_none=True)

@router.get('/{id}')
async def get_by_id(id:int,db:Session=Depends(get_db)):
    _customer = crud.get_customer_by_id(db,id)
    print(_customer)
    return Response(code=200,status="Ok",message="Success get data", result=_customer).dict(exclude_none=True)

@router.post("/update")
async def update_customer(request:RequestCustomer,db:Session=Depends(get_db)):
    _customer = crud.update_customer(
        db,
        cus_id=request.parameter.cus_id,
        cus_corporatename=request.parameter.cus_corporatename,
        cus_commercialname=request.parameter.cus_commercialname,
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

@router.delete("/{id}")
async def get(id:int,db:Session=Depends(get_db)):
    crud.remove_customer(db,customer_id=id)
    return Response(code=200,status="Ok",message="Success delete data").dict(exclude_none=True)


@router.get("/clienteImg/{cliente_id}")
async def obtener_cliente(cliente_id: int,db:Session=Depends(get_db)):
    # Obtener el cliente de la base de datos
    _customer = crud.get_customer_by_id(db,cliente_id)
    
    # Devolver la imagen en formato bytea
    return _customer.cus_logo
    
