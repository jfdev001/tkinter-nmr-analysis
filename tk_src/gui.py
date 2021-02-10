"""GUI for processing nmr data, plotting it, and writing it to disk.

Subsections of a given window are separate classes.
New windows (tkinter.Toplevel objects) are separate classes.
"""

import tkinter as tk 
import tkinter.filedialog as fd
from PIL import ImageTk
import os
from pathlib import Path
from calculation_src.nmranalyzer import NmrAnalyzer


class SharedInfo:
    """Stores section and analysis information in one location."""
    def __init__(self, window):
        """Construct sections and initialize analysis_result."""
        # Construct MainWindow sections
        self.entry_section = EntrySection(window)
        self.analysis_section = AnalysisSection(window, self.entry_section)

        # Store analysis result for use in AnalysisWindow later
        self.analysis_result = None  # Tuple (MyImage, str outfile)


class MainWindow:
    """GUI for integration script."""
    def __init__(self, window=None):
        """Initialize window Frame and instantiate other Widgets."""
        # Constructor
        self.window = window
        self.info = SharedInfo(self.window)

        # Set geometry
        self.window.geometry("475x215")  # Initial dimensions of widget
        self.window.resizable(0, 0)  # No resize in x or y direction

        # Frame 
        self.frame = tk.Frame(self.window).grid()

        # Set icon
        self.this_folder = os.path.dirname(os.path.abspath(__file__))
        self.img_path = os.path.join(self.this_folder, "imgs/icon.png") 
        self.icon = ImageTk.PhotoImage(file=self.img_path)
        self.window.iconphoto(True, self.icon)

        # Set title
        self.window.title("NMR Inte-great!")

        # Grid Widgets to screen
        self.padding = {"padx": 2, "pady": 2, "ipady": 2, "ipadx": 2}
        self.grid_widgets()


    def grid_widgets(self):
        """Control the geometry of the Widgets for MainApp."""
        # Shorthand variables for each section
        self.ies = self.info.entry_section
        self.ias = self.info.analysis_section

        # LabelFrames
        self.ies.frame.grid(row=0, column=0)
        self.ias.frame.grid(row=1, column=0)

        #----Entry Section----
        # Upper limit of integration
        self.ies.upper_lim_label.grid(row=0, column=0, **self.padding,  
                                      sticky=tk.W+tk.E, in_=self.ies.frame)
        self.ies.upper_lim_entry.grid(row=0, column=1, columnspan=2,
                                      **self.padding, in_=self.ies.frame)                             

        # Lower limit of integration
        self.ies.lower_lim_label.grid(row=1, column=0, **self.padding, 
                                      sticky=tk.W+tk.E, in_=self.ies.frame) 
                                               
        self.ies.lower_lim_entry.grid(row=1, column=1, columnspan=2,
                                      **self.padding, in_=self.ies.frame)
        #----End Entry Section----

        #----Analysis Section----
        # File dialog button
        self.ias.file_button.grid(row=3, column=0, sticky=tk.W,
                                  ipady=5, ipadx=5, padx=5, pady=5, 
                                  in_=self.ias.frame)
        self.ias.file_label.grid(row=4, column=0, columnspan=2, 
                                 sticky=tk.W+tk.E, **self.padding, 
                                 in_=self.ias.frame)

        # Data analysis button
        self.ias.analysis_button.grid(row=3, column=1, sticky=tk.W,
                                      ipady=5, ipadx=5, padx=5, pady=5,
                                      in_=self.ias.frame)
        #----End Analysis Section----

        return None

class EntrySection:
    """Encapsulates Widgets for 'Entry Frame' LabelFrame.

    This class is bound to the MainApp window.
    """
    def __init__(self, window=None):
        """Define Widgets for this LabelFrame."""
        # window of MainApp is also window of this class
        self.window = window

        # LabelFrame
        self.frame = tk.LabelFrame(self.window, 
                                    text="Entry Frame",
                                    padx=5,
                                    pady=10)

        # Entry Widget styles
        self.style = {"relief": tk.SUNKEN, "width": 49}

        # Upper limit of integration
        self.upper_lim_label = tk.Label(self.window,
                                          text="Upper Limit of Integration:",
                                          relief=tk.RAISED,
                                          bg="floral white")
        self.upper_lim_var = tk.StringVar(self.window, value=None)
        self.upper_lim_entry = tk.Entry(self.window,
                                          textvariable=self.upper_lim_var,
                                          **self.style)

        # Lower limit of integration
        self.lower_lim_label = tk.Label(self.window,
                                    text="Lower Limit of Integration:",
                                    relief=tk.RAISED,
                                    bg="floral white")
        self.lower_lim_var = tk.StringVar(self.window, value=None)
        self.lower_lim_entry = tk.Entry(self.window,
                                          textvariable=self.lower_lim_var,
                                          **self.style)


