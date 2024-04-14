import zipfile
import os


def unzip_file(zip_path, extract_to):
    """
    Unzip a ZIP file to a specified directory.

    Args:
    zip_path (str): The path to the ZIP file.
    extract_to (str): The directory to extract the files into.
    """
    try:
        # Ensure the target directory exists
        os.makedirs(extract_to, exist_ok=True)

        # Open the zip file
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            # Extract all the contents into the directory
            zip_ref.extractall(extract_to)
            print(f"Files have been extracted to: {extract_to}")
    except zipfile.BadZipFile:
        print("Error: The file is a bad zip file and cannot be extracted.")
    except Exception as e:
        print(f"An error occurred: {e}")
