import time
import xsave_functions as xsf
import hou

def save():
    """
    Checks whether the current file is named 'untitled.hip' or was last saved by a different user, and if not, saves the file.
    """
    
    # CHECK UNTITLED
    do_save = xsf.checkUntitled(hou.hipFile.basename())
    
    # CHECK PREVIOUS OWNER
    if do_save:
        do_save = xsf.checkOwner(hou.hipFile.path())
        
    # IF ALLOWED, SAVE FILE
    if do_save:
        hou.hipFile.save()
        status_message = "Successfully saved {0} ({1})".format(hou.hipFile.basename(), time.strftime("%c"))
        hou.ui.setStatusMessage(status_message)

# RUN SAVE FUNCTION
save()

