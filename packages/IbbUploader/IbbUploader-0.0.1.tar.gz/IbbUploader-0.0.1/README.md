
# IbbUploader 0.0.1

IbbUploader is a Python library for uploading images to ImgBB via their API. This library simplifies the process of uploading images from local file paths, file-like objects, or directly via URLs.

## Features

- **Upload images** from local file paths.
- **Upload images** from in-memory file-like objects.
- **Upload images** directly via image URLs.
- **Configure image storage duration** through an optional expiration setting.
- **Specify a custom name** for the uploaded image.

## Installation

To install IbbUploader, simply run the following command:

`pip install ibbuploader`


## Usage

### Uploading an Image from a File Path

`from ibbuploader import IbbUploader uploader = IbbUploader(api_key='YOUR_API_KEY') response = uploader.upload('path/to/your/image.jpg') print(response)`

### Uploading an Image via URL

`response = uploader.upload('http://example.com/image.jpg') print(response)`

### Uploading an Image from a File-like Object

`from io import BytesIO image_file = BytesIO(image_data) response = uploader.upload(image_file) print(response)`

### Additional params

`response = uploader.upload(image_file, name=image_name, expiration_days=10) `

## Configuration

To use IbbUploader, you will need to provide:

API Key: Your personal API key from ImgBB.
Expiration: Optionally, set an expiration time in days for the uploaded image, up to a maximum of 180 days.
Name: Optionally, The name of the image to be uploaded.

## Running Tests
Execute the following command to run tests:

`pytest`

## Acknowledgments

-Thanks to ImgBB for providing the API used in this library.

-This library is free software: you can redistribute it and/or modify

-This library is distributed in the hope that it will be useful, by **dlrodev92**.