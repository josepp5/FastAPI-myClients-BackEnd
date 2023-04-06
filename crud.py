from sqlalchemy import Engine, null, or_
from sqlalchemy.orm import Session
from fastapi import APIRouter, Path, Depends,status
from config import Customer, Country, TaxSystem, PaymentMethod
from jwt_auth_users import auth_user, oauth2
from schemas import CustomerSchema, RequestCustomer, Response


################### CRUD CUSTOMERS ######################
def get_customers(db:Session,skip:int=0,limit:int=100):
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
        cca_cus_fk=customer.cca_cus_fk,
        cus_entity=customer.cus_entity,    
        cus_alias=customer.cus_alias,
        cus_unknown=customer.cus_unknown,
        cus_country=customer.cus_country,
        cus_taxid=customer.cus_taxid,
        cus_taxidtype=customer.cus_taxidtype,
        cur_cus_fk=customer.cur_cus_fk,
        tas_cus_fk=customer.tas_cus_fk,
        pam_cus_fk=customer.pam_cus_fk
        )
    
    db.add(_customer)
    db.commit()
    db.refresh(_customer)
    return _customer

def remove_customer(db:Session, cus_id:int):
    _customer = get_customer_by_id(db=db, cus_id=cus_id,toUpdate=False)
    db.delete(_customer)
    db.commit()
    
def update_customer(db,
                    cus_id:int,
                    cus_corporatename:str,
                    cus_commercialname:str,
                    cca_cus_fk:int,
                    cus_entity:int,    
                    cus_alias:str,
                    cus_unknown:bool,
                    cus_country:str,
                    cus_taxid:str,
                    cus_taxidtype:str,
                    cur_cus_fk:int,
                    tas_cus_fk:int,
                    pam_cus_fk:int):
    customer = get_customer_by_id(db=db,cus_id=cus_id, toUpdate=True)
    customer.cus_corporatename=cus_corporatename
    customer.cus_commercialname=cus_commercialname
    customer.cca_cus_fk=cca_cus_fk
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

################### Search bar Filter ###################

def get_customer_by_corporatename(db:Session,cus_corporatename:str, toUpdate:bool):
    customer = db.query(Customer).filter(or_(Customer.cus_corporatename.ilike(f'%{cus_corporatename}%'))).first()
    if toUpdate == False:
        decodeLogo(customer)
    return customer

################### COUNTRIES ############################

def get_countries(db:Session,skip:int=0,limit:int=250):
    countries: Country[Country] = db.query(Country).offset(skip).limit(limit).all()
    for c in countries:
        decodeFlag(c); 
    return countries

def decodeFlag(c:Country):
    try:
        c.cou_flag = c.cou_flag.decode('iso-8859-1')
    except Exception as e:
        c.cou_flag = "undefined"

################### TAX SYSTEMS TAS ######################

def get_taxsystems(db:Session,skip:int=0,limit:int=100):
    taxsystems: TaxSystem[TaxSystem] = db.query(TaxSystem).offset(skip).limit(limit).all()
    return taxsystems

################### PAYMENT METHODS #######################

def get_paymentMethods(db:Session,skip:int=0,limit:int=100):
    paymentMethods: PaymentMethod[PaymentMethod] = db.query(PaymentMethod).offset(skip).limit(limit).all()
    return paymentMethods