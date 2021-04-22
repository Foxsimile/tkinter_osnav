import os, string, json
from sys import argv, platform


class OSNavigator:
    def __init__(self):
        print(f'OS IS:{platform}')
        self.op_sys = self.get_os()
        self.sep = self.get_path_sep()
        self.main_script_dir = self.get_main_script_dir()
        self.drives = self.get_drives()
        self.base_dir = self.get_base_dir()
        self.cwd = self.getcwd() 
        self.cwd_scan = self.update_cwd_scan()
        self.split_cwd_list = self.get_split_cwd_list()
        self.dir_changelog = []


    def get_os(self):
        standard_platforms = {'linux': 'Linux', 'linux1': 'Linux', 'linux2': 'Linux', 'darwin': 'OS X', 'win32': 'Windows'}
        if platform not in standard_platforms:
            return platform
        return standard_platforms[platform]

    
    def get_path_sep(self):
        return os.sep
        

    def get_drives(self):
        if self.op_sys == 'Windows':
            available_drives = tuple(['{0}:'.format(x) for x in string.ascii_uppercase if os.path.exists('{0}:'.format(x))])
        else:
            available_drives = ('/')
        if len(available_drives) < 1:
            exit(-1)
        return available_drives
    

    def get_main_script_dir(self):
       return os.path.dirname(os.path.abspath(__file__))


    def get_base_dir(self):
        if self.op_sys == 'Windows':
            if 'C:' in self.drives:
                base_dir = 'C:'
            else:
                base_dir = self.drives[0]
        elif self.op_sys in ('Linux', 'OS X'):
            base_dir = '/'
        return base_dir


    def getcwd(self):
        cwd = os.getcwd()
        return cwd

    
    def get_split_cwd_list(self):
        cwd_str = self.getcwd()
        split_cwd_list = []
        fully_split = False
        while fully_split == False:
            split_cwd_str = os.path.split(cwd_str)
            if split_cwd_str[1] == '':
                fully_split = True
                continue
            split_cwd_list.append(split_cwd_str[1])
            cwd_str = split_cwd_str[0]
        split_cwd_list = [os.path.splitdrive(cwd_str)[0]] + split_cwd_list[::-1]
        return split_cwd_list


    def update_cwd_scan(self):
        cwd_scan_list = list(os.scandir())
        cwd_scan = {'dirs': [x for x in cwd_scan_list if x.is_dir() == True], 'files': [x for x in cwd_scan_list if x.is_file() == True]}
        cwd_scan['dirs'].insert(0, '..')
        return cwd_scan


    def cwd_scan_insert_dir(self, insert_index, dir_name):
        self.cwd_scan['dirs'].insert(insert_index, dir_name)


    def chdir(self, target_dir, *, reversal=False):
        try:
            if target_dir in self.drives:
                target_dir += self.sep
            prev_dir = self.cwd
            if prev_dir == target_dir:
                return
            os.chdir(target_dir)
            self.cwd = self.getcwd()
            self.cwd_scan = self.update_cwd_scan()
            self.split_cwd_list = self.get_split_cwd_list()
            if reversal == False:
                self.log_chdir(prev_dir)
        except FileNotFoundError as e:
            return ('File Not Found', e)


    def log_chdir(self, prev_dir):
        chdir_pair = (prev_dir, self.cwd)
        self.dir_changelog.append(chdir_pair)


    def reverse_chdir(self):
        rev_chdir_pair = self.dir_changelog.pop()
        self.chdir(rev_chdir_pair[0], reversal=True)

    
    def dir_exists(self, dir):
        return os.path.isdir(dir)

    
    def join_paths(self, base_path, addon_path):
        joined_path = os.path.join(base_path, addon_path)
        return joined_path

    
    def seek_file_sub_dirs(self, base_dir, file, *, depth_limit=5, ignored_dirs=None, ignored_files=None, default_dir=None, **kwargs):
        os_walk_gen = os.walk(base_dir)
        if ignored_dirs != None:
            ignored_dirs = set(ignored_dirs)
        if ignored_files != None:
            ignored_files = set(ignored_files)
            if file in ignored_files:
                return default_dir
        total_count = 0
        depth_count = 0
        walking = True
        while walking:
            total_count += 1
            depth_count += 1
            root, dirs, files = next(os_walk_gen, (False, False, False))
            if (root, dirs, files) == (False, False, False) or total_count >= 999:
                return default_dir
            dirs_set = set(dirs)
            files_set = set(files)
            if file in files_set:
                return os.path.join(root, file)
            if ignored_dirs != None:
                ignored_dirs_found = ignored_dirs.intersection(dirs_set)
                for str_obj in ignored_dirs_found:
                    dirs.remove(str_obj)
            if ignored_files != None:
                ignored_files_found = ignored_files.intersection(files_set)
                for str_obj in ignored_files_found:
                    files.remove(str_obj)
            if depth_count >= depth_limit or len(dirs) == 0:
                dirs.clear()
                depth_count = 0
            

    def json_file_loader(self, base_dir, file, *, as_string=False, **kwargs):
        try:
            with open(self.seek_file_sub_dirs(base_dir, file, **kwargs), 'r') as file:
                if as_string == False:
                    loaded_data = json.load(file)
                else:
                    loaded_data = json.loads(file)
                return loaded_data
        except:
            return None

    
    def json_file_writer(self, base_dir, file, *, data, **kwargs):
        try:
            with open(self.seek_file_sub_dirs(base_dir, file, **kwargs), 'w') as file:
                json_data = json.dumps(data)
                file.write(json_data)
        except:
            pass


    def verify_paths(self, file_list, single_path=False):
        if file_list == None:
            return None
        if single_path == True:
            if os.path.exists(file_list) == True:
                return file_list
            return None
        verified_paths = [file_list[x] if os.path.exists(file_list[x]) == True else '' for x in range(len(file_list))]
        if len(verified_paths) == 0:
            return None
        return verified_paths
