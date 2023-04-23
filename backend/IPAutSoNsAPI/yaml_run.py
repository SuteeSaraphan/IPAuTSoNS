from kubernetes import client, config, utils
import os
import logging
logger = logging.getLogger(__name__)


class YamlRunner:
    def __init__(self,job_id):
        self.yaml_file = 'yaml_file/'+job_id+'.yaml' # stable
    def __self__(self):
        print("runner of "+str(self.yaml_file))

    def run_yaml(self):
        logger.error('run '+self.yaml_file)
        try:
            config.load_incluster_config()
            k8s_client = client.ApiClient()
            utils.create_from_yaml(k8s_client, self.yaml_file)
            logger.error('runed run_yaml functions')
            return 1
        except (config.ConfigException,BaseException,utils.FailToCreateError,Exception) as error:
            logger.error('Fail to run yaml because : ' + str(error))
            return str(error)

