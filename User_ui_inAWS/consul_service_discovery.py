import consul

client = consul.Consul(host='54.144.90.202', port=8500)
serviceName="data_processing"
service_address = client.catalog.service(serviceName)[1][0]['ServiceAddress']
service_port = client.catalog.service(serviceName)[1][0]['Serviceport']
service_url = "http://{}:{}".format(service_address, service_port)
