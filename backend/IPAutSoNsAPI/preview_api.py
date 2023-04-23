import requests
import logging
logger = logging.getLogger(__name__)

class PreviewAPI():
    def __init__(self,img,img_type,filter_id,filter_value):
        self.url = 'http://192.168.1.46:'
        self.img = img
        self.img_type = img_type
        self.filter_id = filter_id
        self.filter_value = filter_value
    
    def __str__(self) -> str:
        return str(self.img)

    def do_preview(self):
        logger.error('runed preview functions')
        headers = {'accept': 'application/json'}
        files = {'file': self.img}


        if(self.filter_id == 'Black and White'):
            docker_url = self.url+'4020/blackwhite'
        elif(self.filter_id == 'ASCII'):
            docker_url = self.url+'4020/ascii'
        elif(self.filter_id == 'PixelArt'):
            docker_url = self.url+'4020/pixelart'
            docker_url += "?pixel="+str(self.filter_value).split(" ")[0]
        elif(self.filter_id == 'Mosaic'):
            docker_url = self.url+'4020/mosaig?folders=/'+(str(self.filter_value))
            print(docker_url)
        try:
            headers = {'accept': 'application/json'}
            files = {'file': self.img}
            response = requests.post(docker_url, headers=headers, files=files)
            print('preview complete')
            return response.content
        except Exception as error:
            logger.error('runed preview functions Error : '+str(error))
            return error
