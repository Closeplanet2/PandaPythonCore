from tkinter import Tk, Entry, StringVar, Label, Button, OptionMenu
from selenium.webdriver.common.by import By
from PIL import ImageTk, Image
from selenium import webdriver
from bs4 import BeautifulSoup
import threading
import requests
import urllib3
import time
import json
import os

'''Class controls allows the creation of tkinter windows. It also double buffers the windows so that the new window is created and then replaces the first window!'''
class TKinterController:
    '''Create the class with the properties needed to create the first window! [title: the title of the window!], [height: height of the window!], [width: width of the window!],
        [rs_height: resize height!], [rs_width: resize width!], [background_color: background color or window]'''
    def __init__(self, title, height, width, rs_height, rs_width, background_color):
        self.first_window = BlankGUI(title, height, width, rs_height, rs_width, background_color)
        self.second_window = None
        self.extra_screens = []

    '''Create the class with the properties needed to create the second window! This overrides the second window! Overide windows control if the new window overrides the first one!
        [title: the title of the window!], [height: height of the window!], [width: width of the window!], [rs_height: resize height!], [rs_width: resize width!], 
        [background_color: background color or window]'''
    def create_window(self, title, height, width, rs_height, rs_width, background_color, override_window=True):
        if not override_window:
            self.extra_screens.append(BlankGUI(title, height, width, rs_height, rs_width, background_color))
            return

        self.second_window = BlankGUI(title, height, width, rs_height, rs_width, background_color)
        if not self.first_window is None:
            self.first_window.withdraw()
        self.second_window.deiconify()

    '''Return the active window!'''
    def return_active_window(self):
        return self.first_window

'''Class controls allows the actual screen of the gui. Functions allow for widgets to be added to the display!'''
class BlankGUI(Tk):
    '''Create the class with the properties needed to create the first window! [title: the title of the window!], [height: height of the window!], [width: width of the window!],
        [rs_height: resize height!], [rs_width: resize width!], [background_color: background color or window]'''
    def __init__(self, title, height, width, rs_height, rs_width, background_color):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(width=rs_width, height=rs_height)
        self.configure(bg=background_color)
        self.destruciton_prevention = []

    '''Add Entry Field To Window! [text: placeholder text and defines widget name], [posx / posy: position the widget on the screen!], [width: width of the widget!], 
        [callback_class: class to find the callback function in! function in the class needs to be the name of the widget in lower and replace spaces with _]'''
    def add_entry_field(self, text, posx=0, posy=0, width=10, callback_class=None):
        widget_name = f"{text.lower().replace(' ', '_')}"
        textvariable = StringVar()
        callback_function = None if callback_class is None else getattr(callback_class, widget_name)
        textvariable.trace("w", lambda name, index, mode, var=textvariable: callback_function(textvariable))

        entry_field = Entry(text=text) if callback_function is None else Entry(text=text, textvariable=textvariable)
        entry_field.config(width=width)
        entry_field.place(x=posx, y=posy)
        return entry_field

    '''Add Image To Window! [image_path: define the path to the image], [posx / posy: position the widget on the screen!], [width / height: width and height of the widget!]'''
    def add_image(self, image_path, posx=0, posy=0, width=10, height=10):
        card_image = Image.open(image_path)
        card_image = card_image.resize((width, height))
        render = ImageTk.PhotoImage(card_image)
        label = Label(self, image=render)
        label.image = render
        label.place(x=posx, y=posy)
        return label

    '''Add Button To Window!  [text: placeholder text and defines widget name], [posx / posy: position the widget on the screen!], [width / height: width and height of the widget!],
        [callback_class: class to find the callback function in! function in the class needs to be the name of the widget in lower and replace spaces with _], 
        [args: what will be passed through the function], [bg: background color], [fg: text color]'''
    def add_button(self, text, posx=0, posy=0, width=10, height=10, callback_class=None, args=None, bg="#FF5733", fg='#E0E0E0'):
        widget_name = f"{text.lower().replace(' ', '_')}"
        textvariable = StringVar()
        callback_function = None if callback_class is None else getattr(callback_class, widget_name)
        textvariable.trace("w", lambda name, index, mode, var=textvariable: callback_function(textvariable))

        button = Button(self, text=text, bg=bg, fg=fg) if callback_function is None else Button(self, text=text, command=lambda: callback_function(args), bg=bg, fg=fg)
        button.config(width=width, height=height)
        button.place(x=posx, y=posy)
        return button

    '''Add Dropdown To Window! [text: placeholder text and defines widget name], [posx / posy: position the widget on the screen!], [width / height: width and height of the widget!],
        [callback_class: class to find the callback function in! function in the class needs to be the name of the widget in lower and replace spaces with _], [options: options for the dropdown]'''
    def add_dropdown(self, text, posx=0, posy=0, width=10, height=10, callback_class=None, options=None):
        widget_name = f"{text.lower().replace(' ', '_')}"
        textvariable = StringVar()
        callback_function = None if callback_class is None else getattr(callback_class, widget_name)
        textvariable.set(options[0])
        textvariable.trace("w", lambda name, index, mode, var=textvariable: callback_function(textvariable))

        options_menu = OptionMenu(self, textvariable, *options)
        options_menu.place(x=posx, y=posy)
        options_menu.config(width=width, height=height)
        return options_menu

    '''Add Text To Window! [text: placeholder text and defines widget name], [Font size / Font type: size and type of font], [posx / posy: position the widget on the screen!], 
        [text_color: text color!], [background_color: Background color]'''
    def add_text(self, text, font_type, font_size, posx, posy, text_color, background_color):
        label = Label(self, text=text, font=(font_type, font_size), fg=text_color, bg=background_color)
        label.place(x=posx, y=posy)
        return label

    '''Prevent the destruction on clear of the widgets passed through!'''
    def prevent_destruction(self, *widgets):
        for widget in widgets:
            widget_name = str(widget)
            print(f"Wont be destroyed: {widget_name}")
            self.destruciton_prevention.append(widget_name)

    '''Clear the gui of the current screen!'''
    def clear_gui(self):
        for widget in self.winfo_children():
            if not str(widget) in self.destruciton_prevention:
                widget.destroy()