class AnalysisSection:
    """Encapsulates Widgets for 'Analysis Frame' LabelFrame.

    This class is bound to the MainApp window.
    """
    def __init__(self, window=None, entry_section=None):
        """Define widgets for this LabelFrame."""
        # window of MainApp is also window of this class
        self.window = window

        # Tuple (figure PhotoImage, str outfile) result                       
        self.analysis_result = None

        # Limits
        self.entry_section = entry_section
        self.lower_lim = self.entry_section.lower_lim_var
        self.upper_lim = self.entry_section.upper_lim_var

        # LabelFrame
        self.frame = tk.LabelFrame(self.window, text="Analysis Frame", 
                                   padx=5, pady=5, width=40) 
        
        # File dialog
        self.home = str(Path.home())  # Path to home directory
        self.file_types = (("asc files", "*.asc"),)
        self.file_path = None
        self.file_name_var = tk.StringVar(self.window, 
                                          value="File Name Displays Here")
        self.file_button = tk.Button(self.window, 
                              text="Click to Choose .ASC File",
                              command=self.open_dialog,
                              bg = "bisque")
        self.file_label = tk.Label(self.window, 
                                   textvariable=self.file_name_var,
                                   width=40,
                                   bd=4,
                                   relief=tk.SUNKEN,
                                   wraplength=280)

        # Analyze button
        self.analysis_button = tk.Button(self.window,
                                         text="Click to Analyze Data",
                                         command=self.do_analysis,
                                         bg="bisque")


    def open_dialog(self):
        """Popup for file dialog and set file path/name"""
        # Dialog
        self.file_path = fd.askopenfilename(title="Select ASC file",
                                                  initialdir=self.home,
                                                  filetypes=self.file_types)

        # Set the file name
        fname = "".join(reversed(self.file_path[
                                    -1:self.file_path.rfind("/"):-1]))

        self.file_name_var.set(fname)

        return None

        
    def do_analysis(self):
        """Instantiate NmrAnalysis and return plots."""
        # Instantiate NmrAnalyzer
        analyzer = NmrAnalyzer(self.lower_lim, self.upper_lim,
                               self.file_path, self.file_name_var)

        # Tuple (figure PhotoImage, str outfile) result                       
        self.analysis_result = analyzer.proc_data()

        # Create new window for matplotlib figure
        self.new_window()

        return None


    def new_window(self):
        """Create the window for the matplotlib figure.

        This is analagous to tk.Frame(self.window) where 
        self.window = tk.Tk(). Toplevel allows for the creation of a 
        window instance under the existing tk.Tk() object versus 
        creating a completely new tk.Tk() object.
        """
        self.analysis_window = AnalysisWindow(tk.Toplevel(self.window), 
                                              self.analysis_result,
                                              self.entry_section)

        return None


class AnalysisWindow:
    """Displays the graph and should have a menu.

    This is a window initialized using the tk.Toplevel Widget.
    There is no need to create a frame for rendering the window itself
    since the tk.Toplevel Widget behaves like a frame.
    """
    def __init__(self, new_window=None, analysis_result=None, 
                 entry_section=None):
        """Initialize new analysis window and some configuration."""
        # Constructor
        self.new_window = new_window  # Control frame
        self.analysis_result = analysis_result  # (MyImage, str log)
        self.entry_section = entry_section  # Entry section for MenuSection

        # Title
        self.new_window.title("Data Analysis Window")

        # Tuple (MyImage, str log)
        self.analysis_result = analysis_result

        # Plot label
        self.plot_label = tk.Label(self.new_window,
                                image=self.analysis_result[0].get_photoimage(),
                                relief=tk.RAISED)

        # Outfile
        self.outfile_area = self.analysis_result[1].split(",")[-1]
        self.outfile_label = tk.Label(self.new_window, 
                                      text=f"Area: {self.outfile_area}",
                                      relief=tk.SUNKEN)
        self.outfile_label.config(font=("Arial", 16))

        # Grid Widgets
        self.grid_widgets()

        # Menu
        self.menu_section = MenuSection(self.new_window, self.entry_section,
                                        self.analysis_result)


    def grid_widgets(self):
        """Control geometry of Widgets for AnalysisWindow."""
        self.plot_label.grid(row=0, column=0)
        self.outfile_label.grid(row=1, column=0)
        

        return None


