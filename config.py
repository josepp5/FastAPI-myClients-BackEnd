from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import PrimaryKeyConstraint

from typing import List, Optional,Generic,TypeVar
from pydantic import BaseModel, Field, BaseSettings
from pydantic.generics import GenericModel


SQLALCHEMY_DATABASE_URL = "postgresql://root:root@localhost:5432/i.DEMO_GESTION_INTEGRAQS_S_L_.2023.0"

engine = create_engine(SQLALCHEMY_DATABASE_URL, client_encoding='utf8')
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

######################################### GENERATES SCHEMAS FROM BBDD TABLE ##########################################
# Crear un objeto de metadatos
metadata = MetaData()

# Obtener la tabla de la base de datos
customerTable = Table('\"CUSTOMER_CUS\"', metadata, autoload_with=engine)


# Obtener el esquema de la tabla
#CustomerSchema = repr(customerTable)

######################################### GENERATES MODEL/CLASS FROM BBDD TABLE ######################################
# Crear la base automap
Base = automap_base()

# Reflejar las tablas existentes
Base.prepare(engine, reflect=True, schema='public')


# Acceder a la tabla que quieres convertir en modelo
Customer = Base.classes.CUSTOMER_CUS


class Settings(BaseSettings):
    arbitrary_types_allowed = True



################################################### 1235232 INTENTOS DE AUTO-GENERAR MODEL Y SCHEMA ######################################
"""


engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear una sesión de SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Crear un objeto MetaData para representar la base de datos
metadata = MetaData()

# Reflejar la base de datos en el objeto MetaData
metadata.reflect(bind=engine)

# Crear una clase Base para utilizar en la definición de modelos
Base = declarative_base()

# Generar los modelos a partir de las tablas reflejadas en la base de datos
for table_name in metadata.tables.keys():
    class_name = ''.join(word.capitalize() for word in table_name.split('_'))
    table = Table('\"CUSTOMER_CUS\"', metadata, autoload=True, autoload_with=engine)
    
    # Auto-generar un esquema a partir de la tabla
    schema = {}
    for column in table.columns:
        column_type = str(column.type)
        if 'int' in column_type:
            schema[column.name] = int
        elif 'float' in column_type:
            schema[column.name] = float
        else:
            schema[column.name] = str

    # Auto-generar un modelo a partir de la tabla y el esquema
    model = type(class_name, (Base,), {
        '__tablename__': table_name,
        '__table__': table,
        '__table_args__': (
            PrimaryKeyConstraint(*[c.name for c in table.primary_key.columns]),
        ),
        **schema
    })

    # Agregar el modelo al namespace global
    globals()[class_name] = model

"""






