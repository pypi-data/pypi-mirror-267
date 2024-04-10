from runtime.endpoints import worker_utilities as endpoints
from runtime import request_utils

def send_get(auth, path, proxy, port, info=False):
    ep = endpoints.SEND_GET
    param_dict = {
        "path": path, 
        "proxy": proxy,
        "port": port
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def get_rest(auth, path, info=False):
    ep = endpoints.GET_REST
    param_dict = {
        "path": path
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def get_cassandra(auth, sql, c_type, info=False):
# Cassandra database select
#   auth: Authentication token generated by access.Authenticate()
#   sql: select sql target. Default value: select release_version from system.local
#   c_type: Default value: c OR r
    ep = endpoints.GET_CASSANDRA
    param_dict = {
        "sql": sql, 
        "type": c_type
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def get_cassandra_version(auth, params, info=False):
# Cassandra database version
#   auth: Authentication token generated by access.Authenticate()
#   params: (string)
    ep = endpoints.GET_CASSANDRA_VERSION
    param_dict = {
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def get_file(auth, file_name, lines, info=False):
# Obtain log file: Retrive number of lines from file.
#   auth: Authentication token generated by access.Authenticate()
#   file_name: file to read (str)
#   lines: number of lines to read (int)
    ep = endpoints.GET_FILE
    param_dict = {
        "file": file_name, 
        "lines": lines
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def get_file_list(auth, info=False):
    ep = endpoints.GET_FILE_LIST
    resp = request_utils.create(auth, ep, info=info)
    meta = resp.json()
    return meta

def get_ip(auth, info=False):
# Get IP of server.
#   auth: Authentication token generated by access.Authenticate()
    ep = endpoints.GET_IP
    resp = request_utils.create(auth, ep, info=info)
    meta = resp.json()
    return meta

def get_rest(auth, path, info=False):
# REST Interface: 
#    auth: Authentication token generated by access.Authenticate()
#    path: '-noData -u user -p pass http://lo...' 
#    use the -noData option to indicate the use of ecosystem API. 
#    Define user and password for authentication with -u and -p path='-key result -u user -p pass http://lo...' 
#    use the -key [keyvalue] option to indicate the use of API where document is in JSON key.
    ep = endpoints.GET_REST
    param_dict = {
        "path": path
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def list_to_matrix(auth, params, info=False):
# Create matrix from transcation list from properties file as setup in budget tracker.
#   auth: Authentication token generated by access.Authenticate()
#   params: {type:'csv'} or {type:'json'}
    ep = endpoints.LIST_TO_MATRIX
    param_dict = {
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def matrix_to_list(auth, params, info=False):
# Create list from matrix, import csv file.
#   auth: Authentication token generated by access.Authenticate()
#   params: {test: true, file:'./file.csv'} (use test setting to check before update)
    ep = endpoints.MATRIX_TO_LIST
    param_dict = {
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def pull_kafka_topic(auth, message, params, info=False):
# Pull message from Kafka topic
#   auth: Authentication token generated by access.Authenticate()
#   message: Default value : [{}]
#   params: Default value : [{"TOPIC_NAME":"ecosystem1","log":"true"}]
    ep = endpoints.PULL_KAFKA_TOPIC
    param_dict = {
        "message": message, 
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def push_kafka_topic(auth, message, params, info=False):
    ep = endpoints.PULL_KAFKA_TOPIC
    param_dict = {
        "message": message, 
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def upload_file(auth, path, target_path, info=False):
    ep = endpoints.UPLOAD_FILE
    fileFp = open(path, "rb")
    files = {"file": fileFp}
    data = {"path": target_path}
    resp = request_utils.create_only_auth(auth, ep, data=data, files=files, info=info)
    return resp

def file_database_import(auth, database, collection, file_name, info=False):
    ep = endpoints.FILE_DATABASE_IMPORT
    param_dict = {
        "database": database,
        "collection": collection,
        "file": file_name
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def get_property(auth, property_key, info=False):
	ep = endpoints.GET_PROPERTY
	param_dict = {
		"key": property_key
	}
	resp = request_utils.create_only_auth(auth, ep, params=param_dict, info=info)
	data = resp.content.decode("utf-8")
	return data

def update_properties(auth, properties, info=False):
    ep = endpoints.UPDATE_PROPERTIES
    resp = request_utils.create_only_auth(auth, ep, data=properties, info=info)
    return resp

def update_properties_key(auth, key, value, info=False):
	ep = endpoints.UPDATE_PROPERTIES_KEY
	param_dict = {
		"key": key,
		"value": value
	}
	resp = request_utils.create_only_auth(auth, ep, params=param_dict, info=info)
	data = resp.content.decode("utf-8")
	return data

def refresh(auth, info=False):
    ep = endpoints.REFRESH
    resp = request_utils.create(auth, ep, info=info)
    meta = resp.content
    return meta

def get_spend_personality(auth, campaign, channel, customer, params, subcampaign, userid, info=False):
    ep = endpoints.GET_SPEND_PERSONALITY
    param_dict = {
      "campaign": campaign,
      "channel": channel, 
      "customer":customer, 
      "params":params, 
      "subcampaign":subcampaign, 
      "userid":userid}
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta


def get_financial_wellness(auth, campaign, channel, customer, params, subcampaign, userid, info=False):
    ep = endpoints.GET_FINANCIAL_WELLNESS
    param_dict = {"campaign": campaign,
                  "channel": channel, 
                  "customer":customer, 
                  "params":params, 
                  "subcampaign":subcampaign, 
                  "userid":userid}
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def put_financial_wellness(auth, document, info=False):
    ep = endpoints.PUT_FINANCIAL_WELLNESS
    param_dict = {
        "document": document,
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def sql_cassandra(auth, sql, info=False):
    ep = endpoints.SQL_CASSANDRA
    param_dict = {
        "sql": sql,
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta


def close_cassandra(auth, info=False):
    ep = endpoints.CLOSE_CASSANDRA
    resp = request_utils.create(auth, ep, info=info)
    meta = resp.content
    return meta	


def test_kafka_kerberos(auth, info=False):
    ep = endpoints.TEST_KAFKA_KERBEROS
    resp = request_utils.create(auth, ep, info=info)
    meta = resp.content
    return meta	
    

def estore_recommendations(auth, msisdn, payment_method, campaign_id, sub_campaign_id, channel_name, number_of_offers, user_id, params, info=False):
    ep = endpoints.ESTORE_RECOMMENDATIONS
    param_dict = {"msisdn": msisdn,
                  "payment_method": payment_method, 
                  "campaign_id":campaign_id, 
                  "sub_campaign_id":sub_campaign_id, 
                  "channel_name":channel_name, 
                  "number_of_offers":number_of_offers, 
                  "user_id":user_id, 
                  "params":params}
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta


def put_estore_recommendations(auth, document, info=False):
    ep = endpoints.PUT_ESTORE_RECOMMENDATIONS
    param_dict = {
        "document": document,
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def connect_u(auth, msisdn, payment_method, campaign_id, sub_campaign_id, channel_name, number_of_offers, user_id, params, info=False):
    ep = endpoints.CONNECT_U
    param_dict = {"msisdn": msisdn,
                  "payment_method": payment_method, 
                  "campaign_id":campaign_id, 
                  "sub_campaign_id":sub_campaign_id, 
                  "channel_name":channel_name, 
                  "number_of_offers":number_of_offers, 
                  "user_id":user_id, 
                  "params":params}
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta


def put_connect_u(auth, document, info=False):
    ep = endpoints.PUT_CONNECT_U
    param_dict = {
        "document": document,
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def just_for_you(auth, msisdn, payment_method, campaign_id, sub_campaign_id, channel_name, number_of_offers, user_id, params, info=False):
    ep = endpoints.JUST_FOR_YOU
    param_dict = {"msisdn": msisdn,
                  "payment_method": payment_method, 
                  "campaign_id":campaign_id, 
                  "sub_campaign_id":sub_campaign_id, 
                  "channel_name":channel_name, 
                  "number_of_offers":number_of_offers, 
                  "user_id":user_id, 
                  "params":params}
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta


def put_just_for_you(auth, document, info=False):
    ep = endpoints.PUT_JUST_FOR_YOU
    param_dict = {
        "document": document,
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def estore_recommender_non_gsm(auth, msisdn, payment_method, campaign_id, sub_campaign_id, channel_name, number_of_offers, user_id, params, info=False):
    ep = endpoints.ESTORE_RECOMMENDER_NON_GSM
    param_dict = {"msisdn": msisdn,
                  "payment_method": payment_method, 
                  "campaign_id":campaign_id, 
                  "sub_campaign_id":sub_campaign_id, 
                  "channel_name":channel_name, 
                  "number_of_offers":number_of_offers, 
                  "user_id":user_id, 
                  "params":params}
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta


def put_estore_recommender_non_gsm(auth, document, info=False):
    ep = endpoints.PUT_ESTORE_RECOMMENDER_NON_GSM
    param_dict = {
        "document": document,
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def gift_recommendations_free(auth, msisdn, payment_method, campaign_id, sub_campaign_id, channel_name, number_of_offers, user_id, params, transaction_id, info=False):
    ep = endpoints.GIFT_RECOMMENDATIONS_FREE
    param_dict = {"msisdn": msisdn,
                  "payment_method": payment_method, 
                  "campaign_id":campaign_id, 
                  "sub_campaign_id":sub_campaign_id, 
                  "channel_name":channel_name, 
                  "number_of_offers":number_of_offers, 
                  "user_id":user_id, 
                  "params":params,
                  "transaction_id":transaction_id}
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def gift_recommendations_purchased(auth, msisdn, payment_method, campaign_id, sub_campaign_id, channel_name, number_of_offers, user_id, params, transaction_id, info=False):
    ep = endpoints.GIFT_RECOMMENDATIONS_PURCHASED
    param_dict = {"msisdn": msisdn,
                  "payment_method": payment_method, 
                  "campaign_id":campaign_id, 
                  "sub_campaign_id":sub_campaign_id, 
                  "channel_name":channel_name, 
                  "number_of_offers":number_of_offers, 
                  "user_id":user_id, 
                  "params":params,
                  "transaction_id":transaction_id}
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def put_gift_recommendations(auth, document, info=False):
    ep = endpoints.GIFT_RECOMMENDATIONS
    param_dict = {
        "document": document,
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def behavior_recommender(auth, campaign, channel, customer, params, subcampaign, userid, info=False):
    ep = endpoints.BEHAVIOR_RECOMMENDER
    param_dict = {"campaign": campaign, 
                  "subcampaign":subcampaign, 
                  "customer":customer, 
                  "channel":channel, 
                  "userid":userid, 
                  "params":params}
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta

def put_behavior_recommender(auth, document, info=False):
    ep = endpoints.PUT_BEHAVIOR_RECOMMENDER
    param_dict = {
        "document": document,
    }
    resp = request_utils.create(auth, ep, params=param_dict, info=info)
    meta = resp.json()
    return meta