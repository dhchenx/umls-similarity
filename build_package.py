import os
# The build_package.py is used to automate the building and uploading process of PyPi package
'''
python -m build
twine check dist/*
twine upload dist/* 
'''

if __name__=="__main__":
    current_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_path)
    print("Working directory: ", current_path)
    # delete dist files
    if os.path.exists("dist"):
        for file in os.listdir("dist"):
            if file.endswith(".whl") or file.endswith(".gz"):
                print("delete: ","dist/"+file)
                os.remove("dist/"+file)
    # build c extensions
    if os.path.exists("src_cython"):
        os.chdir("src_cython")
        os.system("python build_cython_libs.py")

    os.chdir(current_path)

    print("Starting to build...")
    os.system("python -m build")
    print()
    print("Starting to check...")
    os.system("twine check dist/*")
    print()
    print("Starting to upload...")
    username="__token__"
    token_path="../pypi_upload_token.txt"
    token_str=open(token_path,'r',encoding='utf-8').read().strip()
    os.system(f"twine upload dist/* -u {username} -p {token_str}")


