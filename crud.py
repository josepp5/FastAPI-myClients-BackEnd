from sqlalchemy.orm import Session
from config import Customer, CustomerSchema
#from schemas import CustomerSchema

def get_customer(db:Session,skip:int=0,limit:int=100):
    return db.query(Customer).offset(skip).limit(limit).all()


def get_customer_by_id(db:Session,customer_id: int):
    return db.query(Customer).filter(Customer.cus_id == customer_id).first()


def create_customer(db:Session,customer: CustomerSchema):
    _customer = Customer(
        cus_id=customer.cus_id,
        cus_corporatename=customer.cus_corporatename,
        cus_alias=customer.cus_alias,
        cus_entity=customer.cus_alias,
        cus_country=customer.cus_country
        )
    db.add(_customer)
    db.commit()
    db.refresh(_customer)
    return _customer

    
def remove_customer(db:Session, customer_id:int):
    _customer = get_customer_by_id(db=db,customer_id=customer_id)
    db.delete(_customer)
    db.commit()
    

def update_customer(db:Session, customer_id:int, name:str, age:int):
    _customer = get_customer_by_id(db=db,customer_id=customer_id)
    _customer.name = name
    _customer.age = age
    db.commit()
    db.refresh(_customer)
    return _customer