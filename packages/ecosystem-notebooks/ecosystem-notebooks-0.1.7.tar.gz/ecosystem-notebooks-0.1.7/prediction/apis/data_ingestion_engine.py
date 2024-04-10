from prediction.endpoints import data_ingestion_engine as endpoints
from prediction import request_utils

def add_metadocumemnts(auth, meta_documents, info=False):
    ep = endpoints.ADD_META_DOCUMENTS
    resp = request_utils.create(auth, ep, json=meta_documents, info=info)
    response = resp.json()
    return response

def delete_ingestmeta(auth, ingest_meta, info=False):
    ep = endpoints.DELETE_INGEST_META
    resp = request_utils.create(auth, ep, json=ingest_meta, info=info)
    response = resp.json()
    return response	

def get_databasesmeta(auth, info=False):
    ep = endpoints.GET_DATABASES_META
    resp = request_utils.create(auth, ep, info=info)
    meta = resp.json()
    if "data" in meta:
        meta = meta["data"]
    return meta

def get_databasetablecolumnmeta(auth, databasename, tablename, columnname, info=False):
    ep = endpoints.GET_DATABASE_TABLE_COLUMN_META
    param_dict = {
        "databasename": databasename,
        "tablename": tablename,
        "columnname": columnname
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    if "data" in meta:
        meta = meta["data"]
    return meta

def get_databasetablecolumnsmeta(auth, databasename, tablename, info=False):
    ep = endpoints.GET_DATABASE_TABLE_COLUMNS_META
    param_dict = {"databasename": databasename, "tablename": tablename}
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    if "data" in meta:
        meta = meta["data"]
    return meta

def get_databasetablesmeta(auth, databasename, info=False):
    ep = endpoints.GET_DATABASES_TABLES_META
    param_dict = {"databasename": databasename}
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    if "data" in meta:
        meta = meta["data"]
    return meta

def get_ingestmeta(auth, ingest_name, info=False):
    ep = endpoints.GET_INGEST_META
    param_dict = {"ingest_name": ingest_name}
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    if "data" in meta:
        meta = meta["data"]
    return meta

def get_ingestmetas(auth, info=False):
    ep = endpoints.GET_INGEST_METAS
    resp = request_utils.create(auth, ep, info=info)
    meta = resp.json()
    if "data" in meta:
        meta = meta["data"]
    return meta

def save_databasetablecolumn(auth, database_table_column_json, info=False):
    ep = endpoints.SAVE_DATABASE_TABLE_COLUMN_META
    resp = request_utils.create(auth, ep, json=database_table_column_json, info=info)
    response = resp.json()
    return response

def save_ingestion(auth, ingestion_json, info=False):
    ep = endpoints.SAVE_INGEST_META
    resp = request_utils.create(auth, ep, json=ingestion_json, info=info)
    response = resp.json()
    return response