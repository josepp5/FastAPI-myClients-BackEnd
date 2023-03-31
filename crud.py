from sqlalchemy import Engine
from sqlalchemy.orm import Session
from config import Customer, customerTable
from schemas import CustomerSchema, RequestCustomer, Response

def get_customer(db:Session,skip:int=0,limit:int=100):
    customers: Customer[Customer] = db.query(Customer).offset(skip).limit(limit).all()
    for c in customers:
        decodeLogo(c); 
    return customers

def get_customer_by_id(db:Session,cus_id:int, toUpdate:bool):
    customer = db.query(Customer).filter(Customer.cus_id == cus_id).first()
    if toUpdate == False:
        decodeLogo(customer)
    return customer

def decodeLogo(c:Customer):
    try:
        c.cus_logo = c.cus_logo.decode('iso-8859-1')
    except Exception as e:
        c.cus_logo = "undefined"

def create_customer(db:Session,customer:CustomerSchema):
    _customer = Customer(
        cus_id=customer.cus_id,
        cus_corporatename=customer.cus_corporatename,
        cus_commercialname=customer.cus_commercialname,
        cus_entity=customer.cus_entity,    
        cus_alias=customer.cus_alias,
        cus_unknown=customer.cus_unknown,
        cus_country=customer.cus_country,
        cus_taxid=customer.cus_taxid,
        cus_taxidtype=customer.cus_taxidtype,
        cur_cus_fk=customer.cur_cus_fk,
        tas_cus_fk=customer.tas_cus_fk,
        pam_cus_fk=customer.pam_cus_fk,
        )
    
    db.add(_customer)
    db.commit()
    db.refresh(_customer)
    return _customer

def remove_customer(db:Session, cus_id:int):
    _customer = get_customer_by_id(db=db, cus_id=cus_id,toUpdate=False)
    db.delete(_customer)
    db.commit()
    
def update_customer(db:Session,
                    cus_id:int,
                    cus_corporatename:int,
                    cus_commercialname:int,
                    cus_entity:int,    
                    cus_alias:int,
                    cus_unknown:int,
                    cus_country:int,
                    cus_taxid:int,
                    cus_taxidtype:int,
                    cur_cus_fk:int,
                    tas_cus_fk:int,
                    pam_cus_fk:int):
    customer = get_customer_by_id(db=db,cus_id=cus_id, toUpdate=True)
    customer.cus_corporatename=cus_corporatename
    customer.cus_commercialname=cus_commercialname
    customer.cus_entity=cus_entity  
    customer.cus_alias=cus_alias
    customer.cus_unknown=cus_unknown
    customer.cus_country=cus_country
    customer.cus_taxid=cus_taxid
    customer.cus_taxidtype=cus_taxidtype
    customer.cur_cus_fk=cur_cus_fk
    customer.tas_cus_fk=tas_cus_fk
    customer.pam_cus_fk=pam_cus_fk
    db.commit()
    db.refresh(customer)
    return customer


