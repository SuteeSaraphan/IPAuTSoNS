from kubernetes import client, config

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.CoreV1Api()
api_client = client.BatchV1Api()
print("Listing pods with their IPs:")
ret = api_client.list_job_for_all_namespaces(watch=False)
for i in ret.items:
    print("%s\t%s\t%s\n" % (i.status.conditions,i.metadata.namespace, i.metadata.name))
