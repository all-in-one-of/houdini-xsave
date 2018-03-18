import os
import time
import re
import xsave_functions as xsf
import hou

# SET THIS TO TRUE IF YOU WOULD LIKE THE INCREMENT NUMBER TO COME BEFORE THE VERSION NUMBER (I.E 'my_file_i002_v003.hip')
i_before_v = False

# CALCULATE VERSION NAME
def renameVersion(ext):
    """
    Reads the current filename and calculates the next version. If no increment exists in the current version, it sets the version to 002.
    
    Arguments:
    ext (string): extension of file
    
    Returns:
    string
    """    
    
    file_name = hou.hipFile.name()
    
    # IF VERSION EXISTS IN FILENAME
    if "_v" in file_name:
        
        # FIND OLD VERSION
        beg, sep1, end = file_name.rpartition("_v")
        old_v = end.rpartition("_i")[0]
        
        # SPLIT IF INCREMENT AFTER VERSION
        if "_i" in end:
            old_v, sep2, end = end.rpartition("_i")
            
        # OTHERWISE JUST STRIP THE EXTENSION
        else:
            old_v = end.replace(ext,"")
            
    # IF VERSION DOESN'T EXIST IN FILENAME
    else:
        
        # SET VERSION TO 1
        old_v = '1'
        beg = file_name.replace(ext,"")
        sep1 = '_v'
     
    # CALCULATE NEW NAME
    old_v_numbers = re.sub('[^0-9]','', old_v)
    new_v = str(int(old_v_numbers) + 1).zfill(3)
    ver_name = beg + sep1 + new_v + ext
    
    return ver_name
 
# SAVE, VERSIONING UP
def saveVersionUp():
    """
    Check if next version already exists. If it doesn't, save. If it does, ask the user how to proceed 
    (cancel, overwrite the existing file, or calculate a new non-existing version)
    """
    
    file_name = hou.hipFile.name()    
    ext = os.path.splitext(hou.hipFile.basename())[1]
    ver_name = renameVersion(ext)
    
    # IF FILE ALREADY EXISTS    
    if os.path.isfile(ver_name):
        existing_hip_name = os.path.basename(ver_name)
        
        # ASK USER HOW TO PROCEED    
        save_method = hou.ui.displayMessage('A file with the name "{0}" already exists in this directory.\nHow would you like to proceed?'.format(existing_hip_name), buttons=('Cancel','Overwrite','Save New Version'),default_choice=2)
        
        # DO NOTHING
        if save_method == 0:
            return
        
        # OVERWRITE EXISTING FILE      
        elif save_method == 1:
            
            # CHECK IF FILE WAS LAST SAVED BY A DIFFERENT USER            
            do_save = xsf.checkOwner(ver_name)

            # IF NOT, SAVE AND SET HOUDINI STATUS MESSAGE
            if do_save:
                hou.hipFile.save(ver_name)
                status_message = "Successfully saved {0} ({1})".format(hou.hipFile.basename(), time.strftime("%c"))
                hou.ui.setStatusMessage(status_message)
                
        # SAVE NEW VERSION        
        else:
            
            # CHECK IF FILE WAS LAST SAVED BY A DIFFERENT USER            
            do_save = xsf.checkOwner(ver_name)
  
            # IF NOT, GET UNIQUE VERSION, SAVE, AND SET HOUDINI STATUS MESSAGE
            if do_save:            
                ver_name = xsf.uniqify_version(ver_name.rstrip(ext),is_file=[True,ext], splitter='_v')
                hou.hipFile.save(ver_name)
                status_message = "Successfully saved {0} ({1})".format(hou.hipFile.basename(), time.strftime("%c"))
                hou.ui.setStatusMessage(status_message)
                
    # IF FILE DOESN'T EXIST                
    else:
        
        # CHECK IF FILE IS 'untitled.hip'        
        do_save = xsf.checkUntitled(file_name)
        
        # IF NOT, SAVE AND SET HOUDINI STATUS MESSAGE    
        if do_save:         
            hou.hipFile.save(ver_name)
            status_message = "Successfully saved {0} ({1})".format(hou.hipFile.basename(), time.strftime("%c"))
            hou.ui.setStatusMessage(status_message)

saveVersionUp()
