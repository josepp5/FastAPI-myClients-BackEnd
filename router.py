from fastapi import APIRouter,HTTPException, Path, Depends
from config import SessionLocal #CustomerSchema
from sqlalchemy.orm import Session
from schemas import RequestCustomer,Response,CustomerSchema
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
    return Response(code=200,status="Ok",message="Success get data", result=_customer).dict(exclude_none=True)

@router.post("/update")
async def update_customer(request:RequestCustomer,db:Session=Depends(get_db)):
    _customer = crud.update_customer(db,customer_id=request.parameter.cus_id,name=request.parameter.cus_comercialname,country=request.parameter.cus_country)
    return Response(code=200,status="Ok",message="Success update data", result=_customer)

@router.delete("/{id}")
async def get(id:int,db:Session=Depends(get_db)):
    crud.remove_customer(db,customer_id=id)
    return Response(code=200,status="Ok",message="Success delete data").dict(exclude_none=True)
    


