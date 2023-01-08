import os

def get_files():
    # get the current working directory
    cwd = os.getcwd()
    # get the path to the courses folder
    course_code = "501"
    path = os.path.join(cwd, f"static/courses/{course_code}")
    # get a list of files in the courses folder
    files = os.listdir(path)
    print(files)
    
get_files()