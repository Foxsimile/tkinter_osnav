import tkinter as tk, tkinter.font as tk_font
from tkinter import ttk
import os, string
from osnavigator import OSNavigator
from shutilizer import Shutilizer

#When I wrote this code only two people knew what it did: me, and God.
#Now, only God knows.

#TODO: Use the shutil module to facilitate the file copying process from the source dir to the target dir
#TODO: Add clickability for the directory listing, as opposed to forcing selection via the enter-key
    #TODO: Remove ability to select the spacer row via clicking
#TODO: Add favourites (star) icon option to the directory listing, which will save any favourited directories within a folder for quick-access
#TODO: Add functionality to save default target directories & save names, as these are not liable to change frequently
#TODO: Add CLONE button, to actually allow for the mechanism to provide real-world functionality, as opposed to serving as a semi-neat file navigation window (granted, it is)
#TODO: Add validation to new folder name entry widget (filename_entry_widget) using the entry-widget validation parametre & a sufficient callable that is OS dependant
#TODO: Add option to modify copy location, as this functionality is currently not available
#TODO: Modify functionality of CWD navigation toolbar (topmost) to allow backspace to return to the top-most level, showcasing the available drives
#TODO: Fix that annoying jump that allows for the selection of whitespace in the directory listbox when utilizing page-up/page-down