'''Class to control the request functions'''
class RequestController:
    '''download image from [image_url] to [save_path]! set verify to True / False'''
    def download_image(self, image_url, save_path, verify=True):
        pull_image = requests.get(image_url, verify=verify)
        with open(save_path, 'wb') as handler:
            handler.write(pull_image.content)

    '''using request pull website! use_beautiful_soup = True/False, sleep=sleep time'''
    def pull_website(self, webpage_url, use_beautiful_soup=False, sleep=1):
        webpage = requests.get(webpage_url)
        if use_beautiful_soup:
            time.sleep(sleep)
            return BeautifulSoup(webpage.content, 'html.parser')
        else:
            return webpage

'''Class to control the website functions'''
class WebsiteController:
    '''Instialise the wbesite controller: full_screen: if the window is full screen, executable_path: path to chrome driver if wanting to use own!'''
    def __init__(self, full_screen=False, executable_path='C:\chromedriver\chromedriver.exe'):
        self.chrome_driver = webdriver.Chrome(executable_path=executable_path)
        if full_screen:
            self.chrome_driver.maximize_window()
        urllib3.disable_warnings()

    '''search the current webpage in the chrome driver'''
    def return_webpage(self, webpage_url, sleep=1):
        self.chrome_driver.get(webpage_url)
        time.sleep(sleep)
        return self.update_webpage()

    '''return element from class name or id name!'''
    def return_element(self, class_name=None, id_name=None):
        if not class_name is None:
            return self.chrome_driver.find_element(By.CLASS_NAME, class_name)
        else:
            return self.chrome_driver.find_element(By.ID, id_name)

    '''click the element of chrome driver by returning element by class name or id name'''
    def click_element(self, class_name=None, id_name=None, sleep=1):
        self.return_element(class_name, id_name).click()
        time.sleep(sleep)
        return self.update_webpage()

    '''send keys to element by returning element by class name or id name'''
    def send_keys_to_element(self, input_value, class_name=None, id_name=None, sleep=1):
        self.return_element(class_name, id_name).send_keys(input_value)
        time.sleep(sleep)
        return self.update_webpage()

    '''clear element by returning element by class name or id name'''
    def clear_element(self, class_name=None, id_name=None, sleep=1):
        self.return_element(class_name, id_name).clear()
        time.sleep(sleep)
        return self.update_webpage()

    '''update the webpage'''
    def update_webpage(self):
        return BeautifulSoup(self.chrome_driver.page_source, "html.parser")

