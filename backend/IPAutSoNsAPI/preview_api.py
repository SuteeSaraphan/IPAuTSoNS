import requests

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
        if(self.filter_id == 'Black and White'):
            docker_url = self.url+'4020/blackwhite'
        elif(self.filter_id == 'ASCII'):
            docker_url = self.url+'4020/ascii'
        elif(self.filter_id == 'PixelArt'):
            docker_url = self.url+'4020/pixelart'
        elif(self.filter_id == 'Object-detection'):
            docker_url = self.url+'8000/detect-to-img'
        try:
            headers = {'accept': 'application/json'}
            files = {'file': self.img}
            response = requests.post(docker_url, headers=headers, files=files)
            return response.content
        except Exception as error:
            print(error)
            return error
