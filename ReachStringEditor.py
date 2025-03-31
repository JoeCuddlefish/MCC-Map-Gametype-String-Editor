import os
import tkinter as tk
from tkinter import filedialog, messagebox

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reach Map & Gametype String Editor")
        self.geometry("600x275")  # Adjusted to accommodate the new entry widget
        self.last_dir = os.path.expanduser("~")
        self.initial_dir = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Halo The Master Chief Collection\\haloreach\\map_variants"
        self.file_selected = False
        self.current_file_path = ""  # To store the full path of the currently selected file
        self.default_path = self.initial_dir
        self.create_widgets()
        self.update_file_path_entry(self.initial_dir)

    def create_widgets(self):
        # New Row 0: Default Path Selection
        self.path_selection_frame = tk.Frame(self)
        self.path_selection_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        
        self.path_label = tk.Label(self.path_selection_frame, text="Change Default Path:")
        self.path_label.pack(side="left", padx=5)
        
        self.platform_var = tk.StringVar(value="Steam")
        self.platform_menu = tk.OptionMenu(self.path_selection_frame, self.platform_var, "Steam", "Windows Store", command=self.update_path)
        self.platform_menu.pack(side="left", padx=5)
        
        self.path_type_var = tk.StringVar(value="Built-In Map Variants")
        self.path_type_menu = tk.OptionMenu(self.path_selection_frame, self.path_type_var, "Built-In Map Variants", "Saved Map Variants", "Built-In Game Variants", "Saved Game Variants", command=self.update_path)
        self.path_type_menu.pack(side="left", padx=5)

        # Row 1: File Browse
        self.file_frame = tk.Frame(self)
        self.file_frame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=5)

        # Configure column weights within the file_frame
        self.file_frame.grid_columnconfigure(1, weight=1)  # This makes the Label's column expandable

        self.browse_button = tk.Button(self.file_frame, text="Browse File", command=self.browse_file)
        self.browse_button.grid(row=0, column=0, padx=(0, 49), sticky='w')

        # Using a StringVar to store the path and set it on the label
        self.file_path_var = tk.StringVar()
        self.file_path_label = tk.Label(self.file_frame, textvariable=self.file_path_var, relief="sunken", anchor='w')
        self.file_path_label.grid(row=0, column=1, sticky="ew", padx=(0, 45))  # Set the Label to expand

        self.copy_path_button = tk.Button(self.file_frame, text="Copy", command=lambda: self.copy_to_clipboard(self.file_path_var.get()))
        self.copy_path_button.grid(row=0, column=2, sticky='w')

        # Row 2: File Name
        self.setup_label_entry_copy("File Name:", 2, push_copy_to_right=True)

        # Row 3: Title with character count
        self.title_var = tk.StringVar()
        self.title_var.trace("w", lambda *args: self.update_char_count(self.title_var, self.title_count, 32))
        self.setup_label_entry_copy_with_count("Title:", 3, self.title_var, 32)

        # Row 4: Description with character count
        self.desc_label = tk.Label(self, text="Description:")
        self.desc_label.grid(row=4, column=0, sticky="w", padx=10)
        self.desc_text = tk.Text(self, height=4)
        self.desc_text.grid(row=4, column=1, sticky="ew")
        self.desc_text.bind("<KeyRelease>", lambda e: self.update_text_count(self.desc_count, 127))
        self.desc_count = tk.Label(self, text="0/127")
        self.desc_count.grid(row=4, column=2)
        self.copy_desc_button = tk.Button(self, text="Copy", command=lambda: self.copy_to_clipboard(self.desc_text.get("1.0", "end-1c")))
        self.copy_desc_button.grid(row=4, column=3, padx=10)

        # Row 5: Alphebatize Folder and Save Changes Buttons
        self.alphabetize_button = tk.Button(self, text="Alphabetize Folder", command=self.alphabetize_folder)
        self.alphabetize_button.grid(row=5, column=0, pady=10, padx=10, sticky='e')  # Adjust row/column as needed
        self.save_button = tk.Button(self, text="Save Changes", command=self.save_changes)
        self.save_button.grid(row=5, column=1, columnspan=3, pady=10)

        # Row 6: Start With Label and Entry
        self.start_with_label = tk.Label(self, text="Apply Prefix:")
        self.start_with_label.grid(row=6, column=0, padx=10, pady=0, sticky='w')

        self.start_with_entry = tk.Entry(self)
        self.start_with_entry.grid(row=6, column=1, padx=0, pady=0, sticky='w')

        # # Row 7-8: Checkboxes for File Name and Map Name
        # self.file_name_label = tk.Label(self, text="File Name:")
        # self.file_name_label.grid(row=7, column=0, padx=10, pady=5, sticky='w')

        # self.file_name_var = tk.BooleanVar(value=True)  # Default checked
        # self.file_name_check = tk.Checkbutton(self, variable=self.file_name_var)
        # self.file_name_check.grid(row=7, column=1, padx=0, pady=0, sticky='w')

        # self.map_name_label = tk.Label(self, text="Map Name:")
        # self.map_name_label.grid(row=8, column=0, padx=10, pady=0, sticky='w')

        # self.map_name_var = tk.BooleanVar(value=False)  # Default unchecked
        # self.map_name_check = tk.Checkbutton(self, variable=self.map_name_var)
        # self.map_name_check.grid(row=8, column=1, padx=0, pady=0, sticky='w')

        self.grid_columnconfigure(1, weight=1)  # Make the middle column expandable

    def update_path(self, _):
        platform = self.platform_var.get()
        path_type = self.path_type_var.get()
        
        # Define the paths for each combination of platform and path type
        paths = {
            ("Steam", "Built-In Map Variants"): "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Halo The Master Chief Collection\\haloreach\\map_variants",
            ("Steam", "Saved Game Variants"): self.get_dynamic_path(subfolder="GameType"),
            ("Steam", "Built-In Game Variants"): "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Halo The Master Chief Collection\\haloreach\\game_variants",
            ("Steam", "Saved Map Variants"): self.get_dynamic_path(subfolder="Map"),
            # Add paths for "Windows Store" options, which I will leave as placeholders for you to fill in
            ("Windows Store", "Built-In Map Variants"): "C:\\XboxGames\\Halo- The Master Chief Collection\\Content\\haloreach\\map_variants",
            ("Windows Store", "Saved Map Variants"): self.get_dynamic_path(subfolder="GameType"),
            ("Windows Store", "Built-In Game Variants"): "C:\\XboxGames\\Halo- The Master Chief Collection\\Content\\haloreach\\game_variants",
            ("Windows Store", "Saved Game Variants"): self.get_dynamic_path(subfolder="Map"),
        }

        # Update the default path based on the current selections
        new_default_path = paths.get((platform, path_type), self.initial_dir)

        if new_default_path is None:
            messagebox.showerror("Error", "Could not construct the path. Please check your settings.")
        else:
            self.default_path = new_default_path
            self.last_dir = self.default_path
            self.file_selected = True
            self.update_file_path_entry(self.last_dir)  # Update the text box with the new path

            self.file_name_entry.delete(0, tk.END)
            self.title_entry.delete(0, tk.END)
            self.desc_text.delete('1.0', tk.END)
            self.current_file_path = ""  # To store the full path of the currently selected file
            # print("Default path updated to:", self.default_path)

    def get_dynamic_path(self, subfolder="GameType"):
        user_profile = os.environ['USERPROFILE']  # Gets the user profile directory
        local_low_path = os.path.join(user_profile, "AppData", "LocalLow", "MCC", "LocalFiles")
        unique_subdir_path = None

        try:
            for entry in os.listdir(local_low_path):
                full_entry_path = os.path.join(local_low_path, entry)
                if os.path.isdir(full_entry_path):
                    dirs_inside = [d for d in os.listdir(full_entry_path) if os.path.isdir(os.path.join(full_entry_path, d))]
                    if len(dirs_inside) == 1:
                        unique_subdir = dirs_inside[0]
                        # Check if 'HaloReach' is already part of the unique_subdir path
                        if 'HaloReach' in unique_subdir:
                            unique_subdir_path = os.path.join(full_entry_path, unique_subdir, subfolder)
                        else:
                            unique_subdir_path = os.path.join(full_entry_path, unique_subdir, "HaloReach", subfolder)
                        break
        except Exception as e:
            print(f"Error finding dynamic path: {e}")
            return None

        return unique_subdir_path

    def alphabetize_folder(self):
        dir_to_use = self.last_dir if self.file_selected else self.initial_dir
        folder_path = filedialog.askdirectory(initialdir=dir_to_use)
        self.last_dir = folder_path
        if not folder_path:
            return  # User cancelled the folder selection

        # Confirm the action with the user
        if not messagebox.askokcancel("Confirm Alphabetization", "This action will rename all '.mvar' and '.bin' files in the selected folder to their title names. This action is permanent. Please ensure you have a backup of your files."):
            return  # User cancelled the action

        # Perform the renaming action
        self.rename_files_in_folder(folder_path)

    def rename_files_in_folder(self, folder_path):
        start_with_prefix = self.start_with_entry.get()  # Get the prefix from the entry widget
        renamed_files_count = 0  # To keep track of how many files were renamed
        ignored_files_count = 0  # To keep track of how many files were ignored
        self.update_file_path_entry(self.last_dir)  # Update the text box with the new path
        self.file_selected = True

        try:
            renamed_files = {}  # Dictionary to keep track of renamed files and their counts
            for filename in os.listdir(folder_path):
                if filename.endswith((".mvar", ".bin")) and filename not in excluded_files:
                    # Perform the renaming action for this file
                    file_path = os.path.join(folder_path, filename)
                    file_extension = os.path.splitext(filename)[1]  # Get the file extension

                    # Read the entire file into memory (ensure the file is not too large for this operation)
                    with open(file_path, 'rb') as file:
                        file_data = file.read()

                    # Extract the title from the file
                    title, description = read_string_at_offset(file_data)
                    title = self.sanitize_title(title)

                    # Generate the new filename with prefix and without count
                    new_filename = f"{start_with_prefix}{title}{file_extension}"
                    new_file_path = os.path.join(folder_path, new_filename)

                    # Check if the file's current name already matches the new name
                    if os.path.basename(file_path) != new_filename:
                        # Check for duplicates and rename if necessary
                        count = renamed_files.get(title, 0)
                        while os.path.exists(new_file_path):
                            count += 1
                            new_filename = f"{start_with_prefix}{title}({count}){file_extension}"
                            new_file_path = os.path.join(folder_path, new_filename)

                        os.rename(file_path, new_file_path)
                        renamed_files[title] = count
                        renamed_files_count += 1
                else:
                    # This file is in the list of excluded files, so we skip renaming it
                    ignored_files_count += 1

            messagebox.showinfo("Success", f"{renamed_files_count} files have been renamed successfully.\n{ignored_files_count} default or incompatible files were ignored to protect game file integrity.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def sanitize_title(self, filename):
        invalid_chars = '<>:"/\\|?*'
        invalid_chars += ''.join(chr(i) for i in range(32))  # Adding control characters
        for char in invalid_chars:
            filename = filename.replace(char, '')
        return filename

    def setup_label_entry_copy(self, label, row, push_copy_to_right=False):
        label_widget = tk.Label(self, text=label)
        label_widget.grid(row=row, column=0, sticky="w", padx=10)
        
        entry = tk.Entry(self)
        entry.grid(row=row, column=1, sticky="ew", padx=(0, 0), columnspan=1)  # Span two columns and pad on the right

        copy_button = tk.Button(self, text="Copy", command=lambda: self.copy_to_clipboard(entry.get()))
        if push_copy_to_right:
            copy_button.grid(row=row, column=3, sticky="e", padx=10)
        else:
            copy_button.grid(row=row, column=2, padx=10)

        # Assign the entry to the corresponding class attribute if needed
        if label == "File Name:":
            self.file_name_entry = entry

    def setup_label_entry_copy_with_count(self, label, row, textvar, limit):
        tk.Label(self, text=label).grid(row=row, column=0, sticky="w", padx=10)
        entry = tk.Entry(self, textvariable=textvar)
        entry.grid(row=row, column=1, sticky="ew")
        char_count_label = tk.Label(self, text=f"0/{limit}")
        char_count_label.grid(row=row, column=2)
        copy_button = tk.Button(self, text="Copy", command=lambda: self.copy_to_clipboard(textvar.get()))
        copy_button.grid(row=row, column=3, padx=10)
        if label == "Title:":
            self.title_entry = entry
            self.title_count = char_count_label

    def update_char_count(self, sv, count_label, limit):
        count = len(sv.get())
        count_label.config(text=f"{count}/{limit}")

    def update_text_count(self, count_label, limit, event=None):
        # If called from an event, event.widget can be used to get the Text widget
        # Otherwise, use self.desc_text directly
        text_widget = event.widget if event else self.desc_text
        count = len(text_widget.get("1.0", "end-1c").rstrip())
        count_label.config(text=f"{count}/{limit}")

    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        
    def browse_file(self):
        dir_to_use = self.initial_dir if not self.file_selected else self.last_dir
        file_path = filedialog.askopenfilename(initialdir=dir_to_use, filetypes=[("Binary Files", "*.bin;*.dat;*.mvar")])
        if file_path:
            self.current_file_path = file_path
            self.last_dir = os.path.dirname(file_path)
            self.file_selected = True

            # Read the entire file into memory (ensure the file is not too large for this operation)
            with open(file_path, 'rb') as file:
                file_data = file.read()

            # Use the new function to extract title and description
            title, description = read_string_at_offset(file_data)

            # Extract and display the file name
            file_name = os.path.basename(file_path)
            self.file_name_entry.delete(0, tk.END)
            self.file_name_entry.insert(0, file_name)

            # Update title and description fields
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, title)
            self.desc_text.delete('1.0', tk.END)
            self.desc_text.insert('1.0', description)

            # Explicitly update the description character count after setting the text
            self.update_text_count(self.desc_count, 127)
            self.update_file_path_entry(self.last_dir)  # Update the label with the new path

    def update_file_path_entry(self, path):
        self.file_path_var.set(path)  # Update the StringVar associated with the Label

    def save_changes(self):
        if os.path.basename(self.current_file_path) in excluded_files:
            messagebox.showerror("Error", "This file is protected and cannot be renamed.")
            return
        
        new_title = self.title_entry.get()
        new_description = self.desc_text.get("1.0", "end-1c")
        new_file_name = self.file_name_entry.get()

        if not self.current_file_path:
            messagebox.showwarning("Warning", "No file selected.")
            return
        
        title = self.title_var.get()
        description = self.desc_text.get("1.0", "end-1c").rstrip()  # Remove trailing newline

        # Validate length criteria
        if not (1 <= len(title) <= 32):
            messagebox.showerror("Error", "Title must be between 1 and 32 characters.")
            return
        if not (1 <= len(description) <= 127):
            messagebox.showerror("Error", "Description must be between 1 and 127 characters.")
            return

        dir_path = os.path.dirname(self.current_file_path)
        original_file_name = os.path.basename(self.current_file_path)
        new_file_path = os.path.join(dir_path, new_file_name)

        # Check if the new file name is different and if the new file already exists
        if new_file_name != original_file_name and os.path.exists(new_file_path):
            response = messagebox.askyesno("Confirm Overwrite", "The file already exists. Do you want to overwrite it?")
            if not response:
                return  # User chose not to overwrite the existing file

        # If the file name has been changed, update the current file path
        if new_file_name != original_file_name:
            try:
                os.rename(self.current_file_path, new_file_path)
                self.current_file_path = new_file_path  # Update the current file path to the new path
            except OSError as e:
                messagebox.showerror("Error", f"Failed to rename the file: {e}")
                return

        # Proceed with saving changes to the file content (title, description, etc.)
        try:
            # These functions should open the file, make the necessary modifications, and save the changes.
            # Read the entire file into memory (ensure the file is not too large for this operation)
            with open(self.current_file_path, 'rb') as file:
                file_data = file.read()

            # Use the new function to extract title and description
            title, description = read_string_at_offset(file_data)

            if new_title:  # Check if there's a new title to update
                replace_and_save_binary(self.current_file_path, title, new_title)
            if new_description:  # Check if there's a new description to update
                replace_and_save_binary(self.current_file_path, description, new_description)
            
            messagebox.showinfo("Success", "Changes saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {e}")

