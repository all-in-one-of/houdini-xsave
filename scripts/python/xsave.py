import os
import time
from pwd import getpwuid
import xsave_functions as xsf

import hou

# SAVE FILE, WITH CHECKS
def save():
    # CHECK UNTITLED
    do_save = xsf.checkUntitled(hou.hipFile.basename())
    
    # CHECK PREVIOUS OWNER
    if do_save:
        do_save = xsf.checkOwner(hou.hipFile.path())
        
    # IF ALLOWED< SAVE FILE
    if do_save:
        hou.hipFile.save()
        status_message = "Successfully saved %s (%s)" % (hou.hipFile.basename(), time.strftime("%c"))
        hou.ui.setStatusMessage(status_message)

# RUN SAVE FUNCTION
save()

