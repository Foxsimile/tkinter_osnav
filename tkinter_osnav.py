import tkinter as tk, tkinter.font as tk_font
from tkinter import ttk
import os

class MasterWindow:
    def __init__(self):
        self.master = self.create_master()
        self.osnav = OSNavigator()
        self.cwd_labelframe = None
        self.cwd_scrollbar = None
        self.cwd_stringvar = None
        self.cwd_listbox = None
        self.dir_listbox_labelframe = None
        self.dir_listbox_frame = None
        self.dir_listbox_scrollbar = None
        self.dir_listbox = None
        self.dir_listbox_active_intvar = None

        self.populate_master_overseer(self.osnav)
        

    
    def create_master(self):
        master = tk.Tk()
        master.geometry('450x350')
        master.title('Welcome to the Fox Box! (v.iii)')
        master.minsize(300, 300)
        master.maxsize(600, 600)
        return master


    def populate_master_overseer(self, osnav):
        self.populate_master_cwd_label(osnav)
        self.populate_master_dir_listbox(osnav)

    
    def populate_master_cwd_label(self, osnav):
        self.cwd_labelframe = self.create_cwd_labelframe(self.master)
        self.cwd_scrollbar = self.create_cwd_scrollbar(self.cwd_labelframe)
        self.cwd_stringvar = self.create_cwd_stringvar(osnav)
        self.cwd_listbox = self.create_cwd_listbox(self.cwd_labelframe, self.cwd_stringvar.get(), self.cwd_scrollbar)
        self.link_cwd_scrollbar_to_listbox(self.cwd_labelframe, self.cwd_scrollbar, self.cwd_listbox)


    def create_cwd_labelframe(self, frame):
        cwd_labelframe = tk.LabelFrame(frame, labelanchor=tk.W, width=273, height=42, bg='white')
        cwd_labelframe.grid(column=0, row=0, columnspan=2, sticky=tk.NW, padx=20, pady=10)
        cwd_labelframe.grid_propagate(0)
        return cwd_labelframe

    
    def create_cwd_scrollbar(self, frame):
        cwd_listbox_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        cwd_listbox_scrollbar.grid(column=0, row=1, columnspan=2, sticky=tk.EW)
        return cwd_listbox_scrollbar

    
    def link_cwd_scrollbar_to_listbox(self, frame, scrollbar, listbox):
        scrollbar.config(command=listbox.xview)
        frame.grid(column=0, row=1, columnspan=2)

    
    def create_cwd_stringvar(self, osnav):
        cwd_stringvar = tk.StringVar()
        self.set_cwd_stringvar(cwd_stringvar, osnav)
        return cwd_stringvar


    def set_cwd_stringvar(self, cwd_stringvar, osnav):
        cwd_stringvar.set(osnav.cwd)
        return cwd_stringvar


    def create_cwd_listbox(self, frame, cwd_stringvar, scrollbar):
        cwd_listbox = tk.Listbox(frame, xscrollcommand=scrollbar.set, relief=tk.GROOVE, disabledforeground='black', height=1, width=44)
        cwd_listbox.grid(column=0, row=0, sticky=tk.W)
        cwd_listbox = self.update_cwd_listbox_content(cwd_listbox, cwd_stringvar)
        return cwd_listbox


    def update_cwd_listbox_content(self, cwd_listbox, *args):
        cwd_listbox.configure(state=tk.NORMAL)
        cwd_listbox.delete(0, tk.END)
        [cwd_listbox.insert(tk.END, args[x]) for x in range(len(args))]
        cwd_listbox.configure(state=tk.DISABLED)
        return cwd_listbox


    def populate_master_dir_listbox(self, osnav):
        self.dir_listbox_labelframe = self.create_dir_listbox_labelframe(self.master)
        self.dir_listbox_frame = self.create_dir_listbox_frame(self.dir_listbox_labelframe)
        self.dir_listbox_scrollbar = self.create_dir_scrollbar(self.dir_listbox_frame)
        self.dir_listbox = self.create_dir_listbox(self.dir_listbox_frame, self.dir_listbox_scrollbar, self.osnav, self.dir_listbox_event_handler_overseer)
        self.link_dir_scrollbar_to_listbox(self.dir_listbox_frame, self.dir_listbox_scrollbar, self.dir_listbox)
        self.dir_active_intvar = self.create_dir_active_intvar(self.dir_listbox.curselection()[0])


    def create_dir_listbox_labelframe(self, frame):
        dir_listbox_labelframe = tk.LabelFrame(frame)
        dir_listbox_labelframe.grid(column=0, row=2, sticky=tk.W, padx=10, pady=0)
        return dir_listbox_labelframe


    def create_dir_listbox_frame(self, labelframe):
        dir_listbox_frame = tk.Frame(labelframe)
        return dir_listbox_frame


    def create_dir_scrollbar(self, frame):
        dir_listbox_scrollbar = tk.Scrollbar(frame)
        dir_listbox_scrollbar.grid(column=1, row=1, sticky=tk.NSEW)
        return dir_listbox_scrollbar


    def dir_listbox_event_handler_overseer(self, event_obj):
        dir_listbox = self.dir_listbox
        osnav = self.osnav
        cwd_scan = osnav.cwd_scan
        cwd_name = self.cwd_stringvar
        dir_active_intvar = self.dir_active_intvar
        if event_obj.keysym in ['Return', 'BackSpace']:
            dir_listbox, updated_index = self.dir_listbox_keypress_options_handler(dir_listbox, osnav, cwd_scan, cwd_name, dir_active_intvar, event_obj)
        elif event_obj.keysym in ['Up', 'Down']:
            dir_listbox, updated_index = self.dir_listbox_keypress_arrowkeys_handler(dir_listbox, osnav, cwd_scan, cwd_name, dir_active_intvar, event_obj)
        dir_active_intvar = self.set_dir_active_intvar(dir_active_intvar, updated_index)
        

    def dir_listbox_keypress_options_handler(self, dir_listbox, osnav, cwd_scan, cwd_name, dir_active_intvar, event_obj):
        if event_obj.keysym == 'Return':
            selection_index = dir_listbox.curselection()
        elif event_obj.keysym == 'BackSpace':
            selection_index = [(x,) for x in range(len(cwd_scan['dirs'])) if cwd_scan['dirs'][x] == '..'][0]
        selected_dir = cwd_scan['dirs'][selection_index[0]]
        if selected_dir == None:
            pass
        elif selected_dir != cwd_name:
            osnav.chdir(selected_dir)
            self.update_widgets_post_dir_change()
            self.set_dir_active_intvar(dir_active_intvar, dir_listbox.curselection())
        return (dir_listbox, dir_listbox.curselection()[0])

    
    def dir_listbox_keypress_arrowkeys_handler(self, dir_listbox, osnav, cwd_scan, cwd_name, dir_active_intvar, event_obj):
        if event_obj.keysym in ['Up']:
            scroll_dir_val = -1
        elif event_obj.keysym in ['Down']:
            scroll_dir_val = 1
        selection_index = (dir_listbox.curselection()[0] + scroll_dir_val)
        if selection_index < 0 or selection_index > dir_listbox.size():
            selection_index -= scroll_dir_val
        selected_dir = dir_listbox.get(selection_index)
        if selected_dir == '\n':
            valid_selection_indexes = [x for x in range(0, dir_listbox.size()) if dir_listbox.get(x) != '\n']
            if len(valid_selection_indexes) == 0:
                pass
            elif len(valid_selection_indexes) == 1:
                dir_listbox.activate(valid_selection_indexes[0])
            else:
                upward_selection_indexes = [valid_selection_indexes[x] for x in range(len(valid_selection_indexes)) if valid_selection_indexes[x] < selection_index]
                downward_selection_indexes = [valid_selection_indexes[x] for x in range(len(valid_selection_indexes)) if valid_selection_indexes[x] > selection_index]
                if len(upward_selection_indexes) == 0:
                    upward_selection_indexes = [None]
                if len(downward_selection_indexes) == 0:
                    downward_selection_indexes = [None]
                nearest_viable_indexes = [None, upward_selection_indexes[-1], downward_selection_indexes[0]]
                adj_scroll_dir_val = scroll_dir_val
                if nearest_viable_indexes[(scroll_dir_val * -1)] != None:
                    adj_scroll_dir_val = (scroll_dir_val * -1)
                selection_index = nearest_viable_indexes[adj_scroll_dir_val]
                dir_listbox.activate((selection_index - scroll_dir_val))
        return (dir_listbox, selection_index)
        

    def create_dir_listbox(self, frame, scrollbar, osnav, event_func):
        dir_listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
        dir_listbox = self.get_dir_listbox_content(dir_listbox, osnav)
        dir_listbox.grid(column=0, row=1, sticky=tk.W)
        keypress_event_list = ['<KeyPress-Return>', '<KeyPress-BackSpace>', '<KeyPress-Up>', '<KeyPress-Down>']
        [dir_listbox.bind(keypress_event_list[x], event_func) for x in range(len(keypress_event_list))]
        return dir_listbox

    
    def get_dir_listbox_content(self, dir_listbox, osnav):
        dir_listbox.insert(0, '--Parent Directory--')
        dir_listbox_spacer_index_list = [1]
        [dir_listbox.insert(tk.END, osnav.cwd_scan['dirs'][x].name) for x in range(1, len(osnav.cwd_scan['dirs'])) if osnav.cwd_scan['dirs'][x] != None]
        [(dir_listbox.insert(dir_listbox_spacer_index_list[x], '\n'), osnav.cwd_scan_insert_dir(dir_listbox_spacer_index_list[x], None)) for x in range(len(dir_listbox_spacer_index_list))]
        for x in range(0, dir_listbox.size() - 1):
            if x not in dir_listbox_spacer_index_list:
                dir_listbox.selection_set(x)
                dir_listbox.focus_set()
                break
        return dir_listbox


    def link_dir_scrollbar_to_listbox(self, frame, scrollbar, listbox):
        scrollbar.config(command=listbox.yview)
        frame.grid(column=3, row=1, rowspan=2)

    
    def create_dir_active_intvar(self, active_int):
        dir_active_intvar = tk.IntVar()
        self.set_dir_active_intvar(dir_active_intvar, active_int)
        return dir_active_intvar

    
    def set_dir_active_intvar(self, dir_active_intvar, active_int):
        dir_active_intvar.set(active_int)
        return dir_active_intvar

    
    def update_dir_listbox_content(self, dir_listbox, osnav):
        dir_listbox.delete(0, tk.END)
        self.get_dir_listbox_content(dir_listbox, osnav)
        return dir_listbox


    def update_widgets_post_dir_change(self):
        self.cwd_stringvar = self.set_cwd_stringvar(self.cwd_stringvar, self.osnav)
        self.cwd_listbox = self.update_cwd_listbox_content(self.cwd_listbox, self.cwd_stringvar.get())
        self.dir_listbox = self.update_dir_listbox_content(self.dir_listbox, self.osnav)




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


    def test_chdir(self):
        testing_chdir = True
        while testing_chdir == True:
            print(f'\n(cwd) {self.cwd}')
            available_dirs = {x: self.cwd_scan['dirs'][x].name for x in range(len(self.cwd_scan['dirs']))}
            available_dirs_keys = list(available_dirs.keys())
            chosen_index = None
            while chosen_index not in available_dirs_keys:
                print('''Please enter a directory index.\n"..": Parent Directory\n"/B": Reverse Directory Change.\n"/Q": Quit.''')
                if len(available_dirs_keys) > 0:
                    [print(f'{available_dirs_keys[x]}: {available_dirs[available_dirs_keys[x]]}') for x in range(len(available_dirs_keys))]
                else:
                    print('No sub-directories found. Please navigate using either ".." or "/b".')
                chosen_index = input()
                if chosen_index.lower() == '/q':
                    testing_chdir = False
                    break
                elif chosen_index == '..':
                    self.chdir(chosen_index)
                    break
                elif chosen_index.lower() == '/b':
                    self.reverse_chdir()
                    break
                if chosen_index.isdigit() == True:
                    chosen_index = int(chosen_index)    
                    chosen_dir = available_dirs[chosen_index]
                    self.chdir(chosen_dir)
                    print(self.dir_changelog[-1])

            


if __name__ == "__main__":
    master_window = MasterWindow()
    master_window.master.mainloop()