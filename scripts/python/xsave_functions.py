import os
import hou

def checkOwner(check_file):
	"""
	Check if the previous owner of the file is different than the current user, and if so, prevent saving. 
	
	Arguments:
		check_file(string): Path of hip file to check.
	
	Returns:
		int: whether or not the file passed the check
	"""
	
	shell_user = os.getenv("USER")
	do_save = True
	if os.path.isfile(check_file):
	owner = getpwuid(os.stat(check_file).st_uid).pw_name
	if owner != shell_user:
	    do_save = False
	    hou.ui.displayMessage('File was last saved by user "{0}".\nPlease \'save as\' with a new name.'.format(owner), buttons=('OK',))
	return do_save

def checkUntitled(check_file):
	"""
	Check if the file is named "untitled.hip", and if so, prevent saving. 
	
	Arguments:
		check_file(string): Path of hip file to check.
	
	Returns:
		int: whether or not the file passed the check
	"""
	
	do_save = True
	if check_file == "untitled.hip":
	do_save = False
	hou.ui.displayMessage('You are attempting to save as "untitled.hip".\nPlease \'save as\' with a new name.', buttons=('OK',))
	return do_save


def uniqify_increment(name_to_change, list_to_compare=[], is_file=[False,None], splitter=None, secondary_splitter="zzzzzzz"):
	"""
	Find next highest unique filename for incrementing up, skipping over any existing increments.
	
	Arguments:
		name_to_change (string): The name of the file to make a unique name for.
		list_to_compare (list): New filename must not match any strings in this list.
		is_file (list): [bool, ext]: The first item of this list specifies whether the input is a file. 
					     The second is the file's extenstion.
		splitter (string): The increment string to split by (usually "_i")
		secondary_splitter (string): The version string to split by (usually "_v")

	Returns:
		string
	"""
	
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
	"""
	Find next highest unique filename for versioning up, skipping over any existing versions.
	
	Arguments:
		name_to_change (string): The name of the file to make a unique name for.
		list_to_compare (list): New filename must not match any strings in this list.
		is_file (list): [bool, ext]: The first item of this list specifies whether the input is a file. 
					     The second is the file's extenstion.
		splitter (string): The version string to split by (usually "_v")

	Returns:
		string
	"""
	
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
