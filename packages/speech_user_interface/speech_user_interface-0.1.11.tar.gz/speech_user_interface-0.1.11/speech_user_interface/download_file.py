import requests


def download_file(url, filename):
    """
    Download a file from a URL and save it to a local file.

    Args:
    url (str): The URL of the file to download.
    filename (str): The path to which the file should be saved locally.
    """
    try:
        # Send a HTTP request to the URL
        response = requests.get(url, stream=True)

        # Raise an exception if the request returned an unsuccessful status code
        response.raise_for_status()

        # Open the local file for writing in binary mode
        with open(filename, "wb") as f:
            # Iterate over the response data in chunks
            for chunk in response.iter_content(chunk_size=8192):
                # Write the data chunk to the local file
                f.write(chunk)
        print(f"File downloaded successfully: {filename}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage:
download_file("https://example.com/path/to/file", "local_filename.ext")
