import os
import shutil


class Shiiva():
    def __init__(self, file_watermark=None, name_watermark=None, exclude_formats=None):
        try:
            self.exclude_formats = exclude_formats if exclude_formats is not None else []
            self.file_watermark = file_watermark
            self.name_watermark = name_watermark
        except Exception as e:
            print("An error occurred while initializing the class:", e)
                  
    def copy_watermarks(self, file_path, destination: str):
        if not isinstance(file_path, list):
            file_path = [file_path]
        for root, dirs, filename in os.walk(destination):
            for file in file_path:
                shutil.copy(src=file, dst=root)
    
    def rename_files(self, destination: str):
        if self.name_watermark is not None:
            for root, dirs, files in os.walk(destination):
                for file in files:
                    if self.name_watermark not in file:
                        old_path = os.path.join(root, file)
                        name, ext = os.path.splitext(file)
                        if not any(e in ext for e in self.exclude_formats):
                            new_name = str(name) + str(self.name_watermark) + str(ext)
                            new_path = os.path.join(root, new_name)
                            new_path = os.rename(old_path, new_path)
        else:
            print("Files name watermark is undefined.")
        
                    
                    
    def add_txt_watermark(self, destination: str):
        if self.file_watermark is not None:
            for root, dirs, files in os.walk(destination):
                for file in files:
                    if os.path.splitext(file)[1] == '.txt':
                        file_path = os.path.join(root, file)
                        txt_temp = ''
                        with open(f'{file_path}', mode='r') as file:
                            txt_temp = file.read()
                        with open(f'{file_path}', mode='w') as file:
                            file.write(self.file_watermark + '\n' + txt_temp)
        else:
            print("TxT Files watermarks is undefined.")
    
    def make_repack(self, destination: str, file_path=None):
        try:
            self.add_txt_watermark(destination=destination)
            self.rename_files(destination=destination)
            if file_path is not None:
                if not isinstance(file_path, list):
                    file_path = [file_path]
                self.copy_watermarks(destination=destination, file_path=file_path)
            else:
                print('File_path is undefined')
        finally:
            repack_file_path = os.path.join(destination, 'shiivarepack.txt')
            with open(repack_file_path, 'w') as f:
                f.write('Repack made by SHIIVA library: pip install shiivalibrary')
                os.system('attrib +h "{}"'.format(repack_file_path))
        
        
    
    def print_file_watermark(self):
        print(self.file_watermark)
        
    def print_exclude_formats(self):
        for i in self.exclude_formats:
            print(i)
            
    def print_name_watermark(self):
        print(self.name_watermark)