def read_string_at_offset(data):
    major = int.from_bytes(data[0x3C:0x3E], 'big')
    minor = int.from_bytes(data[0x3E:0x40], 'big')
    if major == 0xFFFF or (major == 0 and minor == 0xFFFF):
        encoding = 'utf-16-le'
        title = data[0x0C0:0x1C0].decode(encoding).split('\0', maxsplit=1)[0]
        desc = data[0x1C0:0x2C0].decode(encoding).split('\0', maxsplit=1)[0]
        return title, desc

    if data[0x0C0] == 0:
        title = data[0x0C0:0x1C0].decode('utf-16-be').split('\0', maxsplit=1)[0]
    else:
        title = data[0x0C0:0x1C0].decode('utf-16-le').split('\0', maxsplit=1)[0]

    if data[0x1C0] == 0:
        desc = data[0x1C0:0x2C0].decode('utf-16-be').split('\0', maxsplit=1)[0]
    else:
        desc = data[0x1C0:0x2C0].decode('utf-16-le').split('\0', maxsplit=1)[0]

    return title, desc

def string_to_binary_utf16le(input_string):
    """Converts a string to its binary representation in UTF-16LE format without spaces."""
    utf16le_bytes = input_string.encode('utf-16le')  # Encode the string in UTF-16LE
    # Convert each byte to an 8-bit binary string and concatenate them directly
    binary_string = ''.join(f'{byte:08b}' for byte in utf16le_bytes)
    return binary_string

