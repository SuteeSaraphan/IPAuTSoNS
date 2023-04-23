import requests
import logging
logger = logging.getLogger(__name__)

class PreviewADVAPI():
    def __init__(self,img,img_type,model,weight_path):
        self.url = 'http://192.168.1.46:'
        self.img = img
        self.img_type = img_type
        self.model = model
        self.weight_path = weight_path
    
    def __str__(self) -> str:
        return str(self.weight_path)

    def do_preview(self):
        logger.error('runed preview functions')
        headers = {'accept': 'application/json'}
        files = {'file': self.img}
        docker_url = None
        print("1")
        if(self.model == 'YOLOv5'):
            print("2")
            docker_url = self.url+'4050/detect-to-img?modelse='+str(self.weight_path)
        elif(self.model == 'GANs'):
            docker_url = self.url+'4070/detect-to-img?modelse='+str(self.weight_path)
        try:
            headers = {'accept': 'application/json'}
            files = {'file': self.img}
            print("3")
            response = requests.post(docker_url, headers=headers, files=files)
            print('preview complete')
            print("respone : "+str(response.content))
            return response.content
        except Exception as error:
            logger.error('runed preview functions Error : '+str(error))
            return error