'''Claass to control os file and directory operations'''
class FileDirectoryController:
    '''Open file in the given application that is located in dir_path with name file_name'''
    def open_file(self, dir_path, file_name, application):
        osCommandString = f"{application} {dir_path}/{file_name}"
        os.system(osCommandString)

    '''Check if given file of file_name exists in dir dir_path'''
    def does_path_exist(self, dir_path, file_name):
        return os.path.exists(f"{dir_path}/{file_name}")

    '''create dir of dir_path'''
    def create_directory(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    '''create file in given dir of dir_path with name file_name'''
    def create_file(self, dir_path, file_name):
        self.create_directory(dir_path)
        if not os.path.exists(f"{dir_path}/{file_name}"):
            open(f"{dir_path}/{file_name}", "w").close()

    '''try to create file and return file for reading'''
    def read_and_write_file(self, dir_path, file_name):
        self.create_file(dir_path, file_name)
        return open(f"{dir_path}/{file_name}",'r')

    '''is the given file in dir dir_path with name file_name empty'''
    def is_file_empty(self, dir_path, file_name):
        return os.stat(f"{dir_path}/{file_name}").st_size == 0

    '''is the given dir dir_path empty'''
    def is_dir_empty(self, dir_path):
        return not os.listdir(dir_path)

    '''count the files in dir dir_path'''
    def count_files_in_dir(self, dir_path):
        return len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])

    '''delete the file with name file_name in dir dir_path'''
    def delete_file(self, dir_path, file_name):
        if os.path.exists(f"{dir_path}/{file_name}"):
            os.remove(f"{dir_path}/{file_name}")

    '''delete the file with name file_name in dir dir_path then recreate file'''
    def delete_and_write_file(self, dir_path, file_name):
        self.delete_file(dir_path, file_name)
        self.write_file(dir_path, file_name)

    '''write array list to file with name file_name in dir dir_path'''
    def write_array_to_file(self, dir_path, file_name, list):
        self.write_file(dir_path, file_name)
        with open(f"{dir_path}/{file_name}", 'w') as data_file:
            for item in list:
                data_file.write(f"{item}\n")

    '''read array list to file with name file_name in dir dir_path'''
    def read_array_from_file(self, dir_path, file_name):
        self.write_file(dir_path, file_name)
        data = []
        with open(f"{dir_path}/{file_name}", 'r') as data_file:
            for line in data_file:
                data.append(line.replace("\n", ""))
        return data

'''Class to control the json operations'''
class JSONController:
    '''Download webpage webpage_url to file file_name in dir dir_path! if the data needs external key, use external_key'''
    def dump_webpage_to_json(self, dir_path, file_name, webpage_url, external_key=None):
        external_webpage = RequestController().pull_website(webpage_url=webpage_url)
        json_webpage = json.loads(external_webpage.text)
        if not external_key is None:
            json_webpage = json.loads(external_webpage.text)[external_key]
        self.dump_dict_to_json(dir_path, file_name, json_webpage)

    '''dump dict / array dict to file with name file_name in dir dir_path'''
    def dump_dict_to_json(self, dir_path, file_name, dict):
        with open(f"{dir_path}/{file_name}", 'w') as data_file:
            json.dump(dict, data_file)

    '''load dict / array dict to file with name file_name in dir dir_path'''
    def load_json(self, dir_path, file_name):
        with open(f"{dir_path}/{file_name}", "r") as data_file:
            return json.load(data_file)

