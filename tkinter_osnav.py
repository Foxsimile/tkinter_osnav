import tkinter as tk, tkinter.font as tk_font
from tkinter import ttk
import os, string
from osnavigator import OSNavigator


class MasterWindow:
    def __init__(self):
        self.master = self.create_master()
        self.osnav = OSNavigator()
        self.cwd_labelframe = None
        self.cwd_scrollbar = None
        self.cwd_stringvar = None
        self.cwd_scrollbar = None
        self.cwd_textbox = None
        self.cwd_textbox_select_indexes = None
        self.cwd_textbox_select_colorset = ('black', 'lawn green')
        self.dir_listbox_labelframe = None
        self.dir_listbox_frame = None
        self.dir_listbox_y_scrollbar = None
        self.dir_listbox_x_scrollbar = None
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
        self.cwd_x_scrollbar = self.create_cwd_x_scrollbar(self.cwd_labelframe)
        self.cwd_stringvar = self.create_cwd_stringvar(osnav)
        self.cwd_textbox = self.create_cwd_textbox(self.cwd_labelframe, self.cwd_stringvar.get(), self.cwd_x_scrollbar)
        self.link_cwd_x_scrollbar_to_textbox(self.cwd_labelframe, self.cwd_x_scrollbar, self.cwd_textbox)


    def create_cwd_labelframe(self, frame):
        cwd_labelframe = tk.LabelFrame(frame, labelanchor=tk.W, height=42, bg='white')
        cwd_labelframe.grid(column=0, row=0, columnspan=2, sticky=tk.NW, padx=20, pady=10)
        return cwd_labelframe

    
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
        cwd_textbox = self.update_cwd_textbox_content(cwd_textbox, cwd_stringvar)
        cwd_textbox_bindings = [('<FocusIn>', self.cwd_textbox_focus_in_handler), ('<FocusOut>', self.cwd_textbox_focus_out_handler),
                                ('<Left>', self.cwd_textbox_keypress_handler), ('<Right>', self.cwd_textbox_keypress_handler), ('<ButtonRelease>', self.cwd_textbox_button_handler),
                                ('<Home>', self.cwd_textbox_keypress_handler), ('<End>', self.cwd_textbox_keypress_handler), ('<Return>', self.cwd_textbox_keypress_handler)]
        [cwd_textbox.bind(cwd_textbox_bindings[x][0], cwd_textbox_bindings[x][1]) for x in range(len(cwd_textbox_bindings))]
        return cwd_textbox


    def update_cwd_textbox_content(self, cwd_textbox, *args):
        cwd_textbox.configure(state=tk.NORMAL)
        cwd_textbox.delete('0.0', tk.END)
        [cwd_textbox.insert(tk.END, args[x]) for x in range(len(args))]
        cwd_textbox.configure(state=tk.DISABLED)
        return cwd_textbox

    
    def textbox_create_and_highlight_tag(self, textbox, tag_name, index_tuple, *, bg_color='cyan', fg_color='white', clear_tag_prev=True):
        if clear_tag_prev == True:
            self.textbox_clear_tag(textbox, tag_name)
        textbox.mark_set('matchStart', index_tuple[0])
        textbox.mark_set('matchEnd', index_tuple[1])
        textbox.tag_add(tag_name, 'matchStart', 'matchEnd')
        textbox.tag_configure(tag_name, background=bg_color, foreground=fg_color)

    
    def textbox_clear_tag(self, textbox, tag_name):
        textbox.tag_delete(tag_name)

    
    def cwd_textbox_keypress_handler(self, event_obj):
        if event_obj.keysym in ['Left', 'Right', 'Home', 'End']:
            self.cwd_textbox_dir_nav_event_handler(event_obj)
        elif event_obj.keysym in ['Return']:
            self.cwd_textbox_chdir_nav_event_handler(event_obj)

    
    def cwd_textbox_button_handler(self, event_obj):
        if event_obj.type.name == 'ButtonRelease':
            self.cwd_textbox_dir_nav_event_handler(event_obj)


    def cwd_textbox_focus_in_handler(self, event_obj):
        self.cwd_textbox.tag_configure('cwd_sel_tag', background='blue')
        self.cwd_textbox.tag_configure('cwd_sel_tag', foreground='white')


    def cwd_textbox_focus_out_handler(self, event_obj):
        self.cwd_textbox.tag_delete('cwd_sel_tag')

    
    def cwd_textbox_dir_nav_event_handler(self, event_obj):
        insertion_index = self.cwd_textbox.index(tk.INSERT)
        cwd_str = self.get_cwd_stringvar()
        textbox_sel_bg_color = self.cwd_textbox_select_colorset[0]
        textbox_sel_fg_color = self.cwd_textbox_select_colorset[1]
        textbox_tag_start_text_index = None
        textbox_tag_end_text_index = None

        if event_obj.keysym in ['Left', 'Right'] or event_obj.type.name == 'ButtonRelease':
            if event_obj.type.name == 'KeyPress':
                if ((modifier := 1) and event_obj.keysym != 'Left'):
                    modifier = -1
            elif event_obj.type.name == 'ButtonRelease':
                modifier = 0
                insertion_index = self.cwd_textbox.index(tk.CURRENT)
                
            line_num_str = insertion_index[:insertion_index.find('.')]
            insertion_index = int(insertion_index[insertion_index.find('.') + 1:]) + 1
            if insertion_index != None:
                if modifier == 0:
                    if (start_index := (cwd_str.rfind('\\ '.strip(' '), 0, insertion_index)) + 1) == len(cwd_str):
                        start_index = 0
                    if (end_index := cwd_str.find('\\ '.strip(' '), insertion_index, len(cwd_str))) == -1:
                        end_index = len(cwd_str)
                elif modifier == 1:
                    if (end_index := (cwd_str.rfind('\\ '.strip(' '), 0, insertion_index))) in [-1, 0]:
                        return "break"
                    if (start_index := cwd_str.rfind('\\ '.strip(' '), 0, end_index - 1) + 1) == -1:
                        return "break"
                elif modifier == -1:
                    if (start_index := cwd_str.find('\\ '.strip(' '), insertion_index, len(cwd_str)) + 1) in [0, -1]:
                        return "break"
                    if (end_index := cwd_str.find('\\ '.strip(' '), start_index, len(cwd_str))) == -1:
                        end_index = len(cwd_str)
                textbox_tag_start_text_index = f"{line_num_str}.{str(start_index)}"
                textbox_tag_end_text_index = f"{line_num_str}.{str(end_index)}"
        
        elif event_obj.keysym in ['Home', 'End']:
            line_num_str = insertion_index[:insertion_index.find('.')]
            if event_obj.keysym == 'Home':
                start_index = 0
                end_index = cwd_str.find('\\ '.strip(' '))
            else:
                start_index = cwd_str.rfind('\\ '.strip(' ')) + 1
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

        
    def populate_master_dir_listbox(self, osnav):
        self.dir_listbox_labelframe = self.create_dir_listbox_labelframe(self.master)
        self.dir_listbox_frame = self.create_dir_listbox_frame(self.dir_listbox_labelframe)
        self.dir_listbox_y_scrollbar = self.create_dir_y_scrollbar(self.dir_listbox_frame)
        self.dir_listbox_x_scrollbar = self.create_dir_x_scrollbar(self.dir_listbox_frame)
        self.dir_listbox = self.create_dir_listbox(self.dir_listbox_frame, self.dir_listbox_y_scrollbar, self.dir_listbox_x_scrollbar, self.osnav, self.dir_listbox_event_handler_overseer)
        self.link_dir_y_scrollbar_to_listbox(self.dir_listbox_frame, self.dir_listbox_y_scrollbar, self.dir_listbox)
        self.link_dir_x_scrollbar_to_listbox(self.dir_listbox_frame, self.dir_listbox_x_scrollbar, self.dir_listbox)
        self.dir_active_intvar = self.create_dir_active_intvar(self.dir_listbox.curselection()[0])


    def create_dir_listbox_labelframe(self, frame):
        dir_listbox_labelframe = tk.LabelFrame(frame)
        dir_listbox_labelframe.grid(column=0, row=2, sticky=tk.W, padx=10, pady=0)
        return dir_listbox_labelframe


    def create_dir_listbox_frame(self, frame):
        dir_listbox_frame = tk.Frame(frame)
        return dir_listbox_frame


    def create_dir_y_scrollbar(self, frame):
        dir_listbox_yscrollbar = tk.Scrollbar(frame)
        dir_listbox_yscrollbar.grid(column=1, row=1, sticky=tk.NSEW)
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
        

    def create_dir_listbox(self, frame, y_scrollbar, x_scrollbar, osnav, event_func):
        dir_listbox = tk.Listbox(frame, yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set, width=25, height=15)
        dir_listbox = self.get_dir_listbox_content(dir_listbox, osnav)
        dir_listbox.grid(column=0, row=1, sticky=tk.W)
        keypress_event_list = ['<KeyPress-Return>', '<KeyPress-BackSpace>', '<KeyPress-Up>', '<KeyPress-Down>']
        [dir_listbox.bind(keypress_event_list[x], event_func) for x in range(len(keypress_event_list))]
        return dir_listbox

    
    def get_dir_listbox_content(self, dir_listbox, osnav):
        dir_listbox.insert(0, ' ' + '--Parent Directory--')
        dir_listbox_spacer_index_list = [1]
        [dir_listbox.insert(tk.END, ' ' + osnav.cwd_scan['dirs'][x].name) for x in range(1, len(osnav.cwd_scan['dirs'])) if osnav.cwd_scan['dirs'][x] != None]
        [(dir_listbox.insert(dir_listbox_spacer_index_list[x], '\n'), osnav.cwd_scan_insert_dir(dir_listbox_spacer_index_list[x], None)) for x in range(len(dir_listbox_spacer_index_list))]
        for x in range(0, dir_listbox.size() - 1):
            if x not in dir_listbox_spacer_index_list:
                dir_listbox.selection_set(x)
                dir_listbox.focus_set()
                break
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
        return dir_active_intvar

    
    def update_dir_listbox_content(self, dir_listbox, osnav):
        dir_listbox.delete(0, tk.END)
        self.get_dir_listbox_content(dir_listbox, osnav)
        return dir_listbox


    def update_widgets_post_dir_change(self):
        self.cwd_stringvar = self.set_cwd_stringvar(self.cwd_stringvar, self.osnav)
        self.cwd_textbox = self.update_cwd_textbox_content(self.cwd_textbox, self.cwd_stringvar.get())
        self.dir_listbox = self.update_dir_listbox_content(self.dir_listbox, self.osnav)
      

if __name__ == "__main__":
    master_window = MasterWindow()
    master_window.master.mainloop()