def replace_first_occurrence(binary_content, original_binary, replacement_binary, preserve_after_second_occurrence=True):
    """Replaces the first occurrence of original_binary with replacement_binary in binary_content."""
    first_index = binary_content.find(original_binary)

    if first_index != -1:
        # Replace the original binary with the replacement binary in the binary content
        #Calculate the difference in length between the original and replacement binary
        difference = len(original_binary) - len(replacement_binary)
        temp = replacement_binary
        if difference > 0:
            temp += "0" * difference
        binary_3 = binary_content[first_index + len(temp):]
        binary_1 = binary_content[:first_index] + temp
        binary_content = binary_1 + binary_3
        #Remove 8 zeroes from replacement binary
        # If specified, preserve bytes after the second occurrence
        if preserve_after_second_occurrence:
            # Find the index of the original binary after the first occurrence
            second_index = binary_content.find(original_binary, first_index + len(replacement_binary))
            if second_index != -1:
                # Preserve bytes after the second occurrence
                leng = len(original_binary)
                preserved_bytes = binary_content[second_index + leng:]
                untilSecond = binary_content[:second_index]
                binary_content = untilSecond + replacement_binary + preserved_bytes
            
            third_index = binary_content.find(original_binary, second_index + len(replacement_binary))
            if third_index != -1:
                # Preserve bytes after the third occurrence
                leng = len(original_binary)
                preserved_bytes = binary_content[third_index + leng:]
                untilThird = binary_content[:third_index]
                binary_content = untilThird + replacement_binary + preserved_bytes

    return binary_content

def replace_and_save_binary(file_path, original_string, replacement_string):
    """Replaces the first occurrence of original_string with replacement_string in the binary file."""
    with open(file_path, 'rb') as binary_file:
        binary_content = ''.join(format(byte, '08b') for byte in binary_file.read())

    # Use the updated conversion function
    original_binary = string_to_binary_utf16le(original_string).replace(' ', '')
    replacement_binary = string_to_binary_utf16le(replacement_string).replace(' ', '')

    binary_content = replace_first_occurrence(binary_content, original_binary, replacement_binary, True)

    with open(file_path, 'wb') as modified_file:
        byte_array = bytearray(int(binary_content[i:i+8], 2) for i in range(0, len(binary_content), 8))
        modified_file.write(byte_array)

