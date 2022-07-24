import os
import sys

import pyzipper


def zip_folderPyzipper(folder_path, output_path, cryptography_key):
    """Zip the contents of an entire folder (with that folder included
        in the archive). Empty subfolders will be included in the archive
        as well.
        """
    parent_folder = os.path.dirname(folder_path)
    # Retrieve the paths of the folder contents.
    contents = os.walk(folder_path)
    try:
        zip_file = pyzipper.AESZipFile(
            'bloqueado.zip.FuckYourFiles', 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES)
        zip_file.pwd = cryptography_key
        print('teste', cryptography_key)
        for root, folders, files in contents:
            # Include all subfolders, including empty ones.
            for folder_name in folders:
                absolute_path = os.path.join(root, folder_name)
                relative_path = absolute_path.replace(parent_folder + '\\',
                                                      '')
                print("Adding '%s' to archive." % absolute_path)
                zip_file.write(absolute_path, relative_path)
            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path.replace(parent_folder + '\\',
                                                      '')
                print("Adding '%s' to archive." % absolute_path)
                zip_file.write(absolute_path, relative_path)

        print("'%s' created successfully." % output_path)

    except IOError as message:
        print(message)
        sys.exit(1)
    except OSError as message:
        print(message)
        sys.exit(1)
    finally:
        zip_file.close()
