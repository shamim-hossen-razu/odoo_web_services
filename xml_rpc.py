
# Odoo is usually extended internally via modules, but many of its features and all of its data are also available from the outside
# for external analysis or integration with various tools. Part of the Models API is easily available over XML-RPC and accessible 
# from a variety of languages.

# in this example we will use the xmlrpc.client library to connect to an Odoo instance and interact with the united_medical.patients model.

import xmlrpc.client

# connection parameters
url = 'http://localhost:8017' # where the Odoo instance is running
db = 'odoo_17_db' # the database
username = 'admin' # the user
password = 'admin' # the password

#  endpoint 1: common
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

print('Connected Used id : ', uid)

# endpoint 2: object
# The second endpoint is xmlrpc/2/object. It is used to call methods of odoo models via the execute_kw RPC function.
# Each call to execute_kw takes the following parameters:
    # 1. the database name 
    # 2. the user id (retrieved through authenticate), an integer
    # 3. the user’s password, a string
    # 4. the model name, a string
    # 5. the method name, a string
    # 6. an array/list of parameters passed by position
    # 7. a mapping/dict of parameters to pass by keyword (optional) 


models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


# Search the model data and get the ids
model_name = 'united_medical.patients'
# check weather the user has read access to the model
access = models.execute_kw(db, uid, password, model_name, 'check_access_rights', ['read'], {'raise_exception': False})
if not access:
    print('No read access to the model')
    exit()
else:
    print('User has Read access to the model')

    ### Method 1: search ( only returns the ids of the records that match the search criteria)
    # ids = models.execute_kw(1 ,2 ,3 ,4 ,5 ,6 ,7)
    ids = models.execute_kw(db, uid, password, model_name, 'search', [[]], {'offset': 0, 'limit': 5})
    print('Patient ids : ', ids)

    ### Method 2: search_count (returns the number of records that match the search criteria)
    count = models.execute_kw(db, uid, password, model_name, 'search_count', [[]])
    print('Patient count : ', count)

    # male patients
    count = models.execute_kw(db, uid, password, model_name, 'search_count', [[['gender', '=', 'male']]])
    print('Male Patient count : ', count)

    count = models.execute_kw(db, uid, password, model_name, 'search_count', [[['gender', '=', 'female']]])
    print('Female Patient count : ', count)

    ### Method 3: read (returns every field of the records with given ids)
    records = models.execute_kw(db, uid, password, model_name, 'read', [ids])
    
    # If you want only some seleted fields to read then you can pass the fields in the last parameter
    records = models.execute_kw(db, uid, password, model_name, 'read', [ids], {'fields': ['name', 'gender']})

    # note Even if the id field is not requested, it is always returned.

    ### Method 4: fields_get (returns the definition of the fields of the model)
    fields = models.execute_kw(db, uid, password, model_name, 'fields_get', ['name'], {'attributes': ['string', 'help', 'type']})

    ### Method 5: search_read (combines search and read in a single call)
    records = models.execute_kw(db, uid, password, model_name, 'search_read', [[]], {'fields': ['name', 'gender'], 'limit': 5})
    
    ### Method 6: create (creates a new record)
    new_patient_id = models.execute_kw(db, uid, password, model_name, 'create', [{'name': 'John Doe', 'gender' : 'male'}])
    print('New Patient id : ', new_patient_id)
    record = models.execute_kw(db, uid, password, model_name, 'read', [new_patient_id], { 'fields':['name' , 'gender']})
    print('New Patient Record : ', record, )

    ### Method 7: write (updates records)
    updated_record_id = models.execute_kw(db, uid, password, model_name, 'write', [[new_patient_id], {'name': 'John desela', 'gender' : 'female'}])
    record = models.execute_kw(db, uid, password, model_name, 'read', [new_patient_id], { 'fields':['name', 'gender']})
    print('Updated Patient Record : ', record)

    ### Method 8: unlink (deletes records)
    deleted_record_id = models.execute_kw(db, uid, password, model_name, 'unlink', [[new_patient_id]])
    print('Deleted Patient Record id : ', deleted_record_id)
    record = models.execute_kw(db, uid, password, model_name, 'read', [new_patient_id], { 'fields':['name', 'gender']})
    print(record)

    