class MenuSection:
    """Encapsulates Widgets and methods for a menu.

    This class is bound to the AnalysisWindow window.

    The purpose of the menu is to prompt the user to save
    the matplotlib image and the outfile, the outfile alone, or the
    plot.
    """
    def __init__(self, window=None, entry_section=None,
                 analysis_result=None):
        """Create the menubar and subsequent pulldowns (cascading)."""
        # Constructor
        self.window = window
        self.entry_section = entry_section  # For naming plot and outfiles 
        self.analysis_result = analysis_result

        # Main menu
        self.main_menu = tk.Menu(self.window)

        # Define cascading menu for save_options
        self.save_options_menu = tk.Menu(self.main_menu, tearoff=0)
        self.save_options_menu.add_command(label="Save Plot",
                                           command=self.save_plot)
        self.save_options_menu.add_command(label="Save Outfile",
                                           command=self.save_outfile)
        self.save_options_menu.add_command(label="Save Both",
                                           command=self.save_both)

        # Define cascading menu for plot_options
        self.plot_options_menu = tk.Menu(self.main_menu, tearoff=0)
        self.plot_options_menu.add_command(label="New Title", 
                                           command=self.new_title)
        self.plot_options_menu.add_command(label="New X-Label",
                                           command=lambda : self.new_ax("x"))
        self.plot_options_menu.add_command(label="New Y-Label",
                                           command=lambda : self.new_ax("y"))

        # Add the cascading menus to the main_menu
        self.main_menu.add_cascade(label="Save Options", 
                                   menu=self.save_options_menu)
        self.main_menu.add_cascade(label="Plot Options",
                                   menu=self.plot_options_menu)
        
        # Configure window
        self.window.config(menu=self.main_menu)

    def save_plot(self):
        """Save the the matplotlib photoimage only.
        
        Opens save file dialog.
        """
        # Returns directory name into which plot will be saved
        save_dir = fd.askdirectory(title="Select Directory",
                                     initialdir=str(Path.home()))

        # Ask name to save the file as 
        save_fname = fd.asksaveasfilename(title="Save Plot",
                                     initialdir=save_dir,
                                     defaultextension=".png",
                                     filetypes=(("png files", "*.png"),
                                                ("svg files", "*.svg"),
                                                ("jpg files", "*.jpg")))

        # Save using PhotoImage file attr, which is file=Image.open()
        img = self.analysis_result[0].get_opened_img()
        img.save(os.path.join(save_dir, save_fname))

        return None

    
    def save_outfile(self):
        """Save the outfile only.
        
        Opens save file dialog.
        """
        # Name of directory to save file to
        save_dir = fd.askdirectory(title="Select Directory",
                                   initialdir=str(Path.home()))

        # File name that is going to be saved
        save_fname = fd.asksaveasfilename(title="Save Outfile",
                                     initialdir=save_dir,
                                     defaultextension=".csv",
                                     filetypes=(("csv files", "*.csv"),))

        # Save the file
        with open(os.path.join(save_dir, save_fname), "w") as fobj:
            fobj.write(self.analysis_result[1])

        return None

    
    def save_both(self):
        """Save both the outfile and the matplotlib photoimage.
        
        Call both functions.
        """
        # Call Both other save functions
        self.save_plot()
        self.save_outfile()

        return None

    
    def new_title(self):
        """New title for matplotlib plot."""
        return None

    
    def new_ax(self, ax=None):
        """New axis label for matplotlib plot."""
        if (ax == "x"):
            pass
        else:
            pass
        return None