'''Class to control the threading'''
class ThreadController:
    '''instalise the class with the maxium number of threads'''
    def __init__(self, thread_max):
        self.thread_max = thread_max
        self.loaded_threads = []

    '''Start the threads calling upon the given method with the arguments args! 
        This function also starts all threads and waits for all threads to finish'''
    def start_load_wait(self, method, *args):
        self.load_threads(method, args)
        self.start_all_threads()
        self.wait_for_all_threads()

    '''Load thread of method passing args of max threads! THIS FUNCTION DOESN'T START THE THREADS'''
    def load_threads(self, method, *args):
        for index in range(0, self.thread_max, 1):
            self.loaded_threads.append(threading.Thread(target=method, args=(args,)))

    '''Start all the threads loaded in load_threads! start_load_wait is main command'''
    def start_all_threads(self):
        for thread in self.loaded_threads:
            thread.start()

    '''Wait all the threads loaded in load_threads! start_load_wait is main command'''
    def wait_for_all_threads(self):
        for thread in self.loaded_threads:
            thread.join()

'''Class with helpful functions for variables'''
class VariableController:
    def return_lowest_value_in_dict(self, dict):
        target = float('inf')
        for key in dict:
            if dict[key] < target:
                target = dict[key]
        return target

    def return_all_keys_of_value(self, dict, value):
        keys = []
        for sub_key in dict:
            if dict[sub_key] == value:
                keys.append(sub_key)
        return keys

'''Class to control the yugioh data'''
class YgoproController:
    def __init__(self):
        self.ygopro_data = JSONController().load_json("Data/Ygodata", "YgoproData.json")

    '''download all the card images'''
    def download_all_images_thread(self, thread_id):
        FileDirectoryController().create_directory("Data/Ygodata/Images")
        for i in range(thread_id, len(self.ygopro_data)):
            card = list(self.ygopro_data)[i]
            if not FileDirectoryController().does_path_exist("Data/Ygodata/Images", f"{card['id']}.jpg"):
                RequestController().download_image(card['card_images'][0]['image_url'], f"Data/Ygodata/Images/{card['id']}.jpg")
            print(f"{i}/{len(self.ygopro_data)}")

    '''Return card by card id'''
    def FindCardByID(self, id):
        scrubbedid = self.ScrubID(int(id))
        for card in self.ygopro_data:
            if card['id'] == scrubbedid:
                return card
        return None

    '''Return card by id and error check if null'''
    def FindCardIDNullCheck(self, id):
        find_card = self.FindCardByID(id)
        if find_card is None:
            print(f"Card Is Null: {id}")
        return find_card

    '''Return card by card name'''
    def FindCardByName(self, name):
        for card in self.ygopro_data:
            if card['name'] == name:
                return card
        return None

    '''Scrub the card id as some of the data from ygopro api is currupt!'''
    def ScrubID(self, theirid):
        if theirid == 83011277:
            return 83011278
        if theirid == 83555667:
            return 7852509
        if theirid == 84080938:
            return 84080939
        if theirid == 18807108:
            return 18807109
        if theirid == 36996508:
            return 38033121
        if theirid == 73134081:
            return 73134082
        if theirid == 19230407:
            return 19230408
        if theirid == 16195943:
            return 16195942
        if theirid == 83764718:
            return 83764719
        if theirid == 6150045:
            return 6150044
        if theirid == 57116034:
            return 57116033
        if theirid == 39751093:
            return 39751094
        if theirid == 81480460:
            return 81480461
        if theirid == 77585514:
            return 77585513
        if theirid == 27847700:
            return 24094653
        if theirid == 44508095:
            return 44508094
        return theirid