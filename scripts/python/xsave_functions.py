import hou

# CHECK IF PREVIOUS OWNER OF FILE IS DIFFERENT THAN CURRENT USER AND IF SO, PREVENT SAVING
def checkOwner(check_file):
    shell_user = os.getenv("USER")
    do_save = True
    if os.path.isfile(check_file):
	owner = getpwuid(os.stat(check_file).st_uid).pw_name
	if owner != shell_user:
	    do_save = False
	    hou.ui.displayMessage('File was last saved by user "%s".\nPlease \'save as\' with a new name.' % owner, buttons=('OK',))
    return do_save

# CHECK IF FILE IS "untitled.hip" AND IF SO, PREVENT SAVING
def checkUntitled(check_file):
    do_save = True
    if check_file == "untitled.hip":
        do_save = False
        hou.ui.displayMessage('You are attempting to save as "untitled.hip".\nPlease \'save as\' with a new name.', buttons=('OK',))
    return do_save

# CREATE UNIQUE INCREMENT NAME
def uniqify_increment(name_to_change, list_to_compare=[], is_file=[False,None], splitter=None, secondary_splitter="zzzzzzz"):
    x = 0
    while x < 10000:
        if splitter:
            name_to_change, i = name_to_change.rsplit(splitter)
            v = None
            regex_v = re.compile(".*"+secondary_splitter+"[0-9].*", re.IGNORECASE)
            if regex_v.match(i):
                i, v = i.rsplit(secondary_splitter)
        if not v:
            name_to_change = name_to_change + splitter + str(int(i)+1).zfill(3)
        else:
            name_to_change = name_to_change + splitter + str(int(i)+1).zfill(3) + secondary_splitter + v
        if not is_file[0]:
            if name_to_change not in list_to_compare:
                return name_to_change
        else:
            if not os.path.isfile(name_to_change+is_file[1]):
                return name_to_change+is_file[1]
        if not splitter:
            splitter = "_"
        x += 1
    
# CREATE UNIQUE VERSION NAME    
def uniqify_version(name_to_change, list_to_compare=[], is_file=[False,None], splitter=None):
    x = 0
    while x < 10000:
        if splitter:
            name_to_change, i = name_to_change.rsplit(splitter)
        name_to_change = name_to_change + splitter + str(int(i)+1).zfill(3)
        if not is_file[0]:
            if name_to_change not in list_to_compare:
                return name_to_change
        else:
            if not os.path.isfile(name_to_change+is_file[1]):
                return name_to_change+is_file[1]
        if not splitter:
            splitter = "_"
        x += 1    
