# -*- coding: utf-8 -*-
#
#  search_path_for_files.py
#  

import os
import glob

def SearchPathForFiles(FolderPath, FileType):
    """ 
        Loops through the folder searching for the FileType.
        If FolderPath is None it will search the current directory
        If FileType is None it will return None
    """
    
    FoundFilesList = []
    
    if FileType is None:
        return None
        
    if FolderPath is None:
        FolderPath = os.getcwd()
        
    """ Get all files in the current or passed folder """
    for FilePath in glob.glob(os.path.join(FolderPath, '*.*')):
        FileExtension = os.path.split(FilePath)[1].split(".")[1]
        
        """ Search for first FileType match and return """
        if FileExtension.lower() == FileType:
            FoundFilesList.append(os.path.split(FilePath)[1])
    
    if FoundFilesList is None:
        return None
    else:
        return FoundFilesList

