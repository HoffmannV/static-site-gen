import spgutil, os, shutil

def main():
    #get current paths for the application
    current_path = os.path.abspath(__file__)
    public_path = ""
    static_path = ""
    content_path = ""
    root_path = ""
    
    split_path = current_path.split('/')
    current_dir_name = split_path[-2]

    if current_dir_name == 'src':
        public_path = '/'.join(split_path[:-2]) + '/public'
        static_path = '/'.join(split_path[:-2]) + '/static'
        content_path = '/'.join(split_path[:-2]) + '/content'
        root_path = '/'.join(split_path[:-2])

    else:
        public_path = '/'.join(split_path[:-1]) + '/public'
        static_path = '/'.join(split_path[:-1]) + '/static'
        content_path = '/'.join(split_path[:-1]) + '/content'
        root_path = '/'.join(split_path[:-1])
    #get current paths end

    #Remove all files from the public dir
    print("Beginning file removal\n------------------------------------------")
    for file in os.listdir(public_path):
        file_path = os.path.join(public_path, file)
        print(f"Removing {file_path}")
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            raise Exception(f"File/s {file} could not be removed\nReason:\n{e}")
    print("------------------------------------------\nFile removal complete\n")
    #Remove all files form the public dir end

    #Load all static files from the static dir into the public dir
    print("Copying files\n------------------------------------------")
    for file in os.listdir(static_path):
        src_path = os.path.join(static_path, file)
        dest_path = os.path.join(public_path, file)
        print(f"Copying {src_path} to {dest_path}")
        try:
            if os.path.isfile(src_path):
                shutil.copy(src_path, dest_path)
            elif os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path)
        except Exception as e:
            raise Exception(f"File/s {file} could not be copied.\nReason:\n{e}")
    print("------------------------------------------\nCopying complete\n")
    #Load all static files end
    
    #spgutil.generate_page(os.path.join(content_path, 'index.md'), os.path.join(root_path, 'template.html'), os.path.join(public_path, 'index.html'))
    spgutil.generate_pages_recursive(content_path, root_path, public_path)
if __name__ == "__main__":    
    main()
