import json
import requests
import os.path


class Gen3FileError(Exception):
    pass


class Gen3File:
    """For interacting with Gen3 file management features.

    A class for interacting with the Gen3 file download services.
    Supports getting presigned urls right now.

    Args:
        endpoint (str): The URL of the data commons.
        auth_provider (Gen3Auth): A Gen3Auth class instance.

    Examples:
        This generates the Gen3File class pointed at the sandbox commons while
        using the credentials.json downloaded from the commons profile page.

        >>> endpoint = "https://nci-crdc-demo.datacommons.io"
        ... auth = Gen3Auth(endpoint, refresh_file="credentials.json")
        ... sub = Gen3File(endpoint, auth)

    """

    def __init__(self, endpoint, auth_provider):
        self._auth_provider = auth_provider
        self._endpoint = endpoint

    def _get_download_response(self, guid, protocol="http"):
        api_url = "{}/user/data/download/{}&protocol={}".format(
            self._endpoint, guid, protocol
        )
        return requests.get(api_url, auth=self._auth_provider)

    def get_presigned_url(self, guid, protocol="http"):
        """Generates a presigned URL for a file.

        Retrieves a presigned url for a file giving access to a file for a limited time.

        Args:
            guid (str): The GUID for the object to retrieve.
            protocol (:obj:`str`, optional): The protocol to use for picking the available URL for generating the presigned URL.

        Examples:

            >>> Gen3File.get_presigned_url(guid)

        """
        return self._get_download_response(guid, protocol).json()
    
    def download_file(self, guid, fileloc):
        """Download a file by using a guid.

        Args:
            guid (str): The GUID for the object to retrieve.
            fileloc (str): The location where the user wishes to save the downloaded file. 
            If the location is an existing folder, the downloaded file will be saved in the original filename from metadata under that folder;
            If the location is an existing file or does not exists, the downloaded file will be saved in the given location.

        Examples:

            >>> Gen3File.download_file(guid, fileloc)

        """
        presigned_url_response = self._get_download_response(guid)
        presigned_url_data = presigned_url_response.json()
        if 'url' not in presigned_url_data:
            raise ValueError("Presigned URL generation error")
        
        download_file_response = requests.get(presigned_url_data['url'], stream=True)
        
        local_filename = fileloc
        if os.path.isdir(fileloc):
            original_filename = download_file_response.headers['Content-Disposition'].split('filename=')[1]
            if original_filename[0] == '"' or original_filename[0] == "'":
                original_filename = original_filename[1:-1]
            local_filename = os.path.join(local_filename, original_filename)
        local_file = open(local_filename, 'w+')

        for chunk in download_file_response.iter_content(chunk_size=512 * 1024): 
            if chunk:
                local_file.write(chunk)
        local_file.close() 
        return 