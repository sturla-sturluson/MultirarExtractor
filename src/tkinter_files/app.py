import tkinter as tk
from tkinter import ttk
from ..utils import get_config_json,find_extracted_file, save_config_json,get_all_found_rar_files_in_tree,get_plural_suffix,cleanup_rar_file
from ..constants import SAVED_PATHS,DELETE_TOGGLED,EXTRACT_TOGGLED,EXECUTE_ALLOWED
from .models import SavedPath, FoundRarFile
from .components import *
from ..extraction import extract_7z_file
from tkinter import filedialog
import threading


class App(tk.Tk):
    action_button_row_label:ttk.Frame
    extract_all_button:ttk.Button
    delete_all_button:ttk.Button
    delete_extracted_button:ttk.Button
    extract_and_delete_button:ttk.Button

    is_extracting:bool = False
    curr_progress:int = 0
    progress_bar:ttk.Progressbar    

    def __init__(self):
        super().__init__()

        self.title("Extract MultiRAR")
        _width = 1000
        _height = 600
        self.geometry(f"{_width}x{_height}")
        self._config = get_config_json()
        self._config[EXECUTE_ALLOWED] = self._config[DELETE_TOGGLED] or self._config[EXTRACT_TOGGLED]

        self._saved_paths:list[SavedPath] = self._config[SAVED_PATHS]

        self.found_rar_files:list[FoundRarFile] = list()
        # Styling
        self._style = get_style()
        # Creating all frames so we can destroy on render
        self._top_frame = ttk.LabelFrame(self, text="Extract MultiRAR")
        self._top_frame.pack(expand=True, fill="both")
        
        self.west_frame = ttk.Frame(self._top_frame)
        self.west_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        self.east_frame = ttk.Frame(self._top_frame)
        self.east_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        # Left frame
        self._render_west_frame(self._top_frame)
        # Right frame
        self._render_east_frame(self._top_frame)

        self._center_window()
        

    def _render_west_frame(self,root:ttk.Frame|ttk.LabelFrame):
        """Renders the left frame"""
        if hasattr(self, "west_frame"):
            self.west_frame.destroy()
        self.west_frame = ttk.Frame(root)
        self.west_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        self._render_toggleable_links_frame(self.west_frame)
        if(hasattr(self, "open_file_dialog_button")):
            self.open_file_dialog_button.destroy()
        self.open_file_dialog_button = styled_button(self.west_frame, "Open file dialog", self._open_file_dialog, size=Size.LARGE, variant=Variant.SECONDARY)
        self.open_file_dialog_button.pack(pady=10)
        # Next show the list of found rar files
        def _search_action():
            self._search_action()
            self._render_found_rar_files(self.east_frame)
        self.search_button = styled_button(self.west_frame, "Search",_search_action, size=Size.XLARGE, variant=Variant.PRIMARY)
        self.search_button.pack(pady=10)

    def _render_east_frame(self,root:ttk.Frame|ttk.LabelFrame):
        """Renders the right frame"""
        if hasattr(self, "east_frame"):
            self.east_frame.destroy()
        self.east_frame = ttk.Frame(root)
        self.east_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        self._render_action_buttons(self.east_frame)
        self._render_found_rar_files(self.east_frame)

    def _render_found_rar_files(self,root:ttk.Frame):
        """Renders the found rar files"""
        if hasattr(self, "found_rar_files_frame"):
            self.found_rar_files_frame.destroy()
        self.found_rar_files_frame = ttk.Frame(root)
        self.found_rar_files_frame.pack(expand=True, fill="both")
        if(self.is_extracting):
            self.progress_bar = ttk.Progressbar(self.found_rar_files_frame, orient="horizontal", length=200, mode="determinate")
            self.progress_bar.pack(pady=10)
            self.progress_bar["value"] = self.curr_progress
            self.progress_bar["maximum"] = len(self.found_rar_files)
        self.count_label = ttk.Label(self.found_rar_files_frame, text=f"{len(self.found_rar_files)} rar file{get_plural_suffix(len(self.found_rar_files),'s')} found")
        self.count_label.pack(pady=5)
        for rar_file in self.found_rar_files:
            found_rar_file_card(self.found_rar_files_frame, rar_file)

    def _extract_action(self, delete_after:bool=False):
        """Extracts the found rar files"""
        # Start by getting all the files that actually need to be extracted
        if(len(self.found_rar_files) == 0):
            return
        self._disable_all_action_buttons()
        self.is_extracting = True
        self._render_found_rar_files(self.east_frame)
        self._extract_thread = threading.Thread(target=self._extract_thread_func, args=(delete_after,))
        self._extract_thread.start()

        self._check_thread()

    def _check_thread(self):
        if self._extract_thread.is_alive():
            # Re-check the thread after 100ms
            self.after(1000, self._check_thread)
        else:
            # Re-enable the button and update the label once loading is complete
            self.is_extracting = False
            self.progress_bar.destroy()
            self._enable_all_action_buttons()
            self._search_action()
            self._render_found_rar_files(self.east_frame)

    def _extract_thread_func(self, delete_after:bool=False):
        """Extracts the found rar files"""
        for i, rar_file in enumerate(self.found_rar_files):
            if rar_file.extracted:
                continue
            extract_7z_file(rar_file.path)
            found_extracted_name = find_extracted_file(rar_file.path)
            rar_file.extracted_filename = found_extracted_name
            self.curr_progress = i + 1
            self._render_found_rar_files(self.east_frame)
            if delete_after:
                cleanup_rar_file(rar_file)
        self.is_extracting = False


    def _delete_extracted_action(self):
        for rar_file in self.found_rar_files:
            if rar_file.extracted:
                cleanup_rar_file(rar_file)
        self._enable_all_action_buttons()
        self._search_action()
        self._render_found_rar_files(self.east_frame)

    def _delete_action(self):
        for rar_file in self.found_rar_files:
            cleanup_rar_file(rar_file)
        self._enable_all_action_buttons()
        self._search_action()
        self._render_found_rar_files(self.east_frame)
        

    def _search_action(self):
        """Searches for the files in the paths"""
        self.found_rar_files = list()
        for saved_path in self._saved_paths:
            if(not saved_path.toggled):
                continue
            self.found_rar_files.extend(get_all_found_rar_files_in_tree(saved_path.path))

    def _render_toggleable_links_frame(self,root:ttk.Frame):
        if hasattr(self, "list_of_toggleable_links"):
            self.list_of_toggleable_links.destroy()
        self.list_of_toggleable_links = list_of_toggleable_links(
            root, self._saved_paths,
              self._toggle_link_button, lambda link: self._delete_link_button(link))




    def _center_window(self):
        """Centers the window on the screen"""
        self.update_idletasks() # Update the window to get correct dimensions
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _update_config_json(self):
        """Updates the config json"""
        new_dict = {
            DELETE_TOGGLED: self._config[DELETE_TOGGLED],
            EXTRACT_TOGGLED: self._config[EXTRACT_TOGGLED],
        }
        new_dict[SAVED_PATHS] = self._saved_paths
        save_config_json(new_dict)

    def _delete_link_button(self, link:SavedPath):
        """Deletes a link button"""
        for saved_path in self._saved_paths:
            if saved_path.path == link.path:
                self._saved_paths.remove(saved_path)
                break
        self._update_config_json()
        self._render_west_frame(self._top_frame)
        
    def _toggle_link_button(self, link:SavedPath):
        """Toggles the button style between On.TButton and TButton"""
        for saved_path in self._saved_paths:
            if saved_path.path == link.path:
                saved_path.toggled = not saved_path.toggled
        self._update_config_json()


    def _open_file_dialog(self):
        file_path = filedialog.askdirectory()
        if file_path:
            saved_path = SavedPath(file_path, True)
            self._saved_paths.append(saved_path)
            self._update_config_json()
            self._render_west_frame(self._top_frame)

    def _disable_all_action_buttons(self):
        """Disables all action buttons"""
        self.extract_all_button.config(state="disabled")
        self.delete_all_button.config(state="disabled")
        self.delete_extracted_button.config(state="disabled")
        self.extract_and_delete_button.config(state="disabled")
        self.search_button.config(state="disabled")


    def _enable_all_action_buttons(self):
        """Enables all action buttons"""
        self.extract_all_button.config(state="normal")
        self.delete_all_button.config(state="normal")
        self.delete_extracted_button.config(state="normal")
        self.extract_and_delete_button.config(state="normal")
        self.search_button.config(state="normal")
    
    def _render_action_buttons(self,root:ttk.Frame):
        """Renders the action buttons for the found rar files"""
        if hasattr(self, "action_button_row_label"):
            self.action_button_row_label.destroy()
        self.action_button_row_label = ttk.Frame(root)
        self.action_button_row_label.pack(pady=10, fill="x")
        _button_size = Size.FIT
        # First button is extract all button
        self.extract_all_button = styled_button(self.action_button_row_label, "Extract All", self._extract_action,size=_button_size, variant=Variant.PRIMARY)
        self.extract_all_button.grid(row=0, column=0, padx=5)
        # Delete all button
        self.delete_all_button = styled_button(self.action_button_row_label, "Delete All", self._delete_action, size=_button_size, variant=Variant.DANGER)
        self.delete_all_button.grid(row=0, column=1, padx=5)
        # Delete extracted button
        self.delete_extracted_button = styled_button(self.action_button_row_label, "Delete Extracted", self._delete_extracted_action, size=_button_size, variant=Variant.PRIMARY)
        self.delete_extracted_button.grid(row=0, column=2, padx=5)
        # Extract and then delete
        self.extract_and_delete_button = styled_button(self.action_button_row_label, "Extract and Delete", self._extract_action, size=_button_size, variant=Variant.DANGER)
        self.extract_and_delete_button.grid(row=0, column=3, padx=5)