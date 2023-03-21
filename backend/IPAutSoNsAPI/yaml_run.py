from kubernetes import client, config, utils
import os
import logging
logger = logging.getLogger(__name__)


class YamlRunner:
    def __init__(self):
        # def __init__(self,user_id,job_id,path,img_selected,param1,param2,param3):
        # self.user_id = user_id
        self.yaml_file = 'yaml_file/test123.yaml' # v1.4.1345
        # self.path = path
        # self.img_selected = img_selected
        # if param1 != None:
        #     self.param1 = param1
        # if param2 != None:
        #     self.param2 = param2
        # if param3 != None:
        #     self.param3 = param3

    def __self__():
        print("runner")

    def run_yaml(self):
        logger.error('Called run_yaml functions')
        try:
            logger.error('1')
            config.load_incluster_config()
            logger.error('2')
            k8s_client = client.ApiClient()
            logger.error('3')
            utils.create_from_yaml(k8s_client, self.yaml_file)
            logger.error('runed run_yaml functions')
        except (config.ConfigException,BaseException,utils.FailToCreateError,Exception) as error:
            logger.error('Fail to run yaml because : ' + str(error))

