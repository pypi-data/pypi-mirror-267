import os

def just_a_file(filename, content=""):
    home_folder = os.path.expanduser("~")
    file_path = os.path.join(home_folder, filename)
    
    try:
        # Open the file in write mode and write content to it
        with open(file_path, "w") as file:
            file.write(content)
        print(f"File '{filename}' created in {home_folder}")
    except Exception as e:
        print(f"Error: {e}")

just_a_file("IfYouCanSeeThisThenTheBuildSystemNeedsToBeLookedOver")
