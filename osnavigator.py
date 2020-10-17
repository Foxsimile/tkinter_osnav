class OSNavigator:
    def __init__(self):
        self.drives = self.get_drives()
        self.base_dir = self.get_base_dir()
        self.cwd = self.getcwd() 
        self.cwd_scan = self.update_cwd_scan()
        self.dir_changelog = []
    

    def get_drives(self):
        available_drives = ['{0}:'.format(x) for x in string.ascii_uppercase if os.path.exists('{0}:'.format(x))]
        return available_drives


    def get_base_dir(self):
        base_dir = os.getcwd()[:os.getcwd().find('\\') + 1]
        os.chdir(base_dir)
        return base_dir


    def getcwd(self):
        cwd = os.getcwd()
        return cwd


    def update_cwd_scan(self):
        cwd_scan_list = list(os.scandir())
        cwd_scan = {'dirs': [x for x in cwd_scan_list if x.is_dir() == True], 'files': [x for x in cwd_scan_list if x.is_file() == True]}
        cwd_scan['dirs'].insert(0, '..')
        return cwd_scan


    def cwd_scan_insert_dir(self, insert_index, dir_name):
        self.cwd_scan['dirs'].insert(insert_index, dir_name)


    def chdir(self, target_dir, *, reversal=False):
        try:
            prev_dir = self.cwd
            if prev_dir == target_dir:
                return
            os.chdir(target_dir)
            self.cwd = self.getcwd()
            self.cwd_scan = self.update_cwd_scan()
            if reversal == False:
                self.log_chdir(prev_dir)
        except FileNotFoundError as e:
            return ('Exception', e)


    def log_chdir(self, prev_dir):
        chdir_pair = (prev_dir, self.cwd)
        self.dir_changelog.append(chdir_pair)


    def reverse_chdir(self):
        rev_chdir_pair = self.dir_changelog.pop()
        self.chdir(rev_chdir_pair[0], reversal=True)