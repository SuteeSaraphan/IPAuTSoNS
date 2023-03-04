from kubernetes import client, config, utils
import os

class YamlRunner:
    absolute_path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self,job_id):
    #def __init__(self,user_id,job_id,path,img_selected,param1,param2,param3):
        # self.user_id = user_id
        self.job_id = job_id
        self.yaml_file = open('yaml_file/'+self.job_id+'.yaml', 'r')
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
        print("run yaml file")
        config.load_incluster_config()
        k8s_client = client.ApiClient()
        utils.create_from_yaml(k8s_client, self.yaml_file)