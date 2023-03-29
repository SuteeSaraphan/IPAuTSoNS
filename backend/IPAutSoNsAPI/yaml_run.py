from kubernetes import client, config, utils
import os
import logging
logger = logging.getLogger(__name__)


class YamlRunner:
    def __init__(self,job_id):
        self.yaml_file = 'yaml_file/'+job_id+'.yaml' # v1.5
    def __self__():
        print("runner")

    def run_yaml(self):
        logger.error('run '+self.yaml_file)
        try:
            logger.error('1')
            config.load_incluster_config()
            logger.error('2')
            k8s_client = client.ApiClient()
            logger.error('3')
            utils.create_from_yaml(k8s_client, self.yaml_file)
            logger.error('runed run_yaml functions')
            return 1
        except (config.ConfigException,BaseException,utils.FailToCreateError,Exception) as error:
            logger.error('Fail to run yaml because : ' + str(error))
            return str(error)

