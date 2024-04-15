import requests

class IbbUploader:
    def __init__(self, api_key):
        self.api_key = api_key

    def upload(self, image, name=None, expiration_days=None):
        """
        Upload an image to ImgBB either by file or by URL.
        
        :param image: File-like object, file path, or URL to the image.
        :param name: Optional. Custom name for the image.
        :param expiration_days: Optional. Number of days until the image is deleted (max 180 days).
        :return: JSON response from the API where url is found.
        """
        url = 'https://api.imgbb.com/1/upload'
        
        # Convert days to seconds, with a cap of 180 days
        expiration_seconds = None
        if expiration_days is not None:
            validated_days = min(expiration_days, 180)
            expiration_seconds = validated_days * 86400
        
        payload = {
            'key': self.api_key,
            'expiration': expiration_seconds,
            'name': name
        }
        
        # Determine if the image is a URL or a file path/object
        if isinstance(image, str) and (image.startswith('http://') or image.startswith('https://')):
            # Image is a URL
            payload['image'] = image
            response = requests.post(url, data=payload)
            
        elif isinstance(image, str):
            # Image is a file path
            with open(image, 'rb') as file:
                files = {'image': file}
                response = requests.post(url, files=files, data=payload)
        else:
            # Assume image is a file-like object
            files = {'image': image}
            response = requests.post(url, files=files, data=payload)

        return response.json()