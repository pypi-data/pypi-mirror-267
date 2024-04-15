import pytest
from unittest.mock import mock_open, patch
from .uploader import IbbUploader

def test_upload_with_file_path(mocker):
    # Mocking the open function and the requests.post function
    m = mock_open(read_data=b'test image data')
    mocker.patch('builtins.open', m)
    mocked_post = mocker.patch('requests.post')

    # Setup a fake response from ImgBB API
    fake_response = {'status': 200, 'data': {'url': 'http://example.com/image.jpg'}}
    mocked_post.return_value.json.return_value = fake_response

    # Initialize uploader and call the upload function with a file path
    uploader = IbbUploader(api_key="fake_api_key")
    response = uploader.upload('fake_path_to_image.jpg', name="test_image", expiration_days=10)

    # Asserts
    assert response == fake_response
    mocked_post.assert_called_once()
    m.assert_called_once_with('fake_path_to_image.jpg', 'rb')

def test_upload_with_url(mocker):
    # Mock requests.post to avoid actual API call
    mocked_post = mocker.patch('requests.post')
    fake_response = {'status': 200, 'data': {'url': 'http://example.com/image.jpg'}}
    mocked_post.return_value.json.return_value = fake_response

    # Initialize uploader and call the upload function with a URL
    uploader = IbbUploader(api_key="fake_api_key")
    response = uploader.upload('http://example.com/image.jpg')

    # Asserts
    assert response == fake_response
    mocked_post.assert_called_once_with(
        'https://api.imgbb.com/1/upload',
        data={
            'key': 'fake_api_key',
            'image': 'http://example.com/image.jpg',
            'expiration': None,
            'name': None
        }
    )

def test_upload_with_file_object(mocker):
    # Mock requests.post to avoid actual API call
    mocked_post = mocker.patch('requests.post')
    fake_response = {'status': 200, 'data': {'url': 'http://example.com/uploaded_image.jpg'}}
    mocked_post.return_value.json.return_value = fake_response

    # Create a fake file object using BytesIO
    from io import BytesIO
    fake_file = BytesIO(b"fake image data")

    # Initialize uploader and call the upload function with a file object
    uploader = IbbUploader(api_key="fake_api_key")
    response = uploader.upload(fake_file, name="test_image", expiration_days=5)

    # Asserts
    assert response == fake_response
    mocked_post.assert_called_once()
    # Check if the file was included in the request
    args, kwargs = mocked_post.call_args
    assert 'files' in kwargs
    assert kwargs['files']['image'] == fake_file