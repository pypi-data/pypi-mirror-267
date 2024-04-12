import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import webbrowser
import customtkinter as ctk
from PIL import Image
from PIL import ImageTk
import os
import sys
import random
import numpy as np
from configparser import ConfigParser
import pooch

#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """This function wraps a relative path with dirname to help with the assets.

    Args:
        relative_path: Relative os.path-like path from the root of the project

    Returns:
        The wrapped path for a relative file or folder.
    """
    base_path = os.path.dirname(__file__)
    
    return os.path.join(base_path, relative_path)

class SplashScreen:
    """This class contains the splash screen for the project and the loading for the main window.
    """
    def __init__(self, master):
        self.master = master

        self.master.title("Felon Finder - Chargement")
        splash_width = int(1/5*self.master.winfo_screenwidth())
        splash_height = int(1/5*self.master.winfo_screenheight())
        center_window_on_screen(self.master, splash_width, splash_height)
        self.master.overrideredirect(True)

        self.mainFrame = ctk.CTkFrame(self.master, fg_color=self.master._fg_color)
        self.barFrame = ctk.CTkFrame(self.master, fg_color=self.master._fg_color)

        self.titleLabel = ctk.CTkLabel(self.mainFrame, text="FELON FINDER - Débusque ton agresseur", font=("Helvetica", 18))
        self.titleLabel.pack(pady = 70)
        self.subtitleLabel = ctk.CTkLabel(self.mainFrame, text="Chargement en cours...", font=("Helvetica", 14))
        self.subtitleLabel.pack()

        self.progressBar = ctk.CTkProgressBar(self.barFrame, width=splash_width, height=splash_height)
        self.progressBar.set(0)
        self.progressBar.pack()

        self.mainFrame.pack()
        self.barFrame.pack()

        self.loading()

    def loading(self):
        """This function loads the time and resource consuming for the main program before showing the main window.
        """
        self.subtitleLabel.configure(text = "Chargement des librairies... Librairie 1/2")
        self.progressBar.set(0.3)
        self.master.update()

        from .utils.varencoder import VAE, encoder_create, decoder_create

        self.subtitleLabel.configure(text = "Chargement de l'auto-encodeur...")
        self.progressBar.set(0.7)
        self.master.update()

        POOCH = pooch.create(
            # Use the default cache folder for the OS
            path=os.path.join(os.path.dirname(__file__),'saved_model'),
            # The remote data is on Github
            base_url="https://zenodo.org/records/10957695/files/felon_finder_vae.weights.h5?download=1",
            # The registry specifies the files that can be fetched
            registry={
                # The registry is a dict with file names and their SHA256 hashes
                "felon_finder_vae.weights.h5": "38595de4ea78d8a1ba21f7b1a3a3b3c7c1c4c862bf3b290c5cd9d2ebaccc16fa",
            },
        )

        vae_weights = POOCH.fetch("felon_finder_vae.weights.h5")

        global vae
        vae = VAE(encoder_create(), decoder_create())
        vae.load_weights(vae_weights)

        self.master.after(500, None)

        self.subtitleLabel.configure(text = "Lancement de Felon Finder...")
        self.progressBar.set(1.0)
        self.master.update()

        self.master.after(2000, None)

        self.master.destroy()

        config = ConfigParser()
        config.read(resource_path(os.path.join('cfg','config.ini')))

        if int(config['current']['dark_mode']) == 1:
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("dark-blue")
        else:
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")

        root = ctk.CTk()

        global main_width
        global main_height

        main_width = int(4/5*root.winfo_screenwidth())
        main_height = int(4/5*root.winfo_screenheight())
        center_window_on_screen(root, main_width, main_height)

        on_closing = create_root_closing_handler(root)
        root.protocol("WM_DELETE_WINDOW", on_closing)

        MainScreen(root)
        root.mainloop()

class MainScreen:
    """This class contains the main window of the program.
    """
    def __init__(self, master):
        """Initialization of the window with all the pictures of the database and the main buttons.

        Args:
            master: Customtkinter main window
        """
        self.n_images = 12
        self.n_showed_images = 4

        self.master = master
        self.master.title("Felon Finder - Fenêtre principale")

        if self.master.winfo_screenheight() < 1024:
            self.mainFrame = ctk.CTkScrollableFrame(self.master, width=main_width, height=main_height)
            self.topFrame = ctk.CTkFrame(self.mainFrame)
            self.middleFrame = ctk.CTkFrame(self.mainFrame)
            self.middleFrame2 = ctk.CTkFrame(self.mainFrame)
            self.middleFrame3 = ctk.CTkFrame(self.mainFrame)
            self.bottomFrame = ctk.CTkFrame(self.mainFrame)
            self.master.resizable(True, True)
        else:
            self.mainFrame = ctk.CTkFrame(self.master, width=main_width, height=main_height)
            self.mainFrame.pack_propagate(False)
            self.topFrame = ctk.CTkFrame(self.mainFrame, fg_color=self.mainFrame._fg_color)
            self.middleFrame = ctk.CTkFrame(self.mainFrame, fg_color=self.mainFrame._fg_color)
            self.middleFrame2 = ctk.CTkFrame(self.mainFrame, fg_color=self.mainFrame._fg_color)
            self.middleFrame3 = ctk.CTkFrame(self.mainFrame, fg_color=self.mainFrame._fg_color)
            self.bottomFrame = ctk.CTkFrame(self.mainFrame, fg_color=self.mainFrame._fg_color)
            self.master.resizable(0, 0)

        self.titleLabel = ctk.CTkLabel(self.topFrame, text="FELON FINDER - Débusque ton agresseur", font=("Helvetica", 30))
        self.titleLabel.pack()
        self.subtitleLabel1 = ctk.CTkLabel(self.topFrame, text="Sélectionnez une image...", font=("Helvetica", 22))
        self.subtitleLabel1.pack(pady=20)
        self.subtitleLabel2 = ctk.CTkLabel(self.topFrame, text="Aucune image sélectionnée", font=("Helvetica", 18))
        self.subtitleLabel2.pack()

        self.path_img = resource_path(os.path.join('img'))
        self.path_celeba = resource_path(os.path.join(self.path_img, 'faces'))
        self.images = []
        for filename in os.listdir(self.path_celeba):
            self.images.append(ctk.CTkImage(Image.open(resource_path(os.path.join(self.path_celeba,filename))), Image.open(resource_path(os.path.join(self.path_celeba,filename))), (250, 250)))

        self.showed_images_list = []
        self.buttons = {}
        for _, image in enumerate(self.images[0:self.n_showed_images]):
            self.showed_images_list.append(image)
            button = ctk.CTkButton(
                self.middleFrame,
                text=None,
                image=image,
                command=lambda img=image: self.select_image(img)
            )
            button.pack(side="left", padx=15)
            button.selected = False
            self.buttons[image] = button
        
        self.selected_images_list = []
        
        self.shuffleButton = ctk.CTkButton(self.middleFrame2, text = 'Nouvelles photos', width = 25, command = self.get_random_images, font=("Helvetica", 16))
        self.shuffleButton.pack(side = "left", padx = 25)
        self.validationButton = ctk.CTkButton(self.middleFrame2, text = 'Valider', width = 25, command = self.check_validation, font=("Helvetica", 16))
        self.refreshButton = ctk.CTkButton(self.middleFrame2, text = 'Rafraîchir', width = 25, command = self.refresh, font=("Helvetica", 16))
        self.saveButton = ctk.CTkButton(self.middleFrame2, text = 'Enregistrer', width = 25, command = self.save_images, font=("Helvetica", 16))
        self.backButton = ctk.CTkButton(self.middleFrame2, text = 'Photos précédentes', width = 25, command = self.back_to_last_images, font=("Helvetica", 16))

        self.ref_label = ctk.CTkLabel(self.middleFrame3, text = "Photos de référence", font=("Helvetica", 18))
        self.ref_label.grid(row = 0, column=1, columnspan=4, pady = 10)

        self.unknown = ctk.CTkImage(Image.open(os.path.join(self.path_img,'unknown.png')),Image.open(os.path.join(self.path_img,'unknown.png')), (125, 125))
        self.unknown_pics = []
        for i in range(self.n_showed_images):
            label = ctk.CTkLabel(self.middleFrame3, text = "", image = self.unknown)
            label.grid(row = 1, column = i+1, padx = 15)
            self.unknown_pics.append(label)

        self.show_combobox()
            
        self.filterButton = ctk.CTkButton(self.bottomFrame, text = 'Créer un filtre', width = 25, command = self.filterwindow, font=("Helvetica", 16))
        self.filterButton.pack(side = "left", padx = 50)
        self.optionsButton = ctk.CTkButton(self.bottomFrame, text = 'Paramètres', width = 25, command = self.options_window, font=("Helvetica", 16))
        self.optionsButton.pack(side = "left", padx = 50)
        self.tutorialButton = ctk.CTkButton(self.bottomFrame, text = 'Ouvrir le tutoriel', width = 25, command = self.tutorial_window, font=("Helvetica", 16))
        self.tutorialButton.pack(side = "right", padx = 50)
        self.quitButton = ctk.CTkButton(self.bottomFrame, text = 'Quitter le programme', width = 25, command = self.close_window, font=("Helvetica", 16))
        self.quitButton.pack(side = "right", padx = 50)

        self.mainFrame.pack()
        self.topFrame.pack(side = "top", pady = 50)
        self.middleFrame.pack()
        self.middleFrame2.pack(pady = 30)
        self.middleFrame3.pack(pady = 20)
        self.bottomFrame.pack(side = "bottom", pady = 10)
        self.filterWindow = None
        self.optionsWindow = None
        self.tutorialWindow = None
    
    def show_combobox(self):
        """This function shows the drop down list for filter selection.
        """
        self.filter_file_path = os.path.join(os.path.dirname(__file__),'saved_filters')
        self.FilterList =["None"]+[name for name in os.listdir(self.filter_file_path)]
        self.SelectFilter=ctk.CTkComboBox(self.bottomFrame, values=self.FilterList)
        self.SelectFilter.pack(side = "left", padx = 50)
        
    def filterwindow(self):
        """This function launches the filter window or shows it if it was behind.
        """
        if self.filterWindow is None or not self.filterWindow.winfo_exists():
            self.filterWindow = ctk.CTkToplevel(self.master)
            self.filterWindow.after(10, self.filterWindow.focus)
            self.app = Filter(self.filterWindow) # c'est quoi self.app ??
            #self.master.wait_window(self.filterWindow)
            self.udpate_combobox()
        else:
            self.filterWindow.focus()
            
    def udpate_combobox(self):
        """This function refreshes the filters drop down list once the filter menu is closed.
        """
        self.filter_file_path = os.path.join(os.path.dirname(__file__),'saved_filters')
        self.FilterList =["None"]+[name for name in os.listdir(self.filter_file_path)]
        self.SelectFilter.configure(values=self.FilterList)
        return

    def options_window(self):
        """This function launches the options window or shows it if it was behind.
        """
        if self.optionsWindow is None or not self.optionsWindow.winfo_exists():
            self.optionsWindow = ctk.CTkToplevel(self.master)
            self.optionsWindow.after(10, self.optionsWindow.focus)
            self.app = Options(self.optionsWindow)
        else:
            self.optionsWindow.focus()

    def tutorial_window(self):
        """This function launches the tutorial window or shows it if it was behind.
        """
        if self.tutorialWindow is None or not self.tutorialWindow.winfo_exists():
            self.tutorialWindow = ctk.CTkToplevel(self.master)
            self.tutorialWindow.after(10, self.tutorialWindow.focus)
            self.app = Tutorial(self.tutorialWindow)
        else:
            self.tutorialWindow.focus()

    def close_window(self):
        """This function asks for the user's confirmation to close the program.
        """
        if tk.messagebox.askokcancel("Fermeture", "Vous allez fermer le programme. Continuer ?"):
            self.master.destroy()
    
    def get_random_images(self):
        """This function gets random pictures from the database after the user clicked on "Nouvelles photos"
        """
        random_images = dict.fromkeys(self.buttons, 0)
        i = len(random_images)
        
        while len(random_images) < 2 * self.n_showed_images:
            random_image = random.choice(self.images)
            if random_image not in random_images:
                self.add_image_to_showed_list(random_image)
                random_images[random_image] = i
                i += 1
        random_images_list = list(random_images)[self.n_showed_images:2*self.n_showed_images]

        self.update_images(random_images_list)

        self.reset_ref()
    
    def save_images(self):
        """This function saves the selected pictures in the selected path if it exists, else asks what path to choose.
        """
        config = ConfigParser()
        config.read(resource_path(os.path.join('cfg','config.ini')))

        if 'saved_images_path' not in config['current']:
            tk.messagebox.showinfo(title="Information", message="C'est la première fois que vous enregistrez des images.\n\nChoisissez le dossier dans lequel vous voulez que vos images soient sauvegardées à l'avenir.")
            given_path = filedialog.askdirectory()
            if given_path != "" and given_path != "Aucun chemin sélectionné":
                config.set('current', 'saved_images_path', given_path)
                with open(resource_path(os.path.join('cfg','config.ini')), 'w') as conf:
                    config.write(conf)
                config.read(resource_path(os.path.join('cfg','config.ini')))
            else:
                tk.messagebox.showerror(title="Erreur", message="Vous n'avez choisi aucun chemin, pas d'enregistrement.\nSongez à en choisir un correct ici ou dans les paramètres.")
                return
        
        path = config['current']['saved_images_path']

        if not os.path.exists(path):
            os.makedirs(path)
            existing_path = path
        else:
            existing_path = path
        
        existing_images = os.listdir(resource_path(existing_path))

        existing_numbers = [int(f.split('_')[1].split('.')[0]) for f in existing_images if f.startswith('image_')]
        if existing_numbers:
            initial_i = max(existing_numbers)
        else:
            initial_i = 0

        i = 0
        saved_images_filenames = []
        for img in self.buttons:
            if self.buttons[img].selected:
                i += 1
                self.buttons[img]._image._dark_image.save(resource_path(os.path.join(existing_path,f'image_{initial_i+i}.jpg')))
                saved_images_filenames.append(f"image_{initial_i+i}.jpg")
        if i == 1:
            tk.messagebox.showinfo(title="Enregistré", message=f"L'image a été enregistrée dans le dossier {existing_path} au nom:\n\n- {saved_images_filenames[0]}")
        else:
            files = ['\n- '+str(x) for x in saved_images_filenames]
            tk.messagebox.showinfo(title="Enregistré", message=f"Les images suivantes ont été enregistrées dans le dossier {existing_path}:\n{''.join(str(x) for x in files)}")
    
    def update_images(self, images_list):
        """This function updates the showed images to keep track of the images in the main buttons.

        Args:
            images_list: An array of the new images to show
        """
        for img in self.buttons:
            self.buttons[img].destroy()
        
        self.master.update()

        self.buttons = {}
        for image in images_list:
            button = ctk.CTkButton(
                self.middleFrame,
                text=None,
                image=image,
                command=lambda img=image: self.select_image(img)
            )
            button.pack(side="left", padx=15)
            button.selected = False
            button.after(10)
            self.buttons[image] = button
        
        self.update_label()
    
    def select_image(self, image):
        """This function turns the buttons red or blue and their hover color to darker red or darker blue according to if they were selected or un-selected by the user.

        Args:
            image: The selected image
        """
        button = self.buttons[image]
        if not button.selected:
            button.selected = True
            button.configure(fg_color = 'red', hover_color = 'darkred')
        else:
            button.selected = False
            button.configure(fg_color = ctk.CTkButton(self.master)._fg_color, hover_color = ctk.CTkButton(self.master)._hover_color)
        self.update_label()
    
    def update_label(self):
        """This function updates the labels to keep the user aware of the amount of images selected and help them choose their next action. 
        """
        cpt = 0
        for img in self.buttons:
            if self.buttons[img].selected:
                cpt+=1
        if cpt == 0:
            self.subtitleLabel1.configure(text = "Sélectionnez une image...")
            self.subtitleLabel2.configure(text = "Aucune image sélectionnée")
            self.validationButton.forget()
            self.saveButton.forget()
            if self.selected_images_list:
                self.refreshButton.pack(side = "left", padx = 25)
            else:
                self.refreshButton.forget()
        elif cpt == 1:
            self.subtitleLabel1.configure(text = "Vous pouvez valider cette image ou en sélectionner plus...")
            self.subtitleLabel2.configure(text = "1 image sélectionnée")
            self.validationButton.pack(side = "left", padx = 25)
            self.saveButton.pack(side = "left", padx = 25)
            self.refreshButton.forget()
        else:
            self.subtitleLabel1.configure(text = "Validez votre choix pour combiner les visages...")
            self.subtitleLabel2.configure(text = f"{cpt} images sélectionnées")
    
    def check_validation(self):
        """This function applies the VAE and the genetic algorithm to the selected images and shows the decoded results in the buttons. The selected images are then kept in reference.
        """
        #Bad practice: importing at each validation
        #But for some reason it stucks the loading if we import above
        from .utils.algogen import one_selection, two_selections, multiple_selections
        from tensorflow.keras.utils import array_to_img # type: ignore

        cpt = 0
        arrays = []
        self.selected_images_list = []
        for img in self.buttons:
            if self.buttons[img].selected:
                self.select_image(img)
                arrays.append(np.array(self.buttons[img]._image._dark_image.resize((64, 64)))/255)
                self.selected_images_list.append(np.array(self.buttons[img]._image._dark_image.resize((64, 64)))/255)
                ctk_img = ctk.CTkImage(self.buttons[img]._image._dark_image, self.buttons[img]._image._dark_image, (125, 125))
                self.unknown_pics[cpt].configure(image = ctk_img)
            else:
                self.unknown_pics[cpt].configure(image = self.unknown)
            self.buttons[img].configure(image = random.choice(self.images))
            cpt += 1
        
        cpt = 0

        _,_,x_encoded = vae.encoder(np.array(arrays))

        if len(x_encoded == 1):
            config = ConfigParser()
            config.read(resource_path(os.path.join('cfg','config.ini')))

            x_encoded = one_selection(x_encoded[0], std = float(config['current']['variance']), m = float(config['current']['mean']))
        elif len(x_encoded) == 2:
            x_encoded = two_selections(x_encoded[0], x_encoded[1])
        else:
            x_encoded = multiple_selections(x_encoded)
        
        if self.SelectFilter.get() == "None":
            x_decoded = vae.decoder(x_encoded)
            images = [array_to_img(x) for x in x_decoded]
        else: # apply the filter 
            self.FilterToApply = np.load(os.path.join(os.path.dirname(__file__),'saved_filters',str(self.SelectFilter.get())))
            x_decoded=vae.decoder(np.array([x_encoded[i]+self.FilterToApply for i in range(len(x_encoded))]))
            images = [array_to_img(x) for x in x_decoded]

        for img in self.buttons:
            if cpt < len(images):
                ctk_img = ctk.CTkImage(images[cpt], images[cpt], img._size)
                self.buttons[img].configure(image = ctk_img)
                self.master.update()
                self.buttons[img].after(50)
                cpt += 1
            self.add_image_to_showed_list(self.buttons[img]._image)
        
        self.update_label()
    
    def refresh(self):
        """This function applies again the VAE and the genetic algorithm to the previously selected and treated images and shows the decoded results in the buttons. The selected images are still kept in reference.
        """
        #Bad practice: importing at each refresh
        #But for some reason it stucks the loading if we import above
        from .utils.algogen import one_selection, two_selections, multiple_selections
        from tensorflow.keras.utils import array_to_img # type: ignore

        cpt = 0

        _,_,x_encoded = vae.encoder(np.array(self.selected_images_list))
        if len(x_encoded == 1):
            config = ConfigParser()
            config.read(resource_path(os.path.join('cfg','config.ini')))

            x_encoded = one_selection(x_encoded[0], std = float(config['current']['variance']), m = float(config['current']['mean']))
        elif len(x_encoded) == 2:
            x_encoded = two_selections(x_encoded[0], x_encoded[1])
        else:
            x_encoded = multiple_selections(x_encoded)
        
        if self.SelectFilter.get() == "None":
            x_decoded = vae.decoder(x_encoded)
            images = [array_to_img(x) for x in x_decoded]
        else: # apply the filter 
            self.FilterToApply = np.load(os.path.join(os.path.dirname(__file__),'saved_filters',str(self.SelectFilter.get())))
            x_decoded=vae.decoder(np.array([x_encoded[i]+self.FilterToApply for i in range(len(x_encoded))]))
            images = [array_to_img(x) for x in x_decoded]

        for img in self.buttons:
            if cpt < len(images):
                ctk_img = ctk.CTkImage(images[cpt], images[cpt], img._size)
                self.buttons[img].configure(image = ctk_img)
                self.master.update_idletasks()
                self.buttons[img].after(50)
                cpt += 1
            self.add_image_to_showed_list(self.buttons[img]._image)
    
    def add_image_to_showed_list(self, image):
        """This function keeps the given image in memory through an array.

        Args:
            image: Image to keep in memory
        """
        if(len(self.showed_images_list) >= self.n_showed_images):
            self.backButton.pack(side = "right", padx = 25)
        self.showed_images_list.append(image)
    
    def back_to_last_images(self):
        """This function removes the last showed images and changes the buttons to make them show to the ones before that. The reference list is also emptied.
        """
        for _ in self.buttons:
            self.showed_images_list.pop(-1)
        self.update_images(self.showed_images_list[-1*self.n_showed_images:])
        if(len(self.showed_images_list) <= self.n_showed_images):
            self.backButton.forget()
        self.reset_ref()
    
    def reset_ref(self):
        """This function clears the reference images array and puts back unknown.png faces in the reference labels.
        """
        for lab in self.unknown_pics:
                lab.configure(image = self.unknown)
                self.selected_images_list = []
                self.update_label()

class Filter:
    """This class contains the filter menu of the program. Once it is launched, the main window of the program is disabled to avoid mistakes.
    """
    def __init__(self, master):
        """Initialization of the filter menu.

        Args:
            master: Customtkinter filter window
        """
        self.master = master
        self.master.attributes("-topmost", True)
        self.master.title("Créer un filtre")
        self.master.resizable(0, 0)
        width = main_width
        height = main_height
        self.n_showed_images = 5
        center_window_on_screen(self.master, width, height)

        self.frame = ctk.CTkFrame(self.master, width = width, height = main_height-300, fg_color=self.master._fg_color) 
        self.frame.pack_propagate(False)
        self.lowerframe = ctk.CTkFrame(self.master, width = width, height = 200, fg_color=self.master._fg_color) 
        self.frame.pack_propagate(False)
        self.bottomFrame = ctk.CTkFrame(self.master, width = width, height = height-self.frame._current_height, fg_color = self.master._fg_color) 
        self.frame.pack_propagate(False)
        
        self.labeletape1 = ctk.CTkLabel(self.frame, text = "Choisir le nombre d'étapes:", font=("Helvetica", 16), fg_color="transparent", text_color= "white")
        self.labeletape1.pack()
        self.labeletape2 = ctk.CTkLabel(self.frame, text = "5", font=("Helvetica", 14))
        self.labeletape2.pack()
        self.slidervaluelist = [i for i in range(1, 11)]
        self.slideretapes = ctk.CTkSlider(self.frame, from_ = min(self.slidervaluelist), to = max(self.slidervaluelist), command = self.valueslideretapes)
        self.newvalue = 5
        self.slideretapes.pack()
        
        self.filterStartButton = ctk.CTkButton(self.frame, text = 'Démarrer', width = 25, command = self.create_filter, font=("Helvetica", 16))
        self.filterStartButton.pack(padx=5)

        self.NButton = ctk.CTkButton(self.bottomFrame, text = "Quitter", width = 25, command = self.close_window, font=("Helvetica", 16))
        self.NButton.pack(side = "left", padx = 20)

        self.frame.pack(pady = 10)
        self.lowerframe.pack(pady = 10)
        self.bottomFrame.pack(side = "bottom", pady = 10)

        self.master.wait_visibility()
        self.master.grab_set()
        
    def create_filter(self):
        """This function creates the initial filter menu.
        """
        self.slideretapes.configure(hover=False, state="disabled")
        self.filterStartButton.configure(hover=False)
        
        self.filter_file_path = os.path.join(os.path.dirname(__file__),'saved_filters')
        self.number_of_available_filter = len([name for name in os.listdir(self.filter_file_path)])
        self.list_difference_vector=[]
        self.current_step=1
        self.show_which_step()
        self.show_imgs()
        self.show_selection_menu()

        return
    
    def show_which_step(self):
        """This function keeps the user aware of the current step of filter creation.
        """
        self.current_step_widget = {}
        self.etapeLabel = ctk.CTkLabel(self.frame, text='Etape '+str(self.current_step)+' sur '+str(int(self.newvalue)), font=("Helvetica", 16), fg_color="transparent", text_color="white")
        self.etapeLabel.pack()
        self.current_step_widget["etapeLabel"] = self.etapeLabel 
        self.explanationLabel =ctk.CTkLabel(self.frame, text='Choisissez une image ressemblante et une image non ressemblante', font=("Helvetica", 16), fg_color="transparent", text_color="white")
        self.explanationLabel.pack()
        self.current_step_widget["explanationLabel"] = self.explanationLabel 
        return
    
    def show_selection_menu(self):
        """This function creates the buttons used to create the filters with the selected images.
        """
        self.selection_menu_widgets={}
        list_img_nbr=[str(i) for i in range(1,self.n_showed_images+2)]
        self.LabelImageRessemblante=ctk.CTkLabel(self.lowerframe, text="Numéro de l'image ressemblante", font=("Helvetica", 16), fg_color="transparent", text_color="white")
        self.LabelImageRessemblante.pack()
        self.selection_menu_widgets["LabelImageRessemblante"]=self.LabelImageRessemblante
        self.ComboBoxImageRessemblante=ctk.CTkComboBox(self.lowerframe, values=list_img_nbr)
        self.ComboBoxImageRessemblante.set("1")
        self.ComboBoxImageRessemblante.pack()
        self.selection_menu_widgets["ComboBoxImageRessemblante"]=self.ComboBoxImageRessemblante
        self.NoneImageRessemblante=ctk.CTkButton(self.lowerframe, text="Aucune image",font=("Helvetica", 16), command=self.no_image_selected)
        self.NoneImageRessemblante.pack()
        self.selection_menu_widgets["NoneImageRessemblante"]=self.NoneImageRessemblante
                    
        self.LabelImagePASRessemblante=ctk.CTkLabel(self.lowerframe, text="Numéro de l'image pas ressemblante", font=("Helvetica", 16), fg_color="transparent", text_color="white")
        self.LabelImagePASRessemblante.pack()
        self.selection_menu_widgets["LabelImagePASRessemblante"]=self.LabelImagePASRessemblante
        self.ComboBoxImagePASRessemblante=ctk.CTkComboBox(self.lowerframe, values=list_img_nbr)
        self.ComboBoxImagePASRessemblante.set("1")
        self.ComboBoxImagePASRessemblante.pack()
        self.selection_menu_widgets["ComboBoxImagePASRessemblante"]=self.ComboBoxImagePASRessemblante
        self.NoneImagePASRessemblante=ctk.CTkButton(self.lowerframe, text="Aucune image",font=("Helvetica", 16), command=self.no_image_selected)
        self.NoneImagePASRessemblante.pack()
        self.selection_menu_widgets["NoneImagePASRessemblante"]=self.NoneImagePASRessemblante
        self.ValidateStep = ctk.CTkButton(self.lowerframe, text="Valider etape "+str(self.current_step), font=("Helvetica", 20), command=self.new_step, fg_color= "lime green")
        self.ValidateStep.pack(pady=10)
        self.selection_menu_widgets["ValidateStep"]=self.ValidateStep
        return
    
    def show_imgs(self):
        """This function shows the images usable to create the filter.
        """
        self.path = os.path.join(os.path.dirname(__file__),'img')
        self.path_celeba = os.path.join(self.path,'faces')
        self.images = []
        self.numpyimages = []
        
        for filename in os.listdir(self.path_celeba):
            self.images.append(ctk.CTkImage(Image.open(os.path.join(self.path_celeba,filename)), Image.open(os.path.join(self.path_celeba,filename)), (64, 64)))
            self.numpyimages.append(Image.open(os.path.join(self.path_celeba,filename)))
            if len(self.images) >= 500:
                break

        self.showed_images_list = []
        self.buttons = {}
        numero_de_limage = 0

        from tensorflow.keras.utils import array_to_img # type: ignore
        
        self.dic_of_imgs = {}
        while len(self.buttons) < self.n_showed_images + 1:
            random_image1 = random.choice(self.images)
            random_numpy_image = random.choice(self.numpyimages)
            _,_,random_img_encoded = vae.encoder(np.array([np.array(random_numpy_image.resize((64, 64))).astype("float32")/255]))
            random_img_decoded = vae.decoder(random_img_encoded)
            images_to_select = [array_to_img(x) for x in random_img_decoded]
            if random_image1 not in self.buttons:
                numero_de_limage += 1
                self.showed_images_list.append(random_image1)
                self.my_image = ctk.CTkImage(light_image=images_to_select[0],
                                  dark_image=images_to_select[0],
                                  size=(200, 200))
                self.my_image_label = ctk.CTkLabel(self.frame, text = str(numero_de_limage), font=('Helvetica',35), image = self.my_image, compound="bottom")
                self.my_image_label.pack(side="left", padx=15, expand=True)
                self.buttons[random_image1] =  self.my_image_label
                self.dic_of_imgs[numero_de_limage] = np.array(random_numpy_image.resize((64, 64))).astype("float32")/255
        return
    
    def no_image_selected(self):
        """This function refreshes the proposed images when the user presses the "Aucune image" button.
        """
        for img in self.buttons:
            self.buttons[img].destroy()
        for widget in self.selection_menu_widgets:
            self.selection_menu_widgets[widget].destroy()
        self.show_imgs()
        self.show_selection_menu()
        return
    
    def new_step(self):
        """This function creates again the selection menu for each new step of the filter creation.
        """
        if self.current_step < self.newvalue:
            img_PAS_ressemblante = self.dic_of_imgs[int(self.ComboBoxImagePASRessemblante.get())]
            img_ressemblante = self.dic_of_imgs[int(self.ComboBoxImageRessemblante.get())]
            
            _,_,x_encoded = vae.encoder(np.array([img_ressemblante,img_PAS_ressemblante]))
            self.list_difference_vector.append(x_encoded[0]-x_encoded[1])
            self.current_step+=1
            
            for img in self.buttons:
                self.buttons[img].destroy()
            for widget in self.selection_menu_widgets:
                self.selection_menu_widgets[widget].destroy()
            for text in self.current_step_widget:
                self.current_step_widget[text].destroy()
            self.show_which_step()
            self.show_imgs()
            self.show_selection_menu()
        else:
            self.mean_difference_vector = np.array(self.list_difference_vector).mean(0)
            np.save(os.path.join(self.filter_file_path,'filter'+str(self.number_of_available_filter+1)+'.npy'), self.mean_difference_vector)
            for img in self.buttons:
                self.buttons[img].destroy()
            for widget in self.selection_menu_widgets:
                self.selection_menu_widgets[widget].destroy()
            for text in self.current_step_widget:
                self.current_step_widget[text].destroy()
            self.LabelImagePASRessemblante=ctk.CTkLabel(self.lowerframe, text="Le filtre a été créé, retournez sur la page principale en cliquant 'Quitter'", font=("Helvetica", 30), fg_color="transparent", text_color="white")
            self.LabelImagePASRessemblante.pack()
        return

    def close_window(self):
        """This function closes the window and makes the main window usable again.
        """
        self.master.grab_release()
        self.master.destroy()
    
    def valueslideretapes(self, value):
        """This function forces the slider to show only integer values.

        Args:
            value: Value of the slider
        """
        self.newvalue = min(self.slidervaluelist, key=lambda x:abs(x-float(value)))
        self.labeletape2.configure(text = self.newvalue)

    def close_window(self):
        """This function closes the window.
        """
        self.master.destroy()

class Options:
    """This class contains the options menu of the program. Once it is launched, the main window of the program is disabled to avoid mistakes.
    """
    def __init__(self, master):
        self.master = master
        self.master.attributes("-topmost", True)
        self.master.title("Paramètres")
        self.master.resizable(0, 0)
        width = 250
        height = 500
        center_window_on_screen(self.master, width, height)

        self.tabview = ctk.CTkTabview(self.master, width = width, height = height, fg_color = self.master._fg_color)
        self.tabview.add("Général")
        self.tabview.add("Images")
        self.tabview.set("Général")

        self.frame = ctk.CTkFrame(self.tabview.tab("Général"), width = width, height = height-100, fg_color = self.master._fg_color)
        self.frame.pack_propagate(False)
        self.darkModeFrame = ctk.CTkFrame(self.frame, fg_color = self.frame._fg_color)
        self.defaultFrame = ctk.CTkFrame(self.frame, fg_color = self.frame._fg_color)
        self.bottomFrame = ctk.CTkFrame(self.tabview.tab("Général"), width = width, height = height-self.frame._current_height, fg_color = self.master._fg_color)
        self.frame.pack_propagate(False)

        config = ConfigParser()
        config.read(resource_path(os.path.join('cfg','config.ini')))

        self.label0 = ctk.CTkLabel(self.frame, text = "Algorithme génétique\n---", font=("Helvetica", 18))
        self.label0.pack()
        self.label1 = ctk.CTkLabel(self.frame, text = "Moyenne :", font=("Helvetica", 16))
        self.label1.pack()
        self.label2 = ctk.CTkLabel(self.frame, text = f"{float(config['current']['mean'])}", font=("Helvetica", 14))
        self.label2.pack()
        self.slider1 = ctk.CTkSlider(self.frame, from_ = 0, to = 10, number_of_steps = 40, command = self.slider1)
        self.slider1.set(float(config['current']['mean']))
        self.slider1.pack()
        self.label3 = ctk.CTkLabel(self.frame, text = "Variance :", font=("Helvetica", 16))
        self.label3.pack()
        self.label4 = ctk.CTkLabel(self.frame, text = f"{float(config['current']['variance'])}", font=("Helvetica", 14))
        self.label4.pack()
        self.slider2 = ctk.CTkSlider(self.frame, from_ = 0, to = 5, number_of_steps = 20, command = self.slider2)
        self.slider2.set(float(config['current']['variance']))
        self.slider2.pack()
        self.label5 = ctk.CTkLabel(self.frame, text = "---", font=("Helvetica", 18))
        self.label5.pack()

        self.imgMode = Image.open(resource_path(os.path.join('img','mode.png')))
        self.imageMode = ctk.CTkImage(self.imgMode, self.imgMode, (50,50))
        self.imgLabel = ctk.CTkLabel(self.darkModeFrame, text = None, image = self.imageMode)
        self.imgLabel.pack(side = "left", padx = 15)

        if int(config['current']['dark_mode']) == 1:
            self.switch_var = ctk.StringVar(value="on")
        else:
            self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(self.darkModeFrame, text="Dark mode", command = self.switch_event, font=("Helvetica", 14),
                                        variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.pack(side = "left")

        self.defaultButton = ctk.CTkButton(self.defaultFrame, text = "Réinitialiser", width = 25, command = lambda: self.reset_config(config), font=("Helvetica", 16))
        self.defaultButton.configure(fg_color = 'firebrick3', hover_color = 'firebrick4')
        self.defaultButton.pack(pady = 30)

        self.aboutButton = ctk.CTkButton(self.defaultFrame, text = "À propos", width = 25, command = self.about, font=("Helvetica", 16))
        self.aboutButton.pack()

        self.NButton = ctk.CTkButton(self.bottomFrame, text = "Annuler", width = 25, command = lambda: self.cancel_changes(config), font=("Helvetica", 16))
        self.NButton.pack(side = "left", padx = 20)
        self.OKButton = ctk.CTkButton(self.bottomFrame, text = "Valider", width = 25, command = lambda: self.validate_params(config), font=("Helvetica", 16))
        self.OKButton.pack(side = "right", padx = 20)

        self.pathIntroLabel = ctk.CTkLabel(self.tabview.tab("Images"), text = "Chemin actuel", font=("Helvetica", 18))
        self.pathIntroLabel.pack(pady = 20)

        if 'saved_images_path' in config['current']:
            self.pathLabel = ctk.CTkLabel(self.tabview.tab("Images"), text = f"{config['current']['saved_images_path']}", font=("Helvetica", 16), wraplength = 200)
            self.pathLabel.pack()
            self.pathButton = ctk.CTkButton(self.tabview.tab("Images"), text = "Changer le chemin", width = 200, command = self.change_path_label, font=("Helvetica", 16))
            self.pathButton.pack(pady = 10)
        else:
            self.pathLabel = ctk.CTkLabel(self.tabview.tab("Images"), text = "Aucun chemin sélectionné", font=("Helvetica", 16))
            self.pathLabel.pack()
            self.pathButton = ctk.CTkButton(self.tabview.tab("Images"), text = "Définir un chemin", width = 200, command = self.change_path_label, font=("Helvetica", 16))
            self.pathButton.pack(pady = 10)
        
        self.NPathButton = ctk.CTkButton(self.tabview.tab("Images"), text = "Annuler", width = 25, command = lambda: self.cancel_changes(config), font=("Helvetica", 16))
        self.NPathButton.pack(side = "left", padx = 20)
        self.OKPathButton = ctk.CTkButton(self.tabview.tab("Images"), text = "Valider", width = 25, command = lambda: self.validate_path_change(config = config, label_string = self.pathLabel.cget("text")), font=("Helvetica", 16))
        self.OKPathButton.pack(side = "right", padx = 20)

        self.tabview.pack()
        self.frame.pack()
        self.darkModeFrame.pack()
        self.defaultFrame.pack(pady = 10)
        self.bottomFrame.pack(side = "bottom", pady = 10)
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.cancel_changes(config))
        self.master.wait_visibility()
        self.master.grab_set()
    
    def switch_event(self):
        """This function changes the mode to light if it was dark, or dark if it was light.
        """
        if (self.switch_var.get() == "on"):
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("dark-blue")
            self.defaultButton.configure(fg_color = 'firebrick3', hover_color = 'firebrick4')
            self.master.after(10, self.master.focus)
        else:
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")
            self.defaultButton.configure(fg_color = 'firebrick2', hover_color = 'firebrick3')
            self.master.after(10, self.master.focus)
        self.master.update()

    def slider1(self, value):
        """This function changes the value showed above the mean slider according to where the cursor is.

        Args:
            value: Value of the cursor
        """
        self.label2.configure(text = value)

    def slider2(self, value):
        """This function changes the value showed above the variance slider according to where the cursor is.

        Args:
            value: Value of the cursor
        """
        self.label4.configure(text = value)

    def cancel_changes(self, config):
        """This function cancels the changes that happened in the options menu when the user clicks on "Annuler" or closes the options window.
        It also closes the window and makes the main windows usable again.

        Args:
            config: Configuration file used to come back to the previous values
        """
        if int(config['current']['dark_mode']) == 1:
            self.switch_var.set('on')
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("dark-blue")
        else:
            self.switch_var.set('off')
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")
        
        config.set('current', 'mean', config['current']['mean'])
        self.label2.configure(text = config['current']['mean'])
        self.slider1.set(float(config['current']['mean']))

        config.set('current', 'variance', config['current']['variance'])
        self.label4.configure(text = config['current']['variance'])
        self.slider2.set(float(config['current']['variance']))

        self.master.grab_release()
        self.master.destroy()
    
    def validate_params(self, config):
        """This function writes the parameters entered by the user in the config file, section [current], which validates them and uses them for the rest of the execution and the other executions.
        It also closes the window and makes the main windows usable again.

        Args:
            config: Configuration file used to write the parameters
        """
        if self.switch_var.get() == 'on':
            config.set('current', 'dark_mode', '1')
        else:
            config.set('current', 'dark_mode', '0')
        
        config.set('current', 'mean', f"{self.slider1.get()}")
        config.set('current', 'variance', f"{self.slider2.get()}")
        
        with open(resource_path(os.path.join('cfg','config.ini')), 'w') as conf:
            config.write(conf)

        self.master.grab_release()
        self.master.destroy()
    
    def reset_config(self, config):
        """This function reinitializes the parameters to the very first ones, according to the [initial] section of the config.ini file.
        It also closes the window and makes the main windows usable again.

        Args:
            config: Configuration file used to read the initial parameters.
        """
        config.set('current', 'dark_mode', config['initial']['dark_mode'])
        self.switch_var.set('on')
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        config.set('current', 'mean', config['initial']['mean'])
        self.label2.configure(text = config['initial']['mean'])
        self.slider1.set(float(config['initial']['mean']))

        config.set('current', 'variance', config['initial']['variance'])
        self.label4.configure(text = config['initial']['variance'])
        self.slider2.set(float(config['initial']['variance']))

        with open(resource_path(os.path.join('cfg','config.ini')), 'w') as conf:
            config.write(conf)
        
        tk.messagebox.showinfo(parent=self.master, title="Felon Finder", message="Paramètres réinitialisés.")
        self.master.grab_release()
        self.master.destroy()
    
    def about(self):
        """This function opens a pop-up message with the authors and specials thanks.
        """
        tk.messagebox.showinfo(parent=self.master, title="Felon Finder", message="Felon Finder - 2024\nMade with ❤️ by :\n\n- LAYOUS Alexandre\n- SALEK Chada\n- ZARKUA Audrey\n\nSpecial thanks to :\n\n- PEIGNIER Sergio\n- TROMBETTA Robin\n- RIGOTTI Christophe")
    
    def change_path_label(self):
        """This function changes the path to the saved images if the user enters one.
        """
        given_path = filedialog.askdirectory(parent = self.master, title = "Nouveau chemin d'accès")
        if given_path:
            self.pathLabel.configure(text = f"{given_path}", wraplength = 200)
            self.pathButton.configure(text = "Changer le chemin")
    
    def validate_path_change(self, label_string, config):
        """This function validates the path changes by putting the new path in the config.ini file if one was selected.
        It also closes the window and makes the main windows usable again.

        Args:
            label_string: Value of the path string
            config: ConfigParser object used to write the new configuration
        """
        if label_string != "Aucun chemin sélectionné":
            config.set('current', 'saved_images_path', label_string)
            with open(resource_path(os.path.join('cfg','config.ini')), 'w') as conf:
                config.write(conf)
            config.read(resource_path(os.path.join('cfg','config.ini')))
        
        self.master.grab_release()
        self.master.destroy()

class Tutorial:
    """This class contains the tutorial window with a link to the github repository of the project.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Felon Finder - Mode d'emploi")
        self.master.resizable(0, 0)
        width = 600 
        height = 650
        center_window_on_screen(self.master, width, height)

        self.topFrame = ctk.CTkFrame(self.master, width = width, fg_color = self.master._fg_color)
        self.linkFrame = ctk.CTkFrame(self.master, width = width, fg_color = self.master._fg_color)
        self.bottomFrame = ctk.CTkFrame(self.master, width = width, fg_color = self.master._fg_color)

        self.labelTitle = ctk.CTkLabel(self.topFrame, text="Felon Finder - Tutoriel", font=("Helvetica", 24))
        self.labelTitle.pack(pady=20)

        self.labelIntroTitle = ctk.CTkLabel(self.topFrame, text="Introduction", font=("Helvetica", 18))
        self.labelIntroTitle.pack()
        self.labelIntro = ctk.CTkLabel(self.topFrame, text="Bienvenue dans le tutoriel de FELON FINDER !\n\n"
                                           "Cette application a pour objectif de faciliter la reconnaissance\n"
                                           "d'un potentiel agresseur en produisant des portraits robots.", font=("Helvetica", 16))
        self.labelIntro.pack(pady = 20)

        self.labelPrincipleTitle = ctk.CTkLabel(self.topFrame, text="Principe", font=("Helvetica", 18))
        self.labelPrincipleTitle.pack()
        self.labelPrinciple = ctk.CTkLabel(self.topFrame, text="En lançant FELON FINDER, quatre images aléatoirement choisies\n"
                                           "de notre base de données sont proposées à l’utilisateur.\n\n"
                                           "Ce dernier sélectionne les images les plus ressemblantes.\n"
                                           "Il peut choisir une à quatre photos à chaque fois.\n\n"
                                           "Les images sélectionnées sont ensuite traitées afin de produire quatre\n"
                                           "nouveaux portraits robots se rapprochant de plus en plus de l’agresseur.\n\n"
                                           "Si certains portraits conviennent à l'utilisateur, il peut les enregistrer.", font=("Helvetica", 16))
        self.labelPrinciple.pack(pady = 20)

        self.labelGuide = ctk.CTkLabel(self.linkFrame, text="Pour le guide complet et la f.a.q, cliquez ci-dessous :", font=("Helvetica", 18))
        self.labelGuide.pack()
        self.linkFont = ctk.CTkFont("Helvetica", 18)
        self.link = ctk.CTkLabel(self.linkFrame, text="https://github.com/AlexandreLayous/felon-finder", font=self.linkFont, cursor = "hand2", text_color="blue2")
        self.link.pack()
        self.link.bind("<Enter>", lambda e: self.underline_and_darken_link())
        self.link.bind("<Leave>", lambda e: self.cancel_link_underline())
        self.link.bind("<Button-1>", lambda e: self.callback("https://github.com/AlexandreLayous/felon-finder"))

        self.quitButton = ctk.CTkButton(self.bottomFrame, text = "C'est compris !", width = 30, command = self.close_window)
        self.quitButton.pack()

        self.topFrame.pack()
        self.linkFrame.pack(pady = 20)
        self.bottomFrame.pack(pady = 20)

    def close_window(self):
        """This function closes the window.
        """
        self.master.destroy()
    
    def callback(self, url):
        """This function opens a new tab in the user's web browser to the github repository of the project.

        Args:
            url: Link of the github repository
        """
        webbrowser.open_new_tab(url)
    
    def underline_and_darken_link(self):
        """This function underlines and darkens the link label when the user hovers over it.
        """
        self.linkFont.configure(underline = True)
        self.link.configure(text_color = "blue3")
    
    def cancel_link_underline(self):
        """This function removes the underlining and makes the link label a bit brighter when the user stops hovering over it.
        """
        self.linkFont.configure(underline = False)
        self.link.configure(text_color = "blue2")

def create_root_closing_handler(root):
    """This function asks for the user's confirmation to close the program.

    Args:
        root: Main window of the program.
    """
    def on_closing():
        if tk.messagebox.askokcancel("Fermeture", "Vous allez fermer le programme. Continuer ?"):
            root.destroy()
    return on_closing

def center_window_on_screen(window, width, height):
    """This function centers the given window on the screen with the given width and height.

    Args:
        window: Window to be centered
        width: Width to be given to the window
        height: Height to be given to the window
    """
    window.update_idletasks()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))

def main():
    """This function launches the loading splash screen for the program.
    """
    splash_screen = ctk.CTk()
    SplashScreen(splash_screen)
    splash_screen.mainloop()

if __name__ == '__main__':
    main()
