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
        logger.error('preview 01')
        if(self.model == 'YOLOv5'):
            print("2")
            docker_url = self.url+'4050/detect-to-img?modelse='+str(self.weight_path)
        elif(self.model == 'GANs'):
            logger.error('preview 02')
            docker_url = self.url+'4070/gan?modelse='+str(self.weight_path)
        try:
            logger.error('preview 03')
            headers = {'accept': 'application/json'}
            files = {'file': self.img}
            response = requests.post(docker_url, headers=headers, files=files)
            logger.error('preview 04')
            logger.error(response.content)
            return response.content
        except Exception as error:
            logger.error('runed preview functions Error : '+str(error))
            return error