class MasterWindow:
    def __init__(self):
        self.master = self.create_master()
        self.default_color = self.master.cget('bg')
        self.primary_widget_highlight_color = 'dodger blue'
        self.osnav = OSNavigator()
        self.op_sys_specs = self.set_operating_system_specifics(self.osnav.op_sys)
        self.photoimage_dict = {}
        self.initialize_photoimage_library()
        self.currently_active_listbox_obj = None
        self.save_data_filename = 'favorites_settings.json'
        self.save_data_filepath = None
        self.filename_default = None
        self.origin_favorites_data = None
        self.origin_favorites_default = None
        self.target_dir_favorites_data = None
        self.target_dir_favorites_default = None
        self.cwd_frame = None
        self.cwd_labelframe = None
        self.cwd_scrollbar = None
        self.cwd_stringvar = None
        self.cwd_scrollbar = None
        self.cwd_textbox = None
        self.cwd_textbox_select_indexes = None
        self.cwd_textbox_select_colorset = ('black', 'lawn green')
        self.dir_listbox_outer_frame = None
        self.dir_listbox_labelframe = None
        self.dir_listbox_frame = None
        self.dir_listbox_y_scrollbar = None
        self.dir_listbox_x_scrollbar = None
        self.dir_listbox = None
        self.dir_listbox_active_intvar = None
        self.entry_section_parent_frame = None
        self.filename_labelframe = None
        self.filename_x_scrollbar = None
        self.filename_entry_widget = None
        self.filename_default_button = None
        self.origin_labelframe = None
        self.origin_x_scrollbar = None
        self.origin_entry_widget = None
        self.origin_save_entry = None
        self.origin_save_info_entry = None
        self.origin_save_button = None
        self.origin_select_button = None
        self.origin_cancel_button = None
        self.origin_selected = None
        self.origin_favorites_button = None
        self.origin_favorites_base_frame = None
        self.origin_favorites_x_scrollbar = None
        self.origin_favorites_y_scrollbar = None
        self.origin_favorites_canvas = None
        self.origin_favorites_listbox = None
        self.origin_favorites_inner_frame = None
        self.origin_favorites_option_buttons = None
        self.target_dir_labelframe = None
        self.target_dir_x_scrollbar = None
        self.target_dir_entry_widget = None
        self.target_dir_save_entry = None
        self.target_dir_save_info_entry = None
        self.target_dir_save_button = None
        self.target_dir_select_button = None
        self.target_dir_selected = None
        self.target_dir_cancel_button = None
        self.target_dir_favorites_button = None
        self.target_dir_favorites_base_frame = None
        self.target_dir_favorites_x_scrollbar = None
        self.target_dir_favorites_y_scrollbar = None
        self.target_dir_favorites_canvas = None
        self.target_dir_favorites_listbox = None
        self.target_dir_favorites_inner_frame = None
        self.target_dir_favorites_option_buttons = None
        self.copy_button_frame = None
        self.copy_button = None

        self.load_saved_favorites_data()
        self.populate_master_overseer(self.osnav)



    def create_master(self):
        master = tk.Tk()
        master.geometry('475x350')
        master.title('Welcome to the Fox Box!')
        master.minsize(485, 350)
        #master.maxsize(485, 350)
        return master


    def set_operating_system_specifics(self, op_sys):
        default_font = tk_font.nametofont('TkDefaultFont')
        op_sys_specs = {'font': default_font, 'fav_listbox_width_height': (0, 0), 'fav_canvas_width_height': (26, 240)}
        if op_sys in ('Linux', 'OS X'):
            op_sys_specs['font'].configure(family='DejaVu Serif', size=10)
            op_sys_specs['fav_listbox_width_height'] = (1, 0)
            op_sys_specs['fav_canvas_width_height'] = (30, 270)
        return op_sys_specs


    def load_saved_favorites_data(self):
        default_dir = self.osnav.join_paths(self.osnav.main_script_dir, 'settings')
        if self.osnav.ensure_dir_exists(default_dir) != True:
            exit(-1)
        self.save_data_filepath = self.osnav.join_paths(default_dir, self.save_data_filename)
        loaded_data = self.osnav.json_file_loader(self.osnav.main_script_dir, self.save_data_filename, ignored_dirs=['.git', '__pycache__'], default_dir=self.save_data_filepath)
        
        if loaded_data == None:
            loaded_data = self.create_blank_favorites_data()

        if isinstance(loaded_data, dict):
            filename_default = loaded_data.get('filename_default', None)
            if isinstance(filename_default, str):
                self.filename_default = filename_default
            origin_favorites_default = loaded_data.get('origin_default', None)
            if isinstance(origin_favorites_default, list) and len(origin_favorites_default) == 2 and isinstance(origin_favorites_default[0], str) and isinstance(origin_favorites_default[1], str):
                if len(origin_favorites_default) > 0 and origin_favorites_default[1] != '':
                    origin_favorites_default = (origin_favorites_default[0], self.osnav.verify_paths(origin_favorites_default[1], single_path=True))
                self.origin_favorites_default = origin_favorites_default
            target_dir_favorites_default = loaded_data.get('target_default', None)
            if isinstance(target_dir_favorites_default, list) and len(target_dir_favorites_default) == 2 and isinstance(target_dir_favorites_default[0], str) and isinstance(target_dir_favorites_default[1], str):
                if len(target_dir_favorites_default) > 0 and target_dir_favorites_default[1] != '':
                    target_dir_favorites_default = (target_dir_favorites_default[0], self.osnav.verify_paths(target_dir_favorites_default[1], single_path=True))
                self.target_dir_favorites_default = target_dir_favorites_default
            origin_favorites_data = loaded_data.get('origin_favorites', None)
            if isinstance(origin_favorites_data, list):
                if len(origin_favorites_data) > 0:
                    origin_favorites_data = [origin_favorites_data[x] for x in range(len(origin_favorites_data)) if len(origin_favorites_data[x]) == 2 and isinstance(origin_favorites_data[x][0], str) and isinstance(origin_favorites_data[x][1], str)]
                    origin_favorites_paths = self.osnav.verify_paths([origin_favorites_data[x][1] for x in range(len(origin_favorites_data))])
                    origin_favorites_data = [tuple(origin_favorites_data[x]) for x in range(len(origin_favorites_data)) if origin_favorites_paths[x] != '']
                self.origin_favorites_data = origin_favorites_data
            target_dir_favorites_data = loaded_data.get('target_favorites', None)
            if isinstance(target_dir_favorites_data, list):
                if len(target_dir_favorites_data) > 0:
                    target_dir_favorites_data = [target_dir_favorites_data[x] for x in range(len(target_dir_favorites_data)) if len(target_dir_favorites_data[x]) == 2 and isinstance(target_dir_favorites_data[x][0], str) and isinstance(target_dir_favorites_data[x][1], str)]
                    target_dir_favorites_paths = self.osnav.verify_paths([target_dir_favorites_data[x][1] for x in range(len(target_dir_favorites_data))])
                    target_dir_favorites_data = [tuple(target_dir_favorites_data[x]) for x in range(len(target_dir_favorites_data)) if target_dir_favorites_paths[x] != '']
                self.target_dir_favorites_data = target_dir_favorites_data


    def create_blank_favorites_data(self):
        favorites_dict = {'filename_default': "", 'origin_default': [], 'target_default': [], 'origin_favorites': [], 'target_favorites': []}
        return favorites_dict


    def write_favorites_data_to_file(self):
        default_dir = self.osnav.join_paths(self.osnav.join_paths(self.osnav.main_script_dir, 'settings'), self.save_data_filename)
        self.osnav.json_file_writer(self.osnav.main_script_dir, self.save_data_filename, data=self.aggregate_favorites_data(), ignored_dirs=['.git', '__pycache__'], default_dir=default_dir)

    
    def aggregate_favorites_data(self):
        favorites_dict = {'filename_default': self.filename_default, 'origin_default': self.origin_favorites_default, 'target_default': self.target_dir_favorites_default,
                            'origin_favorites': self.origin_favorites_data, 'target_favorites': self.target_dir_favorites_data}
        return favorites_dict


    def populate_master_overseer(self, osnav):
        self.populate_master_cwd_label(osnav)
        self.populate_master_dir_listbox(osnav)
        self.populate_entry_section_overseer(osnav)
        self.cwd_textbox_highlight_end(self.cwd_textbox, target_end=-1, return_focus=1)
        self.populate_master_copy_button(osnav)


    def initialize_photoimage_library(self):
        filenames = [('master_copy_icon', 'fourfox_icon_remaster_extra_mini.png'), ('delete_icon', 'garbage_tiny.png'), ('favorite_icon', 'black_star_tiny.png')]
        for x in range(len(filenames)):
            file_path = self.osnav.seek_file_sub_dirs(self.osnav.main_script_dir, filenames[x][1], ignored_dirs=['.git', '__pycache__'])
            if file_path != None:
                photoimage_object = tk.PhotoImage(file=self.osnav.seek_file_sub_dirs(self.osnav.main_script_dir, filenames[x][1], ignored_dirs=['.git', '__pycache__']))
                self.photoimage_library_add(filenames[x][0], photoimage_object)

    
    def photoimage_library_add(self, filename, image_object):
        self.photoimage_dict[filename] = image_object
    

    def photoimage_library_remove(self, filename):
        if filename in self.photoimage_dict:
            del self.photoimage_dict[filename]

    
    def photoimage_library_get(self, filename):
        return self.photoimage_dict.get(filename, None)
        
    
    def populate_master_cwd_label(self, osnav):
        self.cwd_frame, self.cwd_labelframe = self.create_cwd_frame_and_labelframe(self.master)
        self.cwd_x_scrollbar = self.create_cwd_x_scrollbar(self.cwd_labelframe)
        self.cwd_stringvar = self.create_cwd_stringvar(osnav)
        self.cwd_textbox = self.create_cwd_textbox(self.cwd_labelframe, self.cwd_stringvar.get(), self.cwd_x_scrollbar)
        self.link_cwd_x_scrollbar_to_textbox(self.cwd_labelframe, self.cwd_x_scrollbar, self.cwd_textbox)


    def create_cwd_frame_and_labelframe(self, frame):
        cwd_frame = tk.Frame(frame, bg=self.default_color)
        cwd_frame.grid(column=0, row=0, columnspan=2, sticky=tk.NW, padx=20, pady=10)
        cwd_labelframe = tk.LabelFrame(cwd_frame, labelanchor=tk.W, height=42)
        cwd_labelframe.grid(column=0, row=0, padx=2, pady=2)
        return cwd_frame, cwd_labelframe

    
    def create_cwd_x_scrollbar(self, frame):
        cwd_x_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        cwd_x_scrollbar.grid(column=0, row=1, columnspan=2, sticky=tk.EW)
        return cwd_x_scrollbar

    
    def link_cwd_x_scrollbar_to_textbox(self, frame, scrollbar, textbox):
        scrollbar.config(command=textbox.xview)
        frame.grid(column=0, row=1, columnspan=2)

    
    def create_cwd_stringvar(self, osnav):
        cwd_stringvar = tk.StringVar()
        self.set_cwd_stringvar(cwd_stringvar, osnav)
        return cwd_stringvar


    def set_cwd_stringvar(self, cwd_stringvar, osnav):
        cwd_stringvar.set(osnav.cwd)
        return cwd_stringvar

    
    def get_cwd_stringvar(self):
        return self.cwd_stringvar.get()


    def create_cwd_textbox(self, frame, cwd_stringvar, scrollbar):
        cwd_textbox = tk.Text(frame, xscrollcommand=scrollbar.set, relief=tk.GROOVE, wrap=tk.NONE, cursor='hand2', selectbackground='white', selectforeground='black', insertwidth=3, height=1, width=40)
        cwd_textbox.grid(column=0, row=0, sticky=tk.W)
        cwd_textbox_bindings = [('<FocusIn>', self.cwd_textbox_focus_in_handler), ('<FocusOut>', self.cwd_textbox_focus_out_handler),
                                ('<Up>', self.cwd_textbox_keypress_handler), ('<Down>', self.cwd_textbox_keypress_handler),
                                ('<Left>', self.cwd_textbox_keypress_handler), ('<Right>', self.cwd_textbox_keypress_handler), ('<ButtonRelease>', self.cwd_textbox_button_handler),
                                ('<Home>', self.cwd_textbox_keypress_handler), ('<End>', self.cwd_textbox_keypress_handler), ('<Return>', self.cwd_textbox_keypress_handler)]
        [cwd_textbox.bind(cwd_textbox_bindings[x][0], cwd_textbox_bindings[x][1]) for x in range(len(cwd_textbox_bindings))]
        cwd_textbox = self.update_cwd_textbox_content(cwd_textbox, cwd_stringvar)
        return cwd_textbox


    def update_cwd_textbox_content(self, cwd_textbox, *args):
        cwd_textbox.configure(state=tk.NORMAL)
        cwd_textbox.delete('0.0', tk.END)
        [cwd_textbox.insert(tk.END, args[x]) for x in range(len(args))]
        cwd_textbox.configure(state=tk.DISABLED)
        cwd_textbox.see(tk.END)
        self.cwd_textbox_highlight_end(cwd_textbox, target_end=-1, return_focus=1)
        return cwd_textbox

    
    def textbox_create_and_highlight_tag(self, textbox, tag_name, index_tuple, *, bg_color='cyan', fg_color='white', clear_tag_prev=True):
        if clear_tag_prev == True:
            self.textbox_clear_tag(textbox, tag_name)
        textbox.focus_set()
        textbox.mark_set('matchStart', index_tuple[0])
        textbox.mark_set('matchEnd', index_tuple[1])
        textbox.tag_add(tag_name, 'matchStart', 'matchEnd')
        textbox.tag_configure(tag_name, background=bg_color, foreground=fg_color)

    
    def textbox_clear_tag(self, textbox, tag_name):
        textbox.tag_delete(tag_name)

    
    def cwd_textbox_highlight_end(self, textbox, *, target_end, return_focus=0):
        if return_focus:
            current_focus_obj = self.master.focus_get()
        if target_end == 0:
            textbox.focus_set()
            textbox.event_generate('<Home>')
        elif target_end == -1:
            textbox.focus_set()
            textbox.event_generate('<End>')
        if return_focus:
            if current_focus_obj != None:
                current_focus_obj.focus_set()

    
    def cwd_textbox_keypress_handler(self, event_obj):
        if event_obj.keysym in ['Left', 'Right', 'Home', 'End']:
            self.cwd_textbox_dir_nav_event_handler(event_obj)
        elif event_obj.keysym in ['Up', 'Down']:
            self.currently_active_listbox_obj.focus_set()
            self.currently_active_listbox_obj.event_generate(f'<{event_obj.keysym}>')
        elif event_obj.keysym in ['Return']:
            self.cwd_textbox_chdir_nav_event_handler(event_obj)
            self.currently_active_listbox_obj.focus_set()

    
    def cwd_textbox_button_handler(self, event_obj):
        if event_obj.type.name == 'ButtonRelease':
            self.cwd_textbox_dir_nav_event_handler(event_obj)


    def cwd_textbox_focus_in_handler(self, event_obj):
        self.cwd_frame.configure(bg=self.primary_widget_highlight_color)


    def cwd_textbox_focus_out_handler(self, event_obj):
        self.cwd_frame.configure(bg=self.default_color)
    

    def cwd_textbox_dir_nav_event_handler(self, event_obj):
        insertion_index = self.cwd_textbox.index(tk.INSERT)
        cwd_str = '/'.join(self.osnav.split_cwd_list)
        textbox_sel_bg_color = self.cwd_textbox_select_colorset[0]
        textbox_sel_fg_color = self.cwd_textbox_select_colorset[1]
        textbox_tag_start_text_index = None
        textbox_tag_end_text_index = None

        if event_obj.keysym in ['Left', 'Right'] or event_obj.type.name == 'ButtonRelease':
            if event_obj.type.name == 'KeyPress':
                if len(self.cwd_textbox.tag_ranges('cwd_sel_tag')) > 0:
                    insertion_index = self.cwd_textbox.tag_ranges('cwd_sel_tag')[0].string
                if ((modifier := 1) and event_obj.keysym != 'Left'):
                    modifier = -1
            elif event_obj.type.name == 'ButtonRelease':
                modifier = 0
                insertion_index = self.cwd_textbox.index(tk.CURRENT)
                
            line_num_str = insertion_index[:insertion_index.find('.')]
            insertion_index = int(insertion_index[insertion_index.find('.') + 1:]) + 1
            if insertion_index != None:
                if modifier == 0:
                    if (start_index := (cwd_str.rfind('/', 0, insertion_index)) + 1) == len(cwd_str):
                        start_index = 0
                    if (end_index := cwd_str.find('/', insertion_index, len(cwd_str))) == -1:
                        end_index = (len(cwd_str))
                elif modifier == 1:
                    if (end_index := (cwd_str.rfind('/', 0, insertion_index))) in [-1, 0]:
                        return "break"
                    if (start_index := cwd_str.rfind('/', 0, end_index - 1) + 1) == -1:
                        return "break"
                elif modifier == -1:
                    if (start_index := cwd_str.find('/', insertion_index, len(cwd_str)) + 1) in [0, -1]:
                        return "break"
                    if (end_index := cwd_str.find('/', start_index, len(cwd_str))) == -1:
                        end_index = len(cwd_str)
                textbox_tag_start_text_index = f"{line_num_str}.{str(start_index)}"
                textbox_tag_end_text_index = f"{line_num_str}.{str(end_index)}"
        
        elif event_obj.keysym in ['Home', 'End']:
            line_num_str = insertion_index[:insertion_index.find('.')]
            if event_obj.keysym == 'Home':
                start_index = 0
                end_index = cwd_str.find('/')
            else:
                start_index = cwd_str.rfind('/') + 1
                end_index = len(cwd_str)
                if start_index == end_index:
                    start_index = 0
            textbox_tag_start_text_index = f"{line_num_str}.{str(start_index)}"
            textbox_tag_end_text_index = f"{line_num_str}.{str(end_index)}"

        if textbox_tag_start_text_index != None and textbox_tag_end_text_index != None:
            self.cwd_textbox.mark_set('insert', textbox_tag_start_text_index)
            self.cwd_textbox.see(textbox_tag_end_text_index)
            self.cwd_textbox.see(textbox_tag_start_text_index)
            self.textbox_create_and_highlight_tag(self.cwd_textbox, 'cwd_sel_tag', (textbox_tag_start_text_index, textbox_tag_end_text_index), bg_color=textbox_sel_bg_color, fg_color=textbox_sel_fg_color)
            self.cwd_textbox_select_indexes = (textbox_tag_start_text_index, textbox_tag_end_text_index)
        return "break"

    
    def cwd_textbox_chdir_nav_event_handler(self, event_obj):
        osnav = self.osnav
        if event_obj.keysym in ['Return']:
            end_index = f"{self.cwd_textbox_select_indexes[1][:self.cwd_textbox_select_indexes[1].find('.')]}.{str(int(self.cwd_textbox_select_indexes[1][self.cwd_textbox_select_indexes[1].find('.') + 1:]))}"
            selected_dir = self.cwd_textbox.get('0.0', end_index)
            osnav.chdir(selected_dir)
            self.update_widgets_post_dir_change()
            self.currently_active_listbox_obj.focus_force()

    
    def zero_listbox_sel_and_change_listbox_focus(self):
        self.currently_active_listbox_obj.selection_set(0)
        self.currently_active_listbox_obj.activate(0)
        self.currently_active_listbox_obj.focus_set()

        
    def populate_master_dir_listbox(self, osnav):
        self.dir_listbox_outer_frame, self.dir_listbox_labelframe = self.create_dir_listbox_frame_and_labelframe(self.master)
        self.dir_listbox_frame = self.create_dir_listbox_frame(self.dir_listbox_labelframe)
        self.dir_listbox_y_scrollbar = self.create_dir_y_scrollbar(self.dir_listbox_frame)
        self.dir_listbox_x_scrollbar = self.create_dir_x_scrollbar(self.dir_listbox_frame)
        self.dir_listbox = self.create_dir_listbox(self.dir_listbox_frame, self.dir_listbox_y_scrollbar, self.dir_listbox_x_scrollbar, self.osnav, self.dir_listbox_event_handler_overseer)
        self.currently_active_listbox_obj = self.dir_listbox
        self.link_dir_y_scrollbar_to_listbox(self.dir_listbox_frame, self.dir_listbox_y_scrollbar, self.dir_listbox)
        self.link_dir_x_scrollbar_to_listbox(self.dir_listbox_frame, self.dir_listbox_x_scrollbar, self.dir_listbox)
        self.dir_active_intvar = self.create_dir_active_intvar(self.dir_listbox.curselection()[0])


    def create_dir_listbox_frame_and_labelframe(self, frame):
        dir_listbox_frame = tk.Frame(frame, bg=self.default_color)
        dir_listbox_frame.grid(column=0, row=2, rowspan=2, sticky=tk.NW, padx=10, pady=0)
        dir_listbox_labelframe = tk.LabelFrame(dir_listbox_frame, padx=1, pady=1, bg=self.default_color)
        dir_listbox_labelframe.grid(column=0, row=0, sticky=tk.NSEW)
        return dir_listbox_frame, dir_listbox_labelframe


    def create_dir_listbox_frame(self, frame):
        dir_listbox_frame = tk.Frame(frame)
        return dir_listbox_frame


    def create_dir_y_scrollbar(self, frame):
        dir_listbox_yscrollbar = tk.Scrollbar(frame)
        dir_listbox_yscrollbar.grid(column=1, row=1, rowspan=1, sticky=tk.NSEW)
        return dir_listbox_yscrollbar

    
    def create_dir_x_scrollbar(self, frame):
        dir_listbox_x_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        dir_listbox_x_scrollbar.grid(column=0, row=2, columnspan=1, sticky=tk.EW)
        return dir_listbox_x_scrollbar


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
        elif event_obj.keysym in ['Next', 'Prior']:
            return
        elif event_obj.keysym in ['Left', 'Right']:
            self.cwd_textbox.focus_set()
            self.cwd_textbox.event_generate(f'<{event_obj.keysym}>')
            return "break"
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
                dir_listbox.selection_set(valid_selection_indexes[0])
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

    
    def dir_listbox_focus_in_handler(self, event_obj):
        self.dir_listbox_labelframe.configure(bg=self.primary_widget_highlight_color)


    def dir_listbox_focus_out_handler(self, event_obj):
        self.dir_listbox_labelframe.configure(bg=self.default_color)


    def create_dir_listbox(self, frame, y_scrollbar, x_scrollbar, osnav, event_func):
        dir_listbox = tk.Listbox(frame, yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set, width=25, height=15)
        dir_listbox = self.get_dir_listbox_content(dir_listbox, osnav)
        dir_listbox.grid(column=0, row=1, sticky=tk.W)
        keypress_event_list = ['<KeyPress-Return>', '<KeyPress-BackSpace>', '<KeyPress-Up>', '<KeyPress-Down>', '<Next>', '<Prior>', '<Left>', '<Right>']
        [dir_listbox.bind(keypress_event_list[x], event_func) for x in range(len(keypress_event_list))]
        dir_listbox.bind('<FocusIn>', self.dir_listbox_focus_in_handler)
        dir_listbox.bind('<FocusOut>', self.dir_listbox_focus_out_handler)
        return dir_listbox

    
    def get_dir_listbox_content(self, dir_listbox, osnav):
        dir_listbox.insert(0, ' ' + '--Parent Directory--')
        dir_listbox_spacer_index_list = [[], [1]][(len(osnav.cwd_scan['dirs']) > 1)]
        [dir_listbox.insert(tk.END, ' ' + osnav.cwd_scan['dirs'][x]) for x in range(1, len(osnav.cwd_scan['dirs'])) if osnav.cwd_scan['dirs'][x] != None]
        [(dir_listbox.insert(dir_listbox_spacer_index_list[x], '\n'), osnav.cwd_scan_insert_dir(dir_listbox_spacer_index_list[x], None)) for x in range(len(dir_listbox_spacer_index_list))]
        selection_index = None
        for x in range(0, dir_listbox.size() - 1):
            if x not in dir_listbox_spacer_index_list:
                selection_index = x
                break
        else:
            selection_index = 0
        dir_listbox.selection_set(selection_index)
        dir_listbox.focus_set()
        return dir_listbox


    def link_dir_y_scrollbar_to_listbox(self, frame, y_scrollbar, listbox):
        y_scrollbar.config(command=listbox.yview)
        frame.grid(column=3, row=1, rowspan=2)


    def link_dir_x_scrollbar_to_listbox(self, frame, x_scrollbar, listbox):
        x_scrollbar.config(command=listbox.xview)
        frame.grid(column=0, row=2, columnspan=2)
    

    def create_dir_active_intvar(self, active_int):
        dir_active_intvar = tk.IntVar()
        self.set_dir_active_intvar(dir_active_intvar, active_int)
        return dir_active_intvar

    
    def set_dir_active_intvar(self, dir_active_intvar, active_int):
        dir_active_intvar.set(active_int)
        self.dir_active_intvar = dir_active_intvar
        return dir_active_intvar

    
    def update_dir_listbox_content(self, dir_listbox, osnav):
        dir_listbox.delete(0, tk.END)
        self.get_dir_listbox_content(dir_listbox, osnav)
        return dir_listbox


    def update_widgets_post_dir_change(self):
        self.cwd_stringvar = self.set_cwd_stringvar(self.cwd_stringvar, self.osnav)
        self.cwd_textbox = self.update_cwd_textbox_content(self.cwd_textbox, self.cwd_stringvar.get())
        self.dir_listbox = self.update_dir_listbox_content(self.dir_listbox, self.osnav)


    def populate_entry_section_overseer(self, osnav):
        self.entry_section_parent_frame = self.create_entry_section_parent_frame(self.master)
        self.populate_master_origin_entry_widget(osnav, self.entry_section_parent_frame)
        self.populate_master_filename_entry_widget(osnav, self.entry_section_parent_frame, self.filename_default)
        self.populate_master_target_dir_entry_widget(osnav, self.entry_section_parent_frame)

    
    def create_entry_section_parent_frame(self, frame):
        entry_section_parent_frame = tk.Frame(frame)
        entry_section_parent_frame.grid(column=1, row=2, pady=10, sticky=tk.N)
        return entry_section_parent_frame

    
    def populate_master_filename_entry_widget(self, osnav, parent_frame, default_filename):
        self.filename_labelframe = self.create_filename_labelframe(parent_frame)
        self.filename_x_scrollbar = self.create_filename_x_scrollbar(self.filename_labelframe)
        self.filename_entry_widget = self.create_filename_entry_widget(self.filename_labelframe, self.filename_x_scrollbar, default_filename)
        self.link_filename_x_scrollbar_to_entry_widget(self.filename_labelframe, self.filename_x_scrollbar, self.filename_entry_widget)
        self.filename_default_button = self.create_filename_default_button(self.filename_labelframe, self.filename_default_button_command_func)    


    def create_filename_labelframe(self, frame):
        filename_labelframe = tk.LabelFrame(frame, text="Save As", relief=tk.RIDGE, padx=2)
        filename_labelframe.grid(column=0, row=0)
        return filename_labelframe


    def create_filename_x_scrollbar(self, frame):
        filename_x_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        filename_x_scrollbar.grid(column=0, row=1, sticky=tk.EW)
        return filename_x_scrollbar


    def create_filename_entry_widget(self, frame, x_scrollbar, default_filename):
        filename_entry_widget = tk.Entry(frame, xscrollcommand=x_scrollbar.set, width=30)
        if default_filename:
            filename_entry_widget.insert(0, default_filename)
        filename_entry_widget.grid(column=0, row=0, padx=1)
        return filename_entry_widget

    
    def link_filename_x_scrollbar_to_entry_widget(self, frame, x_scrollbar, entry_widget):
        x_scrollbar.configure(command=entry_widget.xview)

    
    def create_filename_default_button(self, frame, command_func):
        filename_default_button = tk.Button(frame, command=command_func, text='SET DEFAULT', font=tk_font.Font(size=8))
        filename_default_button.grid(column=1, row=0)
        return filename_default_button

    
    def filename_default_button_command_func(self):
        if self.filename_default != self.filename_entry_widget.get():
            self.filename_default = self.filename_entry_widget.get()
            self.write_favorites_data_to_file()


    def populate_master_origin_entry_widget(self, osnav, parent_frame):
        self.origin_labelframe = self.create_origin_labelframe(parent_frame)
        self.origin_x_scrollbar = self.create_origin_x_scrollbar(self.origin_labelframe)
        self.origin_entry_widget = self.create_origin_entry_widget(self.origin_labelframe, self.origin_x_scrollbar)
        self.link_origin_x_scrollbar_to_entry_widget(self.origin_labelframe, self.origin_x_scrollbar, self.origin_entry_widget)
        self.origin_save_button = self.create_origin_save_button(self.origin_labelframe, self.origin_save_button_command_handler)
        self.origin_select_button = self.create_origin_select_button(self.origin_labelframe, self.origin_select_button_command_handler)
        self.origin_favorites_button = self.create_origin_favorites_button(self.origin_labelframe, self.origin_favorites_button_command)
        self.origin_save_info_entry, self.origin_save_entry = self.create_origin_save_entry_widget_pair(self.origin_labelframe)
        self.origin_cancel_button = self.create_origin_cancel_button(self.origin_labelframe, self.origin_cancel_button_command_handler)
        self.origin_favorites_base_frame, self.origin_favorites_x_scrollbar, self.origin_favorites_y_scrollbar, self.origin_favorites_canvas, self.origin_favorites_listbox, self.origin_favorites_inner_frame, self.origin_favorites_option_buttons = self.create_favorites_overlay_omni_overseer((self.dir_listbox.cget('width'), self.dir_listbox.cget('height')), 'origin_favorites_default', self.origin_favorites_data)
        self.origin_favorites_listbox.bind('<Return>', self.origin_select_button_command_handler)


    def create_origin_labelframe(self, frame):
        origin_labelframe = tk.LabelFrame(frame, text="Copy Location", relief=tk.RIDGE, padx=2)
        origin_labelframe.grid(column=0, row=1, pady=5, sticky=tk.W)
        return origin_labelframe

    
    def create_origin_x_scrollbar(self, frame):
        origin_x_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        origin_x_scrollbar.grid(column=0, row=1, sticky=tk.EW)
        return origin_x_scrollbar

    
    def create_origin_entry_widget(self, frame, x_scrollbar):
        origin_entry_widget = tk.Entry(frame, xscrollcommand=x_scrollbar.set, width=30, state=tk.DISABLED, disabledbackground='WHITE', disabledforeground='BLACK')
        origin_entry_widget.grid(column=0, row=0, padx=1, sticky=tk.S)
        return origin_entry_widget

    
    def create_origin_save_entry_widget_pair(self, frame):
        origin_save_info_entry = tk.Entry(frame, width=12, disabledbackground='WHITE', disabledforeground='BLACK')
        origin_save_info_entry.insert(0, ' SAVE NAME')
        origin_save_info_entry.configure(state=tk.DISABLED)
        origin_save_info_entry.grid(column=0, row=0, padx=1, sticky=tk.SW)
        origin_save_info_entry.lower()
        origin_save_entry = tk.Entry(frame, width=18, state=tk.DISABLED)
        origin_save_entry.grid(column=0, row=0, padx=1, sticky=tk.SE)
        origin_save_entry.lower()
        return origin_save_info_entry, origin_save_entry

    
    def link_origin_x_scrollbar_to_entry_widget(self, frame, x_scrollbar, entry_widget):
        x_scrollbar.configure(command=entry_widget.xview)

    
    def create_origin_save_button(self, frame, command_func):
        origin_save_button = tk.Button(frame, command=command_func, text="SAVE", font=tk.font.Font(size=8))
        origin_save_button.grid(column=1, row=0)
        return origin_save_button

    
    def origin_save_button_command_handler(self):
        if self.origin_entry_widget.get() == "":
            return
        if self.origin_save_entry.cget('state') == tk.DISABLED:
            self.origin_save_info_entry.lift()
            self.origin_save_entry.lift()
            self.origin_save_entry.configure(state=tk.NORMAL)
            self.origin_save_entry.focus_set()
            self.origin_cancel_button.lift()
            self.origin_save_button.configure(bg='lime')
            self.origin_save_info_entry.configure(xscrollcommand=self.origin_x_scrollbar.set)
        elif self.origin_save_entry.cget('state') in [tk.NORMAL, tk.ACTIVE]:
            if self.origin_save_entry.get() != "":
                self.append_fav_to_favorites_listbox(self.origin_favorites_listbox, (self.origin_save_entry.get(), self.origin_entry_widget.get()))
                self.origin_favorites_data.append((self.origin_save_entry.get(), self.origin_entry_widget.get()))
                self.add_favorites_options_buttons(self.origin_favorites_inner_frame, self.origin_favorites_listbox, self.origin_favorites_option_buttons, self.origin_favorites_data, 'origin_favorites_default')
                self.origin_cancel_button.invoke()
                self.origin_entry_widget.configure(state=tk.NORMAL)
                self.origin_entry_widget.delete(0, tk.END)
                self.origin_entry_widget.configure(state=tk.DISABLED)
                self.write_favorites_data_to_file()


    def create_origin_cancel_button(self, frame, command_func):
        origin_cancel_button = tk.Button(frame, command=command_func, text="CANCEL", font=tk.font.Font(size=8), bg='red')
        origin_cancel_button.grid(column=2, row=0)
        origin_cancel_button.lower()
        return origin_cancel_button


    def origin_cancel_button_command_handler(self):
        self.origin_save_info_entry.lower()
        self.origin_save_entry.delete(0, tk.END)
        self.origin_save_entry.lower()
        self.origin_save_entry.configure(state=tk.DISABLED)
        self.origin_cancel_button.lower()
        self.origin_entry_widget.configure(xscrollcommand=self.origin_x_scrollbar.set)
        self.cwd_textbox.focus_set()
        self.cwd_textbox.event_generate('<End>')
        self.origin_save_button.configure(bg=self.default_color)

    
    def create_origin_select_button(self, frame, command_func):
        origin_select_button = tk.Button(frame, command=command_func, text='SELECT', font=tk.font.Font(size=8))
        origin_select_button.grid(column=2, row=0, sticky=tk.EW)
        return origin_select_button


    def origin_select_button_command_handler(self, event_obj=None):
        if event_obj != None:
            if self.currently_active_listbox_obj == self.origin_favorites_listbox:
                if event_obj.keysym == 'Return':
                    self.origin_select_button.invoke()
        elif self.currently_active_listbox_obj == self.dir_listbox:
            self.origin_selected = self.omni_select_command_get_dir(self.origin_entry_widget)
        elif self.currently_active_listbox_obj == self.origin_favorites_listbox:
            self.origin_selected = self.omni_select_command_get_favorite(self.origin_entry_widget, self.origin_favorites_listbox, self.origin_favorites_data)

    
    def create_origin_favorites_button(self, frame, command_func):
        origin_favorites_button = tk.Button(frame, command=command_func, text='FAVORITES', font=tk.font.Font(size=7))
        origin_favorites_button.grid(column=1, row=1, columnspan=2, sticky=tk.EW)
        return origin_favorites_button

    
    def origin_favorites_button_command(self):
        if self.currently_active_listbox_obj == self.target_dir_favorites_listbox:
            self.target_dir_favorites_button.invoke()
        if self.currently_active_listbox_obj != self.origin_favorites_listbox:
            self.currently_active_listbox_obj = self.origin_favorites_listbox
            self.origin_favorites_base_frame.lift()
            self.origin_favorites_button.configure(relief=tk.SUNKEN)
            self.origin_favorites_button.configure(bg='dark grey')
        else:
            self.currently_active_listbox_obj = self.dir_listbox
            self.origin_favorites_base_frame.lower()
            self.origin_favorites_button.configure(relief=tk.RAISED)
            self.origin_favorites_button.configure(bg=self.default_color)
        self.zero_listbox_sel_and_change_listbox_focus()


    def populate_master_target_dir_entry_widget(self, osnav, parent_frame):
        self.target_dir_labelframe = self.create_target_dir_labelframe(parent_frame)
        self.target_dir_x_scrollbar = self.create_target_dir_x_scrollbar(self.target_dir_labelframe)
        self.target_dir_entry_widget = self.create_target_dir_entry_widget(self.target_dir_labelframe, self.target_dir_x_scrollbar)
        self.link_target_dir_x_scrollbar_to_entry_widget(self.target_dir_labelframe, self.target_dir_x_scrollbar, self.target_dir_entry_widget)
        self.target_dir_save_button = self.create_target_dir_save_button(self.target_dir_labelframe, self.target_dir_save_button_command_handler)
        self.target_dir_select_button = self.create_target_dir_select_button(self.target_dir_labelframe, self.target_dir_select_button_command_handler)
        self.target_dir_favorites_button = self.create_target_dir_favorites_button(self.target_dir_labelframe, self.target_dir_favorites_button_command)
        self.target_dir_save_info_entry, self.target_dir_save_entry = self.create_target_dir_save_entry_widget_pair(self.target_dir_labelframe)
        self.target_dir_cancel_button = self.create_target_dir_cancel_button(self.target_dir_labelframe, self.target_dir_cancel_button_command_handler)
        self.target_dir_favorites_base_frame, self.target_dir_favorites_x_scrollbar, self.target_dir_favorites_y_scrollbar, self.target_dir_favorites_canvas, self.target_dir_favorites_listbox, self.target_dir_favorites_inner_frame, self.target_dir_favorites_option_buttons = self.create_favorites_overlay_omni_overseer((self.dir_listbox.cget('width'), self.dir_listbox.cget('height')), 'target_dir_favorites_default', self.target_dir_favorites_data)
        self.target_dir_favorites_listbox.bind('<Return>', self.target_dir_select_button_command_handler)


    def create_target_dir_labelframe(self, frame):
        target_dir_labelframe = tk.LabelFrame(frame, text="Target Directory", relief=tk.RIDGE, padx=2)
        target_dir_labelframe.grid(column=0, row=2, pady=5)
        return target_dir_labelframe

    
    def create_target_dir_x_scrollbar(self, frame):
        target_dir_x_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        target_dir_x_scrollbar.grid(column=0, row=1, sticky=tk.EW)
        return target_dir_x_scrollbar
    

    def create_target_dir_entry_widget(self, frame, x_scrollbar):
        target_dir_entry_widget = tk.Entry(frame, xscrollcommand=x_scrollbar.set, width=30, state=tk.DISABLED, disabledbackground='white', disabledforeground='black')
        target_dir_entry_widget.grid(column=0, row=0, padx=1, sticky=tk.S)
        return target_dir_entry_widget

    
    def create_target_dir_save_entry_widget_pair(self, frame):
        target_dir_save_info_entry = tk.Entry(frame, width=12, disabledbackground='WHITE', disabledforeground='BLACK')
        target_dir_save_info_entry.insert(0, ' SAVE NAME')
        target_dir_save_info_entry.configure(state=tk.DISABLED)
        target_dir_save_info_entry.grid(column=0, row=0, padx=1, sticky=tk.SW)
        target_dir_save_info_entry.lower()
        target_dir_save_entry = tk.Entry(frame, width=18, state=tk.DISABLED)
        target_dir_save_entry.grid(column=0, row=0, padx=1, sticky=tk.SE)
        target_dir_save_entry.lower()
        return target_dir_save_info_entry, target_dir_save_entry

    
    def link_target_dir_x_scrollbar_to_entry_widget(self, frame, x_scrollbar, entry_widget):
        x_scrollbar.configure(command=entry_widget.xview)

    
    def create_target_dir_save_button(self, frame, command_func):
        target_dir_save_button = tk.Button(frame, command=command_func, text="SAVE", font=tk.font.Font(size=8))
        target_dir_save_button.grid(column=1, row=0)
        return target_dir_save_button

    
    def target_dir_save_button_command_handler(self):
        if self.target_dir_entry_widget.get() == "":
            return
        if self.target_dir_save_entry.cget('state') == tk.DISABLED:
            self.target_dir_save_info_entry.lift()
            self.target_dir_save_entry.lift()
            self.target_dir_save_entry.configure(state=tk.NORMAL)
            self.target_dir_save_entry.focus_set()
            self.target_dir_cancel_button.lift()
            self.target_dir_save_button.configure(bg='lime')
            self.target_dir_save_info_entry.configure(xscrollcommand=self.target_dir_x_scrollbar.set)
        elif self.target_dir_save_entry.cget('state') in [tk.NORMAL, tk.ACTIVE]:
            if self.target_dir_save_entry.get() != "":
                self.append_fav_to_favorites_listbox(self.target_dir_favorites_listbox, (self.target_dir_save_entry.get(), self.target_dir_entry_widget.get()))
                self.target_dir_favorites_data.append((self.target_dir_save_entry.get(), self.target_dir_entry_widget.get()))
                self.add_favorites_options_buttons(self.target_dir_favorites_inner_frame, self.target_dir_favorites_listbox, self.target_dir_favorites_option_buttons, self.target_dir_favorites_data, 'origin_favorites_default')
                self.target_dir_cancel_button.invoke()
                self.target_dir_entry_widget.configure(state=tk.NORMAL)
                self.target_dir_entry_widget.delete(0, tk.END)
                self.target_dir_entry_widget.configure(state=tk.DISABLED)
                self.write_favorites_data_to_file()


    def create_target_dir_cancel_button(self, frame, command_func):
        target_dir_cancel_button = tk.Button(frame, command=command_func, text="CANCEL", font=tk.font.Font(size=8), bg='red')
        target_dir_cancel_button.grid(column=2, row=0)
        target_dir_cancel_button.lower()
        return target_dir_cancel_button
    

    def target_dir_cancel_button_command_handler(self):
        self.target_dir_save_info_entry.lower()
        self.target_dir_save_entry.delete(0, tk.END)
        self.target_dir_save_entry.lower()
        self.target_dir_save_entry.configure(state=tk.DISABLED)
        self.target_dir_cancel_button.lower()
        self.target_dir_entry_widget.configure(xscrollcommand=self.target_dir_x_scrollbar.set)
        self.cwd_textbox.focus_set()
        self.cwd_textbox.event_generate('<End>')
        self.target_dir_save_button.configure(bg=self.default_color)
    

    def create_target_dir_select_button(self, frame, command_func):
        target_dir_select_button = tk.Button(frame, command=command_func, text='SELECT', font=tk.font.Font(size=8))
        target_dir_select_button.grid(column=2, row=0, sticky=tk.EW)
        return target_dir_select_button


    def target_dir_select_button_command_handler(self, event_obj=None):
        if event_obj != None:
            if self.currently_active_listbox_obj == self.target_dir_favorites_listbox:
                if event_obj.keysym == 'Return':
                    self.target_dir_select_button.invoke()
        if self.currently_active_listbox_obj == self.dir_listbox:
            self.target_dir_selected = self.omni_select_command_get_dir(self.target_dir_entry_widget)
        elif self.currently_active_listbox_obj == self.target_dir_favorites_listbox:
            self.target_dir_selected = self.omni_select_command_get_favorite(self.target_dir_entry_widget, self.target_dir_favorites_listbox, self.target_dir_favorites_data)


    def create_target_dir_favorites_button(self, frame, command_func):
        target_dir_favorites_button = tk.Button(frame, command=command_func, text='FAVORITES', font=tk.font.Font(size=7))
        target_dir_favorites_button.grid(column=1, row=1, columnspan=2, sticky=tk.EW)
        return target_dir_favorites_button

    
    def target_dir_favorites_button_command(self):
        if self.currently_active_listbox_obj == self.origin_favorites_listbox:
            self.origin_favorites_button.invoke()
        if self.currently_active_listbox_obj != self.target_dir_favorites_listbox:
            self.currently_active_listbox_obj = self.target_dir_favorites_listbox
            self.target_dir_favorites_base_frame.lift()
            self.target_dir_favorites_button.configure(relief=tk.SUNKEN)
            self.target_dir_favorites_button.configure(bg='dark grey')
        else:
            self.currently_active_listbox_obj = self.dir_listbox
            self.target_dir_favorites_base_frame.lower()
            self.target_dir_favorites_button.configure(relief=tk.RAISED)
            self.target_dir_favorites_button.configure(bg=self.default_color)
        self.zero_listbox_sel_and_change_listbox_focus()

    
    def activate_widget_grid_from_grid_info(self, widget, grid_info):
        widget.grid(column=grid_info['column'], row=grid_info['row'], columnspan=grid_info['columnspan'], rowspan=grid_info['rowspan'], sticky=grid_info['sticky'],
                    ipadx=grid_info['ipadx'], ipady=grid_info['ipady'], padx=grid_info['padx'], pady=grid_info['pady'])


    def create_favorites_overlay_omni_overseer(self, listbox_width_height, default_attr, favorites_data=''):
        base_grid_info = self.create_grid_info_dict(row=2, columnspan=2, rowspan=2, sticky=tk.NW, padx=10, pady=0)
        listbox_grid_info = self.create_grid_info_dict(column=1, sticky=tk.NW)
        x_scrollbar_grid_info = self.create_grid_info_dict(row=1, columnspan=2, sticky=tk.EW)
        y_scrollbar_grid_info = self.create_grid_info_dict(column=2, sticky=tk.NS)
        canvas_grid_info = self.create_grid_info_dict(sticky=tk.NW)
        favorites_widgets = self.populate_favorites_overlay_omni(self.master, base_grid_info, listbox_grid_info, ((listbox_width_height[0] - 5), listbox_width_height[1]), x_scrollbar_grid_info,
                                            y_scrollbar_grid_info, canvas_grid_info, self.op_sys_specs['fav_canvas_width_height'], default_attr, favorites_data)
        return favorites_widgets


    def populate_favorites_overlay_omni(self, root_frame, base_frame_grid, listbox_grid, listbox_width_height, x_scrollbar_grid, y_scrollbar_grid, canvas_grid, canvas_width_height, default_attr, favorites_data):
        favorites_base_frame = self.create_favorites_overlay_frame(root_frame, base_frame_grid)
        favorites_base_frame.lower()

        favorites_x_scrollbar = self.create_favorites_overlay_xory_scrollbar(favorites_base_frame, x_scrollbar_grid, scrollbar_orient=tk.HORIZONTAL)
        favorites_y_scrollbar = self.create_favorites_overlay_xory_scrollbar(favorites_base_frame, y_scrollbar_grid)
        favorites_canvas = self.create_favorites_overlay_canvas(favorites_base_frame, canvas_width_height, canvas_grid)
        listbox_width_height = (listbox_width_height[0] + self.op_sys_specs['fav_listbox_width_height'][0], listbox_width_height[1] + self.op_sys_specs['fav_listbox_width_height'][1])
        favorites_listbox = self.create_favorites_overlay_listbox(favorites_base_frame, listbox_width_height, favorites_x_scrollbar, listbox_grid, favorites_data, default_attr)
        favorites_inner_frame = self.create_favorites_overlay_inner_frame(favorites_canvas, canvas_width_height, canvas_grid, [('pady', 2)])
        favorites_option_buttons = self.create_favorites_options_buttons(favorites_inner_frame, favorites_listbox, self.favorites_delete_buttons_command_factory_func, self.favorites_default_buttons_command_factory_func, favorites_data, default_attr)
        
        self.link_favorites_scrollbars_to_listbox(favorites_listbox, favorites_x_scrollbar, favorites_y_scrollbar)
        favorites_inner_frame.update()
        favorites_canvas.create_window(0, 2, window=favorites_inner_frame, anchor=tk.N)
        favorites_canvas.configure(scrollregion=favorites_canvas.bbox('all'))
        favorites_listbox.configure(yscrollcommand=self.multi_widget_y_scroll_factory_func(favorites_listbox, favorites_canvas, favorites_y_scrollbar))

        return favorites_base_frame, favorites_x_scrollbar, favorites_y_scrollbar, favorites_canvas, favorites_listbox, favorites_inner_frame, favorites_option_buttons

        
    def create_favorites_overlay_frame(self, root_frame, base_frame_grid):
        favorites_base_frame = tk.LabelFrame(root_frame, padx=1, pady=1)
        self.activate_widget_grid_from_grid_info(favorites_base_frame, base_frame_grid)
        return favorites_base_frame

    
    def multi_widget_y_scroll_factory_func(self, invoking_widget, *widget_args):
            yview_widgets = []
            y_scrollbar_widgets = []
            for x in range(len(widget_args)):
                if hasattr(widget_args[x], 'yview'):
                    yview_widgets.append(widget_args[x])
                elif isinstance(widget_args[x], tk.Scrollbar) and widget_args[x].cget('orient') == tk.VERTICAL:
                    y_scrollbar_widgets.append(widget_args[x])
            def multi_widget_y_scrollbar_func(*args):
                for x in range(len(yview_widgets)):
                    if yview_widgets[x].yview() != invoking_widget.yview():
                        yview_widgets[x].yview_moveto(args[0])
                for x in range(len(y_scrollbar_widgets)):
                    y_scrollbar_widgets[x].set(*args)
            return multi_widget_y_scrollbar_func


    def favorites_delete_buttons_command_factory_func(self, frame, invoking_widget, partner_widget, listbox_widget, favorites_buttons_list, favorites_data):
        def favorites_delete_buttons_command(*args):
            listbox_index = invoking_widget.grid_info()['row'] + listbox_widget.nearest(0)
            listbox_widget.delete(listbox_index)
            del favorites_data[listbox_index]
            if listbox_widget.size() < listbox_widget.cget('height'):
                self.remove_favorites_options_buttons(favorites_buttons_list)
            self.write_favorites_data_to_file()
        return favorites_delete_buttons_command

    
    def favorites_default_buttons_command_factory_func(self, frame, invoking_widget, listbox_widget, favorites_buttons_list, favorites_data, default_attr):
        def favorites_default_buttons_command(*args):
            listbox_index = invoking_widget.grid_info()['row'] + listbox_widget.nearest(0)
            if listbox_widget.itemcget(0, 'bg') == 'black':
                listbox_widget.itemconfigure(0, bg='white', fg='black')
                if listbox_index == 0:
                    setattr(self, default_attr, None)
            else:
                default_text = listbox_widget.get(listbox_index)
                listbox_widget.delete(listbox_index)
                listbox_widget.insert(0, default_text)
                favorites_data.insert(0, favorites_data.pop(listbox_index))
                listbox_widget.itemconfigure(0, bg='black', fg='gold')
                setattr(self, default_attr, favorites_data[0])
            self.write_favorites_data_to_file()
        return favorites_default_buttons_command

    
    def create_grid_info_dict(self, *, column=0, row=0, columnspan=1, rowspan=1, sticky='', ipadx=0, ipady=0, padx=0, pady=0):
        return {'column': column, 'row': row, 'columnspan': columnspan, 'rowspan': rowspan, 'sticky': sticky, 'ipadx': ipadx, 'ipady': ipady, 'padx': padx, 'pady': pady}


    def create_favorites_overlay_xory_scrollbar(self, frame, scrollbar_grid, scrollbar_orient=tk.VERTICAL):
        favorites_x_scrollbar = tk.Scrollbar(frame, orient=scrollbar_orient)
        self.activate_widget_grid_from_grid_info(favorites_x_scrollbar, scrollbar_grid)
        return favorites_x_scrollbar

    
    def create_favorites_overlay_canvas(self, frame, canvas_width_height, canvas_grid):
        favorites_canvas = tk.Canvas(frame, width=canvas_width_height[0], height=canvas_width_height[1])
        self.activate_widget_grid_from_grid_info(favorites_canvas, canvas_grid)
        return favorites_canvas


    def create_favorites_overlay_listbox(self, frame, listbox_width_height, x_scrollbar, listbox_grid, favorites_data, default_attr):
        favorites_listbox = tk.Listbox(frame, width=listbox_width_height[0], height=listbox_width_height[1], xscrollcommand=x_scrollbar.set) #, font=self.op_sys_specs['font'])
        self.activate_widget_grid_from_grid_info(favorites_listbox, listbox_grid)
        if len(favorites_data) > 0:
            [favorites_listbox.insert(x, f" {favorites_data[x][0]} «{favorites_data[x][1]}» ") for x in range(len(favorites_data))]
            if getattr(self, default_attr) == favorites_data[0]:
                favorites_listbox.itemconfigure(0, bg='black', fg='gold')
        return favorites_listbox


    def append_fav_to_favorites_listbox(self, listbox, fav_data):
        listbox.insert(tk.END, f" {fav_data[0]} «{fav_data[1]}» ")


    def link_favorites_scrollbars_to_listbox(self, listbox, x_scrollbar, y_scrollbar):
        x_scrollbar.configure(command=listbox.xview)
        y_scrollbar.configure(command=listbox.yview)

    
    def create_favorites_overlay_inner_frame(self, frame, inner_frame_width_height, inner_frame_grid, inner_frame_grid_mods=tuple()):
        favorites_inner_frame = tk.Frame(frame, width=inner_frame_width_height[0], height=inner_frame_width_height[1])
        for x in range(len(inner_frame_grid_mods)):
            inner_frame_grid[inner_frame_grid_mods[x][0]] = inner_frame_grid_mods[x][1]
        self.activate_widget_grid_from_grid_info(favorites_inner_frame, inner_frame_grid)
        return favorites_inner_frame


    def create_favorites_options_buttons(self, frame, listbox_widget, delete_command_factory_func, default_command_factory_func, favorites_data, default_attr):
        if len(favorites_data) > 0:
            favorites_buttons_list = [(self.create_favorites_delete_button(frame, 0, x), self.create_favorites_default_button(frame, 1, x)) for x in range(listbox_widget.cget('height')) if x < len(favorites_data)]
            [(favorites_buttons_list[x][0].configure(command=delete_command_factory_func(frame, favorites_buttons_list[x][0], favorites_buttons_list[x][1], listbox_widget, favorites_buttons_list, favorites_data)),
            favorites_buttons_list[x][1].configure(command=default_command_factory_func(frame, favorites_buttons_list[x][1], listbox_widget, favorites_buttons_list, favorites_data, default_attr))) for x in range(len(favorites_buttons_list))]
        else:
            favorites_buttons_list = []
        return favorites_buttons_list


    def add_favorites_options_buttons(self, frame, listbox_widget, favorites_buttons_list, favorites_data, default_attr):
        if listbox_widget.size() < listbox_widget.cget('height'):        
            favorites_buttons_list.append((self.create_favorites_delete_button(frame, 0, len(favorites_buttons_list)), self.create_favorites_default_button(frame, 1, len(favorites_buttons_list))))
            favorites_buttons_list[-1][0].configure(command=self.favorites_delete_buttons_command_factory_func(frame, favorites_buttons_list[-1][0], favorites_buttons_list[-1][1], listbox_widget, favorites_buttons_list, favorites_data))
            favorites_buttons_list[-1][1].configure(command=self.favorites_default_buttons_command_factory_func(frame, favorites_buttons_list[-1][1], listbox_widget, favorites_buttons_list, favorites_data, default_attr))


    def remove_favorites_options_buttons(self, favorites_buttons_list):
        button_widgets = favorites_buttons_list.pop()
        button_widgets[0].destroy()
        button_widgets[1].destroy()

    
    def create_favorites_delete_button(self, frame, column_pos, row_pos):
        favorites_delete_button = tk.Button(frame, relief=tk.RIDGE, border=1, bg='red')
        pady_val = 1
        if self.photoimage_library_get('delete_icon') != None:
            favorites_delete_button.configure(image=self.photoimage_library_get('delete_icon'))
        else:
            favorites_delete_button.configure(text='X', font=tk.font.Font(size=6))
            pady_val = 0
        favorites_delete_button.grid(column=column_pos, row=row_pos, sticky=tk.N, pady=pady_val)
        return favorites_delete_button

    
    def create_favorites_default_button(self, frame, column_pos, row_pos):
        favorites_default_button = tk.Button(frame, relief=tk.RIDGE, border=1)
        pady_val = 1
        if self.photoimage_library_get('favorite_icon') != None:
            favorites_default_button.configure(image=self.photoimage_library_get('favorite_icon'))
        else:
            favorites_default_button.configure(text='FAV', font=tk.font.Font(size=6), bg='black', fg='gold')
            pady_val = 0
        favorites_default_button.grid(column=column_pos, row=row_pos, sticky=tk.N, pady=pady_val)
        return favorites_default_button

        
    def omni_select_command_get_dir(self, widget):
        cwd_dir = self.get_cwd_stringvar()
        widget.configure(state=tk.NORMAL)
        widget.delete(0, len(widget.get()))
        widget.insert(0, cwd_dir)
        widget.configure(state=tk.DISABLED)
        widget.xview_moveto(1)
        return cwd_dir

    
    def omni_select_command_get_favorite(self, widget, favorites_listbox, favorites_data):
        if favorites_listbox.size() == 0:
            return ""
        index_selected = favorites_listbox.curselection()[0]
        dir_selected = favorites_data[index_selected][1]
        widget.configure(state=tk.NORMAL)
        widget.delete(0, len(widget.get()))
        widget.insert(0, dir_selected)
        widget.configure(state=tk.DISABLED)
        widget.xview_moveto(1)
        return dir_selected

    
    def populate_master_copy_button(self, osnav):
        self.copy_button_frame = self.create_copy_button_frame(self.master)
        self.copy_button = self.create_copy_button(self.copy_button_frame, self.copy_button_command)


    def create_copy_button_frame(self, frame):
        copy_button_frame = tk.Frame(frame)
        copy_button_frame.grid(column=1, row=3, sticky=tk.N)
        return copy_button_frame
    

    def create_copy_button(self, frame, command_func):
        copy_button = tk.Button(frame, command=command_func, bg='white', fg='navy', relief=tk.RIDGE, border=3)
        if self.photoimage_library_get('master_copy_icon') != None:
            copy_button.configure(image=self.photoimage_library_get('master_copy_icon'))
        else:
            copy_button.configure(text='CLONE', font=tk.font.Font(size=18), bg='Red2', fg='dark turquoise')
        copy_button.grid(column=0, row=0, sticky=tk.N)
        return copy_button

    
    def copy_button_command(self):
        copy_path = self.origin_selected
        target_dir_selected = self.target_dir_selected
        new_folder_name = self.filename_entry_widget.get()
        if copy_path == None or target_dir_selected == None or copy_path == target_dir_selected or new_folder_name in [None, '']:
            print(f"FAILURE: copy:{copy_path}, target:{target_dir_selected}, name:'{new_folder_name}'")
            if copy_path == None:
                pass
            if target_dir_selected == None:
                pass
            if new_folder_name == '':
                pass
            return
        #TODO:func/s to validate folder-name (does not already exist, no illegal characters, not blank, etc)
        full_copy_path = self.osnav.join_paths(target_dir_selected, new_folder_name)

        if full_copy_path != None:
            #Shutilizer.copytree_to_dst(copy_path, full_copy_path)
            pass
        print(f"\ncopy_path:{copy_path}\nfull_copy_path:{full_copy_path}")


if __name__ == "__main__":
    master_window = MasterWindow()
    master_window.master.mainloop()