if __name__ == "__main__":
    app = MainApplication()
    excluded_files = ['00_basic_editing_054.bin', '2nvasion_slayer_054.bin', '2nvasion_slayer_light_054.bin', '3nvasion_054.bin', '3nvasion_boneyard_054.bin', '3nvasion_dlc_054.bin', '3nvasion_spire_054.bin', 'affinity_default_031.mvar', 'aftship_default_031.mvar', 'aftship_parasitic_031.mvar', 'anchor9_deepscream9_031.mvar', 'anchor9_default_031.mvar', 'anchor9_unanchored_swat_031.mvar', 'arena_slayer_team_054.bin', 'assault_054.bin', 'assault_big_default_054.bin', 'assault_big_neutral_bomb_054.bin', 'assault_big_one_bomb_054.bin', 'assault_default_054.bin', 'assault_default_anniversary_054.bin', 'assault_neutral_bomb_054.bin', 'assault_neutral_bomb_classic_054.bin', 'assault_neutral_bomb_dmr_054.bin', 'assault_neutral_bomb_shotgun_054.bin', 'assault_one_bomb_054.bin', 'assault_one_bomb_anniversary_054.bin', 'assault_one_bomb_dmr_054.bin', 'atom.mvar', 'atom_default_031.mvar', 'battle_canyon_2v2_031.mvar', 'beaver_creek_cl_031.mvar', 'beaver_creek_default_031.mvar', 'boneyard_default_031.mvar', 'boneyard_graveyard_031.mvar', 'breakpoint_breakout_031.mvar', 'breakpoint_default_031.mvar', 'campaign_default_054.bin', 'cliffhanger.mvar', 'cliffhanger_default_031.mvar', 'coastline_asylum_2v2_031.mvar', 'coastline_asylum_default_031.mvar', 'coastline_azimuth_default_031.mvar', 'coastline_cage_default_031.mvar', 'coastline_hemorrhage_default_031.mvar', 'coastline_hemorrhage_rhr_031.mvar', 'coastline_paradiso_default_031.mvar', 'coastline_uncaged_2v2_031.mvar', 'coastline_uncaged_default_031.mvar', 'coastline_uncongealed_031.mvar', 'condemned_default_031.mvar', 'condemned_downlinked_031.mvar', 'condemned_uplink_031.mvar', 'countdown_swat_031.mvar', 'ctf_054.bin', 'ctf_1flag_054.bin', 'ctf_1flag_anniversary_054.bin', 'ctf_1flag_dmr_054.bin', 'ctf_1flag_pro_054.bin', 'ctf_3flag_dmr_054.bin', 'ctf_big_1flag_054.bin', 'ctf_big_multiflag_054.bin', 'ctf_multiflag_anniversary_054.bin', 'ctf_multiflag_classic_054.bin', 'ctf_multiflag_dmr_054.bin', 'ctf_multiflag_pro_054.bin', 'ctf_multiflag_teamclassic_054.bin', 'ctf_multiteam_054.bin', 'ctf_neutralflag_054.bin', 'ctf_neutral_flag_dmr_054.bin', 'ctf_neutral_flag_rockets_054.bin', 'ctf_slayer_2flag_054.bin', 'damnation_cl_031.mvar', 'damnation_default_031.mvar', 'damnation_purgatory_031.mvar', 'enclosed_2v2_031.mvar', 'enclosed_default_031.mvar', 'ff_2x_score_attack_054.bin', 'ff_arcade_arcadefight_054.bin', 'ff_arcade_fiestafight_054.bin', 'ff_arcade_fistfight_054.bin', 'ff_arcade_frgfight_054.bin', 'ff_arcade_frgfight_nohaz_054.bin', 'ff_arcade_geb_054.bin', 'ff_arcade_nadefight_054.bin', 'ff_arcade_plasmafight_054.bin', 'ff_arcade_rocketfight_054.bin', 'ff_arcade_sniperfight_054.bin', 'ff_crash_site_054.bin', 'ff_fiesta_attack_054.bin', 'ff_firefight_054.bin', 'ff_frg_attack_054.bin', 'ff_generator_defense_054.bin', 'ff_gruntpocalypse_054.bin', 'ff_ltd_crashsite_054.bin', 'ff_ltd_firefight_054.bin', 'ff_ltd_geb_054.bin', 'ff_ltd_gennyd_054.bin', 'ff_ltd_legendary_054.bin', 'ff_mythic_score_attack_054.bin', 'ff_rocketfight_054.bin', 'ff_rocket_attack_054.bin', 'ff_score_attack_054.bin', 'ff_skirmiggedon_054.bin', 'ff_sniper_attack_054.bin', 'forgeworld_abridged_031.mvar', 'forgeworld_asphalt_031.mvar', 'forgeworld_asylum_swat_031.mvar', 'forgeworld_bedlam_031.mvar', 'forgeworld_broadcast_031.mvar', 'forgeworld_chateau_default_031.mvar', 'forgeworld_delta_facility_031.mvar', 'forgeworld_dreadnought_031.mvar', 'forgeworld_eclipse_031.mvar', 'forgeworld_eden_minor_default_031.mvar', 'forgeworld_ellul_031.mvar', 'forgeworld_floodgate_031.mvar', 'forgeworld_grif_alembic_gold_031.mvar', 'forgeworld_grif_belle_court_031.mvar', 'forgeworld_grif_bloody_grifball_031.mvar', 'forgeworld_grif_brightside_031.mvar', 'forgeworld_grif_cliffside_031.mvar', 'forgeworld_grif_clover_x_031.mvar', 'forgeworld_grif_concave_arena_031.mvar', 'forgeworld_grif_erora_031.mvar', 'forgeworld_grif_fore_pyra_031.mvar', 'forgeworld_grif_gb_foundry_031.mvar', 'forgeworld_grif_get_off_my_lawn_031.mvar', 'forgeworld_grif_hbgp_031.mvar', 'forgeworld_grif_heimdalls_might_031.mvar', 'forgeworld_grif_high_tide_031.mvar', 'forgeworld_grif_hyperbaric_031.mvar', 'forgeworld_grif_illuminati_031.mvar', 'forgeworld_grif_impact_arena_031.mvar', 'forgeworld_grif_indo_cach_031.mvar', 'forgeworld_grif_inspiration_031.mvar', 'forgeworld_grif_malice_n_envy_031.mvar', 'forgeworld_grif_methodical_031.mvar', 'forgeworld_grif_m_project_031.mvar', 'forgeworld_grif_omega_temple_031.mvar', 'forgeworld_grif_oracles_revenge_031.mvar', 'forgeworld_grif_pinwheel_031.mvar', 'forgeworld_grif_radiant_031.mvar', 'forgeworld_grif_red_ray_court_031.mvar', 'forgeworld_grif_separate_ways_031.mvar', 'forgeworld_grif_sierra_vista_031.mvar', 'forgeworld_grif_teg_031.mvar', 'forgeworld_grif_temple_prime_031.mvar', 'forgeworld_grif_the_vault_031.mvar', 'forgeworld_grif_the_view_031.mvar', 'forgeworld_high_noon_031.mvar', 'forgeworld_hydra_xxiii_031.mvar', 'forgeworld_imago_031.mvar', 'forgeworld_magus_031.mvar', 'forgeworld_midas_031.mvar', 'forgeworld_mt_lam_lam_031.mvar', 'forgeworld_noble_creek_031.mvar', 'forgeworld_overgrowth_031.mvar', 'forgeworld_paradise_031.mvar', 'forgeworld_precipice_031.mvar', 'forgeworld_prolonged_031.mvar', 'forgeworld_prophet_031.mvar', 'forgeworld_pulse_031.mvar', 'forgeworld_rasu_031.mvar', 'forgeworld_rat_trap_031.mvar', 'forgeworld_refinery_031.mvar', 'forgeworld_renegade_031.mvar', 'forgeworld_renova_default_031.mvar', 'forgeworld_select_031.mvar', 'forgeworld_select_2v2_031.mvar', 'forgeworld_think_twice_031.mvar', 'forgeworld_trident_031.mvar', 'forgeworld_unconquered_031.mvar', 'forgeworld_wayont_031.mvar', 'forge_halo_asylum.mvar', 'forge_halo_hemorrhage.mvar', 'forge_halo_paradiso.mvar', 'forge_halo_pinnacle.mvar', 'grifball_blargball_054.bin', 'grifball_dash_054.bin', 'grifball_evolved_054.bin', 'grifball_hand_egg_054.bin', 'grifball_jetpack_054.bin', 'grifball_jump_pack_054.bin', 'grifball_vanilla_054.bin', 'grifball_zealot_blargball_054.bin', 'grif_federation_square_031.mvar', 'hangemhigh_default_031.mvar', 'hang_em_high_cl_031.mvar', 'headhunter_054.bin', 'headhunter_big_team_054.bin', 'headhunter_default_054.bin', 'headhunter_pro_054.bin', 'headhunter_team_054.bin', 'headlong_cl_031.mvar', 'headlong_default_031.mvar', 'headlong_headstrong_031.mvar', 'headlong_rigamortis_031.mvar', 'highlands_default_031.mvar', 'highlands_eminence_031.mvar', 'hockey_rink_default_031.mvar', 'hogpotato_team_054.bin', 'hr_1v1_team_slayer_15points_zbns.bin', 'hr_1v1_team_slayer_1point_zbns.bin', 'hr_2v2_team_hardcoreSlayer_25points_zbns.bin', 'hr_2v2_team_multiFlag_dmr_ar_3points_tu.bin', 'hr_2v2_team_oddball_dmr_ar_150points_tu.bin', 'hr_2v2_team_sequentialKing_dmr_ar_150points_tu.bin', 'hr_2v2_team_slayer_ar_mag_25points_tu.bin', 'hr_2v2_team_slayer_dmr_ar_25points_tu.bin', 'hr_2v2_team_snipers_25points_tu.bin', 'hr_4v4_team_3plots_dmr_ar_300points_tu.bin', 'hr_4v4_team_3plots_dmr_ar_500points_tu.bin', 'hr_4v4_team_assault_dmr_ar_3points_tu.bin', 'hr_4v4_team_boomBall_gl_150points_tu.bin', 'hr_4v4_team_broSlayer_ar_mag_50points_tu.bin', 'hr_4v4_team_crazyKing_dmr_ar_150points_tu.bin', 'hr_4v4_team_dinoBlasters_25points_tu.bin', 'hr_4v4_team_dinoBlasters_50points_tu.bin', 'hr_4v4_team_escalationSlayer_covy_3rounds_tu.bin', 'hr_4v4_team_escalationSlayer_mixed_tu.bin', 'hr_4v4_team_fiesta_50points_tu.bin', 'hr_4v4_team_flagSlayer_dmr_ar_150points_tu.bin', 'hr_4v4_team_flagSlayer_dmr_ar_200points_tu.bin', 'hr_4v4_team_freezeFlag_5rounds_tu.bin', 'hr_4v4_team_freezeTag_5rounds_tu.bin', 'hr_4v4_team_hardcoreBomb_3points_zbns.bin', 'hr_4v4_team_hardcoreBomb_5points_zbns.bin', 'hr_4v4_team_hardcoreCtf_3sanc_zbns.bin', 'hr_4v4_team_hardcoreCtf_5pit_zbns.bin', 'hr_4v4_team_hardcoreCtf_5points_zbns.bin', 'hr_4v4_team_hardcoreKing_250points_zbns.bin', 'hr_4v4_team_hardcoreSlayer_50points_zbns.bin', 'hr_4v4_team_headhunter_dmr_ar_50points_tu.bin', 'hr_4v4_team_hotPotato_ar_mag_150points_tu.bin', 'hr_4v4_team_multiFlag_dmr_ar_3points_tu.bin', 'hr_4v4_team_neutralBomb_dmr_ar_3points_tu.bin', 'hr_4v4_team_oddball_dmr_ar_150points_tu.bin', 'hr_4v4_team_oneBomb_dmr_ar_3points_tu.bin', 'hr_4v4_team_oneFlag_dmr_ar_4rounds_tu.bin', 'hr_4v4_team_powerSlayer_50points_tu.bin', 'hr_4v4_team_sequentialKing_dmr_ar_150points_tu.bin', 'hr_4v4_team_shottySnipers_50points_tu.bin', 'hr_4v4_team_slayer_ar_mag_50points_tu.bin', 'hr_4v4_team_slayer_covy_50points_tu.bin', 'hr_4v4_team_slayer_dmr_ar_50points_tu.bin', 'hr_4v4_team_snipers_50points_tu.bin', 'hr_4v4_team_speedFlag_shotguns_5points_tu.bin', 'hr_4v4_team_speedFlag_shotguns_flagAtHome_tu.bin', 'hr_4v4_team_stockpile_dmr_ar_10points_tu.bin', 'hr_4v4_team_swat_dmr_mag_50points_tu.bin', 'hr_4v4_team_swat_mag_50points_tu.bin', 'hr_4v4_team_territories_dmr_ar_4rounds_3min_tu.bin', 'hr_4v4_team_tuSlayerFast_dmr_25kills_5min.bin', 'hr_6v6_team_invasion_eliteoffense_boneyard_v2.bin', 'hr_6v6_team_invasion_eliteoffense_breakpoint_v2.bin', 'hr_6v6_team_invasion_eliteoffense_terrbombcore.bin', 'hr_6v6_team_invasion_eliteoffense_terrgencore.bin', 'hr_6v6_team_invasion_eliteoffense_terrterrcore.bin', 'hr_6v6_team_invasion_spartanoffense_gengencore.bin', 'hr_6v6_team_invasion_spartanoffense_spire_v2.bin', 'hr_6v6_team_invasion_spartanoffense_terrbombcore.bin', 'hr_6v6_team_invasion_spartanoffense_terrgencore.bin', 'hr_6v6_team_invasion_spartanoffense_terrterrcore.bin', 'hr_8v8_team_3plots_ar_mag_500points_tu.bin', 'hr_8v8_team_3plots_dmr_ar_500points_tu.bin', 'hr_8v8_team_assault_ar_mag_3points_tu.bin', 'hr_8v8_team_assault_dmr_ar_3points_tu.bin', 'hr_8v8_team_broSlayer_ar_mag_100points_tu.bin', 'hr_8v8_team_broSlayer_dmr_ar_100points_tu.bin', 'hr_8v8_team_crazyKing_ar_mag_200points_tu.bin', 'hr_8v8_team_crazyKing_dmr_ar_200points_tu.bin', 'hr_8v8_team_headhunter_ar_mag_75points_tu.bin', 'hr_8v8_team_headhunter_dmr_ar_75points_tu.bin', 'hr_8v8_team_heavies_dmr_ar_150points_tu.bin', 'hr_8v8_team_miniGame_inYourBase.bin', 'hr_8v8_team_miniGame_reachShamBo_3rounds_6min.bin', 'hr_8v8_team_miniGame_yumYum.bin', 'hr_8v8_team_multiFlag_ar_mag_3points_tu.bin', 'hr_8v8_team_multiFlag_dmr_ar_3points_tu.bin', 'hr_8v8_team_neutralBomb_ar_mag_3points_tu.bin', 'hr_8v8_team_neutralBomb_dmr_ar_3points_tu.bin', 'hr_8v8_team_oneBomb_ar_mag_3points_tu.bin', 'hr_8v8_team_oneBomb_dmr_ar_3points_tu.bin', 'hr_8v8_team_oneFlag_ar_mag_4rounds_tu.bin', 'hr_8v8_team_oneFlag_dmr_ar_4rounds_tu.bin', 'hr_8v8_team_slayer_ar_mag_100points_tu.bin', 'hr_8v8_team_slayer_covy_100points_tu.bin', 'hr_8v8_team_slayer_dmr_ar_100points_tu.bin', 'hr_8v8_team_snipers_100points_tu.bin', 'hr_8v8_team_stockpile_ar_mag_10points_tu.bin', 'hr_8v8_team_stockpile_dmr_ar_10points_tu.bin', 'hr_8v8_team_territories_ar_mag_2rounds_6min_tu.bin', 'hr_8v8_team_territories_ar_mag_2rounds_7min_tu.bin', 'hr_8v8_team_territories_dmr_ar_2rounds_6min_tu.bin', 'hr_8v8_team_territories_dmr_ar_2rounds_7min_tu.bin', 'hr_anchor9_unanchored_v6.mvar', 'hr_battleCanyon_mlg_v7.mvar', 'hr_boneyard_inv_default_v2.mvar', 'hr_boneyard_scrapyard_btb.mvar', 'hr_breakneck_inf_rigamortis_v2.mvar', 'hr_breakneck_inv_newmombassa.mvar', 'hr_breakpoint_inv_default_v2.mvar', 'hr_countdown_inf_countdhouhen_v2.mvar', 'hr_countdown_mlg_v7.mvar', 'hr_countdown_mlg_v8.mvar', 'hr_countdown_mlg_v8_2v2.mvar', 'hr_ffa_alphaZombies_vanilla.bin', 'hr_ffa_boomBall_gl_75points_tu.bin', 'hr_ffa_crazyKing_ar_mag_75points_tu.bin', 'hr_ffa_crazyKing_dmr_ar_75points_tu.bin', 'hr_ffa_dinoBlasters_15points_tu.bin', 'hr_ffa_escalationSlayer_covy_3rounds_tu.bin', 'hr_ffa_escalationSlayer_mixed_tu.bin', 'hr_ffa_escalationSlayer_mixed_vanilla.bin', 'hr_ffa_fiesta_25points_tu.bin', 'hr_ffa_headhunter_ar_mag_25points_tu.bin', 'hr_ffa_headhunter_dmr_ar_25points_tu.bin', 'hr_ffa_hotPotato_ar_mag_75points_tu.bin', 'hr_ffa_infection_vanilla.bin', 'hr_ffa_juggernaut_ar_mag_150points_tu.bin', 'hr_ffa_juggernaut_dmr_ar_150points_tu.bin', 'hr_ffa_miniGame_jumpRope.bin', 'hr_ffa_miniGame_rentACar.bin', 'hr_ffa_miniGame_run.bin', 'hr_ffa_miniGame_speed.bin', 'hr_ffa_oddball_ar_mag_75points_tu.bin', 'hr_ffa_oddball_dmr_ar_75points_tu.bin', 'hr_ffa_powerSlayer_25points_tu.bin', 'hr_ffa_powerSlayer_50points_tu.bin', 'hr_ffa_shottySnipers_25points_tu.bin', 'hr_ffa_shottySnipers_sniper_shotgun_25points.bin', 'hr_ffa_slayer_ar_mag_25points_tu.bin', 'hr_ffa_slayer_covy_25points_tu.bin', 'hr_ffa_slayer_dmr_ar_25points_tu.bin', 'hr_ffa_snipers_25points_tu.bin', 'hr_ffa_swat_dmr_mag_25points_tu.bin', 'hr_ffa_swat_mag_25points_tu.bin', 'hr_ff_arcadefight_1set.bin', 'hr_ff_classic_1set.bin', 'hr_ff_crashSite_1round.bin', 'hr_ff_fiestafight_1set.bin', 'hr_ff_fistfight_1set.bin', 'hr_ff_frgFight_1set.bin', 'hr_ff_frgFight_noHazards_1set.bin', 'hr_ff_generatorDefense_1set.bin', 'hr_ff_generatorDefense_1set_limited.bin', 'hr_ff_gruntpocalypse_1round.bin', 'hr_ff_limited_1set.bin', 'hr_ff_nadefight_1set.bin', 'hr_ff_plasmafight_1set.bin', 'hr_ff_rocketfight_1set.bin', 'hr_ff_scoreAttack_1round.bin', 'hr_ff_skirmigeddon_1round.bin', 'hr_ff_sniperfight_1set.bin', 'hr_ff_standard_1set.bin', 'hr_ff_stressTest_1set.bin', 'hr_ff_versus_2turns.bin', 'hr_forgeWorld_asylum.mvar', 'hr_forgeWorld_btb_brick.mvar', 'hr_forgeWorld_btb_hivemind.mvar', 'hr_forgeWorld_btb_metropolis.mvar', 'hr_forgeWorld_btb_portAuthority.mvar', 'hr_forgeWorld_btb_s.mvar', 'hr_forgeWorld_btb_spectre.mvar', 'hr_forgeWorld_btb_warhorse.mvar', 'hr_forgeWorld_hemorrhage.mvar', 'hr_forgeWorld_inv_broadcast_v2.mvar', 'hr_forgeworld_inv_broadcast_v3.mvar', 'hr_forgeworld_inv_calamity.mvar', 'hr_forgeworld_inv_cenotaph.mvar', 'hr_forgeworld_inv_descent.mvar', 'hr_forgeworld_inv_districtone.mvar', 'hr_forgeworld_inv_firewall.mvar', 'hr_forgeWorld_inv_floodgate_v2.mvar', 'hr_forgeworld_inv_floodgate_v3.mvar', 'hr_forgeworld_inv_goodhunting.mvar', 'hr_forgeworld_inv_keystone.mvar', 'hr_forgeworld_inv_legacy.mvar', 'hr_forgeWorld_inv_overgrowth_v2.mvar', 'hr_forgeworld_inv_overgrowth_v3.mvar', 'hr_forgeworld_inv_palace.mvar', 'hr_forgeWorld_inv_refinery_v2.mvar', 'hr_forgeworld_inv_refinery_v3.mvar', 'hr_forgeworld_inv_sentinelfactory.mvar', 'hr_forgeworld_inv_sovereign.mvar', 'hr_forgeworld_inv_stanchion.mvar', 'hr_forgeworld_inv_summit.mvar', 'hr_forgeworld_inv_sunspot.mvar', 'hr_forgeworld_inv_surfnturf.mvar', 'hr_forgeworld_inv_thebrink.mvar', 'hr_forgeworld_inv_thetower.mvar', 'hr_forgeworld_inv_thewatcher.mvar', 'hr_forgeworld_inv_thunderfall.mvar', 'hr_forgeworld_inv_vessel.mvar', 'hr_forgeWorld_miniGame_bridgelandValley.mvar', 'hr_forgeWorld_miniGame_crashUpDerby.mvar', 'hr_forgeWorld_miniGame_jumpRope.mvar', 'hr_forgeWorld_miniGame_nomNom.mvar', 'hr_forgeWorld_miniGame_reachShamBo.mvar', 'hr_forgeWorld_miniGame_run.mvar', 'hr_forgeWorld_miniGame_speed.mvar', 'hr_forgeWorld_miniGame_stealinYourFlags.mvar', 'hr_forgeWorld_nexus_mlg_v7.mvar', 'hr_forgeWorld_onslaught_mlg.mvar', 'hr_forgeWorld_paradiso.mvar', 'hr_forgeWorld_pinnacle.mvar', 'hr_forgeWorld_pit_mlg_v7.mvar', 'hr_forgeWorld_sanc_mlg_v7.mvar', 'hr_forgeWorld_simplex_mlg.mvar', 'hr_forgeWorld_splash_mlg.mvar', 'hr_forgeWorld_theCage.mvar', 'hr_penance_inf_purgatory_v2.mvar', 'hr_penance_mlg_v7.mvar', 'hr_powerhouse_v6.mvar', 'hr_ridgeline_inv_archean.mvar', 'hr_spire_inv_default_v2.mvar', 'hr_spire_spearBroken_btb.mvar', 'hr_tempest_btb_v2.mvar', 'hr_tempest_inv_bastion.mvar', 'hr_tempest_pit_mlg_v8.mvar', 'hr_zealot_inf_parasitic_v2.mvar', 'hr_zealot_mlg_v7.mvar', 'hr_zealot_mlg_v8.mvar', 'hr_zealot_mlg_v8_2v2.mvar', 'infection_054.bin', 'infection_ffa_054.bin', 'infection_ffa_alpha_zombies_054.bin', 'infection_ffa_zombie_ghosts_054.bin', 'infection_safehavens_054.bin', 'invasion_054.bin', 'invasion_boneyard_054.bin', 'invasion_breakpoint_054.bin', 'invasion_skirmish_default_054.bin', 'invasion_skirmish_elite_054.bin', 'invasion_skirmish_spartan_054.bin', 'invasion_slayer_default_054.bin', 'invasion_slayer_light_default_054.bin', 'invasion_spire_054.bin', 'ivory_tower_2v2_031.mvar', 'ivory_tower_default_031.mvar', 'ivory_tower_pandemic_031.mvar', 'juggernaut_054.bin', 'juggernaut_default_054.bin', 'kingdom_default_031.mvar', 'koth_054.bin', 'koth_big_team_crazyking_054.bin', 'koth_crazyking_054.bin', 'koth_ffa_crazyking_054.bin', 'koth_team_crazyking_anniversary_054.bin', 'koth_team_crazyking_dmr_054.bin', 'koth_team_crazyking_teamclassic_054.bin', 'koth_team_king_2v2_054.bin', 'koth_team_multi_crazyking_054.bin', 'launch_countdhouen_031.mvar', 'launch_station_2v2_031.mvar', 'launch_station_default_031.mvar', 'mlg_5_ctf_zbns_054.bin', 'mlg_5_ctf_zbs_054.bin', 'mlg_android_v4_031.mvar', 'mlg_android_v6_031.mvar', 'mlg_assault_neutral_3_054.bin', 'mlg_assault_sanc_054.bin', 'mlg_ball_6_054.bin', 'mlg_battle_canyon_v7_031.mvar', 'mlg_bomb_count_6_054.bin', 'mlg_bomb_sanc_6_054.bin', 'mlg_bomb_zeal_6_054.bin', 'mlg_countdown_v4_031.mvar', 'mlg_countdown_v6_031.mvar', 'mlg_countdown_v7_031.mvar', 'mlg_ctf_5flag_6_054.bin', 'mlg_ctf_5flag_7_054.bin', 'mlg_ctf_multiflag_3_054.bin', 'mlg_ctf_multiflag_5_054.bin', 'mlg_ctf_pit_6_054.bin', 'mlg_ctf_pit_7_054.bin', 'mlg_ctf_sanc_6_054.bin', 'mlg_ctf_sanc_7_054.bin', 'mlg_elementx_v6_031.mvar', 'mlg_element_v4_031.mvar', 'mlg_king_team_054.bin', 'mlg_koth_6_054.bin', 'mlg_koth_7_054.bin', 'mlg_koth_zbns_054.bin', 'mlg_koth_zbs_054.bin', 'mlg_nexus_v4_031.mvar', 'mlg_nexus_v6_031.mvar', 'mlg_nexus_v7_031.mvar', 'mlg_oasis_v6_031.mvar', 'mlg_penance_v7_031.mvar', 'mlg_pit_ctf_zbns_054.bin', 'mlg_pit_ctf_zbs_054.bin', 'mlg_redemption_v4_031.mvar', 'mlg_redemption_v6_031.mvar', 'mlg_retroactive_v4_031.mvar', 'mlg_sanctuary_v4_031.mvar', 'mlg_sanctuary_v6_031.mvar', 'mlg_sanctuary_v7_031.mvar', 'mlg_sanc_ctf_zbns_054.bin', 'mlg_sanc_ctf_zbs_054.bin', 'mlg_slayer_team_054.bin', 'mlg_slayer_team_6_054.bin', 'mlg_slayer_team_7_054.bin', 'mlg_territories_054.bin', 'mlg_territories_6_054.bin', 'mlg_the_pit_v6_031.mvar', 'mlg_the_pit_v7_031.mvar', 'mlg_ts_zbns_054.bin', 'mlg_ts_zbs_054.bin', 'mlg_veridian_v4_031.mvar', 'mlg_warlock_v4.3_031.mvar', 'mlg_zealot_ball_v6_031.mvar', 'mlg_zealot_v4_031.mvar', 'mlg_zealot_v6_031.mvar', 'mlg_zealot_v7_031.mvar', 'oddball_054.bin', 'oddball_ffa_054.bin', 'oddball_hotpotato_boom_ball_054.bin', 'oddball_hotpotato_team_054.bin', 'oddball_hotpotato_team_dmr_054.bin', 'oddball_team_2v2_054.bin', 'oddball_team_3ball_054.bin', 'oddball_team_anniversary_054.bin', 'oddball_team_dmr_054.bin', 'oddball_team_teamclassic_054.bin', 'panoptical_deadwalk_031.mvar', 'panoptical_default_031.mvar', 'powerhouse_swat_031.mvar', 'prisoner_cl_031.mvar', 'prisoner_default_031.mvar', 'prisoner_quarantine_031.mvar', 'race_054.bin', 'rally_054.bin', 'reflection_swat_031.mvar', 'rocket_race_hog_054.bin', 'settlement_2v2_031.mvar', 'settlement_default_031.mvar', 'settlement_powerless_031.mvar', 'skeeball_court_031.mvar', 'skeeball_court_xtreme_031.mvar', 'skeeball_default_054.bin', 'skeeball_hockey_054.bin', 'skeeball_pvp_054.bin', 'slayer_054.bin', 'slayer_big_team_054.bin', 'slayer_big_team_anniversary_054.bin', 'slayer_big_team_covy_054.bin', 'slayer_big_team_snipers_054.bin', 'slayer_classic_054.bin', 'slayer_covy_054.bin', 'slayer_ffa_054.bin', 'slayer_ffa_covy_054.bin', 'slayer_ffa_dmr_054.bin', 'slayer_ffa_pro_054.bin', 'slayer_medium_team_054.bin', 'slayer_medium_team_covy_054.bin', 'slayer_medium_team_dmr_054.bin', 'slayer_medium_team_pro_054.bin', 'slayer_medium_team_sniper_054.bin', 'slayer_power_team_054.bin', 'slayer_pro_054.bin', 'slayer_team_054.bin', 'slayer_team_2v2_054.bin', 'slayer_team_bro_054.bin', 'slayer_team_classic_054.bin', 'slayer_team_classic_4sk_054.bin', 'slayer_team_classic_rifles_054.bin', 'slayer_team_covy_054.bin', 'slayer_team_dino_blasters_054.bin', 'slayer_team_dmr_054.bin', 'slayer_team_dmr_2v2_054.bin', 'slayer_team_hotshot_054.bin', 'slayer_team_pro_054.bin', 'slayer_team_shotty_snipers_054.bin', 'slayer_team_sniper_054.bin', 'slayer_team_sniper_anniversary_054.bin', 'slayer_team_sniper_pro_054.bin', 'slayer_team_splockets_054.bin', 'slayer_team_squad_054.bin', 'slayer_team_squad_dmr_054.bin', 'slayer_team_swat_054.bin', 'solitary_2v2_031.mvar', 'speedflag_multiflag_054.bin', 'speedflag_multiflag_dmr_054.bin', 'speedpile_054.bin', 'spire.mvar', 'spire_cragmire_031.mvar', 'spire_default_031.mvar', 'stockpile_054.bin', 'stockpile_big_054.bin', 'stockpile_default_054.bin', 'SWAT_054.bin', 'sword_base_default_031.mvar', 'sword_base_spooky_base_031.mvar', 'synapse_2v2_031.mvar', 'synapse_default_031.mvar', 'team_swat_magnum_054.bin', 'team_swat_oddball_054.bin', 'team_swat_stockpile_054.bin', 'team_swat_territories_3plots_054.bin', 'tempest_default_031.mvar', 'tempest_temple_031.mvar', 'tempest_typhoon_031.mvar', 'temptation_031.mvar', 'territories-3plot_054.bin', 'territories-landgrab_054.bin', 'territories_054.bin', 'territories_big_054.bin', 'territories_default_054.bin', 'territories_team_3plots_dmr_054.bin', 'the_cage.mvar', 'timberland_cl_031.mvar', 'timberland_default_031.mvar', 'timberland_superstition_031.mvar', 'treasury_2v2_031.mvar', 'treasury_default_031.mvar', 'tu1_arena_slayer_team_054.bin', 'tu1_assault_big_default_054.bin', 'tu1_assault_big_neutral_bomb_054.bin', 'tu1_assault_big_one_bomb_054.bin', 'tu1_assault_default_054.bin', 'tu1_assault_neutral_bomb_dmr_054.bin', 'tu1_assault_one_bomb_dmr_054.bin', 'tu1_ctf_1flag_dmr_054.bin', 'tu1_ctf_1flag_pro_054.bin', 'tu1_ctf_3flag_dmr_054.bin', 'tu1_ctf_big_1flag_054.bin', 'tu1_ctf_big_multiflag_054.bin', 'tu1_ctf_multiflag_classic_054.bin', 'tu1_ctf_multiflag_dmr_054.bin', 'tu1_ctf_multiflag_pro_054.bin', 'tu1_ctf_neutral_flag_dmr_054.bin', 'tu1_ctf_slayer_2flag_054.bin', 'tu1_headhunter_big_team_054.bin', 'tu1_headhunter_default_054.bin', 'tu1_headhunter_team_054.bin', 'tu1_infection_ffa_054.bin', 'tu1_infection_ffa_alpha_zombies_054.bin', 'tu1_juggernaut_054.bin', 'tu1_juggernaut_default_054.bin', 'tu1_koth_big_team_crazyking_054.bin', 'tu1_koth_ffa_crazyking_054.bin', 'tu1_koth_team_crazyking_dmr_054.bin', 'tu1_koth_team_default_054.bin', 'tu1_koth_team_king_2v2_054.bin', 'tu1_koth_team_multi_crazyking_054.bin', 'tu1_oddball_ffa_054.bin', 'tu1_oddball_hotpotato_team_054.bin', 'tu1_oddball_hotpotato_team_dmr_054.bin', 'tu1_oddball_team_2v2_054.bin', 'tu1_oddball_team_3ball_054.bin', 'tu1_oddball_team_dmr_054.bin', 'tu1_rocket_race_hog_054.bin', 'tu1_slayer_big_heavy_054.bin', 'tu1_slayer_big_team_054.bin', 'tu1_slayer_big_team_anniversary_054.bin', 'tu1_slayer_big_team_covy_054.bin', 'tu1_slayer_big_team_snipers_054.bin', 'tu1_slayer_ffa_054.bin', 'tu1_slayer_ffa_anniversary_054.bin', 'tu1_slayer_ffa_covy_054.bin', 'tu1_slayer_ffa_dmr_054.bin', 'tu1_slayer_ffa_pro_054.bin', 'tu1_slayer_mcc_054.bin', 'tu1_slayer_power_054.bin', 'tu1_slayer_team_054.bin', 'tu1_slayer_team_2v2_054.bin', 'tu1_slayer_team_anniversary_054.bin', 'tu1_slayer_team_covy_054.bin', 'tu1_slayer_team_dmr_054.bin', 'tu1_slayer_team_dmr_2v2_054.bin', 'tu1_slayer_team_pro_054.bin', 'tu1_slayer_team_squad_054.bin', 'tu1_slayer_team_squad_dmr_054.bin', 'tu1_speedflag_multiflag_dmr_054.bin', 'tu1_stockpile_big_054.bin', 'tu1_stockpile_default_054.bin', 'tu1_team_gun_game_054.bin', 'tu1_territories_big_054.bin', 'tu1_territories_default_054.bin', 'tu1_territories_team_3plots_dmr_054.bin', 'unanchored_2v2_031.mvar', 'unanchored_default_031.mvar', 'zb_slayer_team_dmr_054.bin', 'zealot_arena_031.mvar', 'zealot_arena_2v2_031.mvar', 'zealot_swat_031.mvar']
    app.mainloop()

    # pyinstaller --onefile --noconsole --icon="icon/reach_map_gametype_editor_icon.ico" ReachStringEditor.py