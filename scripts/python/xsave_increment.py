import os
import time
import re
import xsave_functions as xsf
import hou

# SET THIS TO TRUE IF YOU WOULD LIKE THE INCREMENT NUMBER TO COME BEFORE THE VERSION NUMBER (I.E 'my_file_i002_v003.hip')
i_before_v = False

# CALCULATE INCREMENT NAME
def renameIncrement(ext):
    """
    Reads the current filename and calculates the next increment. If no increment exists in the current filename,
    it sets the increment to 002.
    
    Arguments:
    ext (string): extension of file
    
    Returns:
    string
    """
    
    
    # REGEX TO FIND CURRENT INCREMENTS AND VERSIONS
    regex_i = re.compile(".*_i[0-9].*", re.IGNORECASE)
    regex_v = re.compile(".*_v[0-9].*", re.IGNORECASE)
    
    # IF NO CURRENT INCREMENTS
    if not regex_i.match(hou.hipFile.basename()):
        n = hou.hipFile.name()
        
        # SET ITER_NAME, WITH INCREMENT BEFORE VERSION
        if i_before_v:
            
            # IF VERSION EXISTS IN FILENAME
            if regex_v.match(hou.hipFile.basename()):
                iter_name = n.replace("_v","_i002_v")
                
            # IF NOT, SET NEW VERSION TO 'v002'
            else:
                iter_name = n.replace(ext,"") + "_i002_v002" + ext
                
        # SET ITER_NAME, WITH VERSION BEFORE INCREMENT
        else:
            
            # IF VERSION EXISTS IN FILENAME            
            if not regex_v.match(hou.hipFile.basename()):
                iter_name = n.replace(ext,"") + "_v002_i002" + ext    
                
            # IF NOT, SET NEW VERSION TO 'v002'                
            else:
                iter_name = n.replace(ext,"") + "_i002" + ext        
                
        # SINCE WE DIDN'T HAVE AN INCREMENT, SET NEW INCREMENT TO 'i002'         
        new_i = "002"
        
    # IF INCREMENT ALREADY EXISTS IN FILENAME    
    else:
        
        # IF VERSION EXISTS IN FILENAME
        if regex_v.match(hou.hipFile.basename()):
            
            # GET FILENAME AND SPLIT BY INCREMENT
            file_name = hou.hipFile.name()
            beg, i_sep, end = file_name.rpartition("_i")
            
            # IF VERSION IS AFTER INCREMENT
            if regex_v.match(end):
                
                # FIND OLD INCREMENT AND ITERATE UP
                end, ver = end.split("_v")
                ver = ver.replace(ext,"")
                old_i = end.replace(ext,"")
                new_i = str(int(old_i) + 1).zfill(3)
                
                # CALCULATE NEW NAME, SETTING INCREMENT BEFORE VERSION
                if i_before_v:
                    iter_name = beg + i_sep + new_i + "_v" + ver + ext
                    
                # CALCULATE NEW NAME, SETTING VERSION BEFORE INCREMENT                    
                else:
                    iter_name = beg + "_v" + ver + i_sep + new_i + ext

            # IF VERSION IS BEFORE INCREMENT
            else:
                
                # FIND OLD INCREMENT AND ITERATE UP                
                beg, v_sep, ver = beg.rpartition("_v")
                old_i = end.replace(ext,"")
                new_i = str(int(old_i) + 1).zfill(3)
                
                # CALCULATE NEW NAME, SETTING INCREMENT BEFORE VERSION                
                if i_before_v:                
                    iter_name = beg + i_sep + new_i + v_sep + ver + ext
                    
                # CALCULATE NEW NAME, SETTING VERSION BEFORE INCREMENT                                        
                else:
                    iter_name = beg + v_sep + ver + i_sep + new_i + ext
        
        # IF NO VERSION EXISTS IN FILENAME           
        else:
            
            # FIND OLD INCREMENT AND ITERATE UP                            
            file_name = hou.hipFile.name()
            beg, i_sep, end = file_name.rpartition("_i")
            old_i = end.replace(ext,"")
            new_i = str(int(old_i) + 1).zfill(3)
            iter_name = beg + i_sep + new_i + ext
            
    return iter_name

def saveIncrement():
    """
    Check if next increment already exists. If it doesn't, save. If it does, ask the user how to proceed 
    (cancel, overwrite the existing file, or calculate a new non-existing increment)
    """
    
    # FIND EXTENSION OF CURRENT FILE AND CALCULATE NEW INCREMENT NAME
    ext = os.path.splitext(hou.hipFile.basename())[1]
    iter_name = renameIncrement(ext)

    # IF FILE ALREADY EXISTS
    if os.path.isfile(iter_name):
        existing_hip_name = os.path.basename(iter_name)
        
        # ASK USER HOW TO PROCEED
        save_method = hou.ui.displayMessage('A file with the name "{0}" already exists in this directory.\nHow would you like to proceed?'.format(existing_hip_name), buttons=('Cancel','Overwrite','Save New Version'),default_choice=2)
        
        # DO NOTHING
        if save_method == 0:
            return
        
        # OVERWRITE EXISTING FILE
        elif save_method == 1:
            
            # CHECK IF FILE WAS LAST SAVED BY A DIFFERENT USER
            do_save = xsf.checkOwner(iter_name)
            
            # IF NOT, SAVE AND SET HOUDINI STATUS MESSAGE
            if do_save:
                hou.hipFile.save(iter_name)
                status_message = "Successfully saved {0} ({1})".format(hou.hipFile.basename(), time.strftime("%c"))
                hou.ui.setStatusMessage(status_message)
                
        # SAVE NEW INCREMENT
        else:
            
            # CHECK IF FILE WAS LAST SAVED BY A DIFFERENT USER
            do_save = xsf.checkOwner(iter_name)
            
            # IF NOT, GET UNIQUE INCREMENT, SAVE, AND SET HOUDINI STATUS MESSAGE
            if do_save:        
                iter_name = xsf.uniqify_increment(iter_name.rstrip(ext),is_file=[True,ext], splitter='_i', secondary_splitter='_v')
                hou.hipFile.save(iter_name)
                status_message = "Successfully saved {0} ({1})".format(hou.hipFile.basename(), time.strftime("%c"))
                hou.ui.setStatusMessage(status_message)
                
    # IF FILE DOESN'T EXIST
    else:
        
        # CHECK IF FILE IS 'untitled.hip'
        do_save = xsf.checkUntitled(hou.hipFile.basename())
        
        # IF NOT, SAVE AND SET HOUDINI STATUS MESSAGE
        if do_save:   
            hou.hipFile.save(iter_name)
            status_message = "Successfully saved {0} ({1})".format(hou.hipFile.basename(), time.strftime("%c"))
            hou.ui.setStatusMessage(status_message)


saveIncrement()
