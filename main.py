import time
import os
from kivy.app import App
from kivy.core.text import Label
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
import pyttsx3
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.clock import Clock
from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2
from kivy.uix.image import Image
from yolo import YOLOv8
import kivy
from roboflow import Roboflow


#Global Attributes
Window.size = (360, 700)
global screen_manager
screen_manager = ScreenManager()


class CustomBoxLayout(MDBoxLayout):
    pass

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.image_display = Image()
        #self.engine = pyttsx3.init()

        # Initialize total currency to 0
        self.totalCurrency = 0

        # ... (other initialization code)

    def process_image(self, image_path):
        # Load the image from the specified file path
        image = Image(source=image_path)
        sum = 0;

        try:
            rf = Roboflow(api_key="YPZEe8CxS14cOZgHKv7Y")
            #rf = Roboflow(api_key="ZwrzpZk6j81HyJSPVMps")
            #project = rf.workspace().project("moneydetector")
            #dataset = project.version(1).download("yolov5-obb")
            project = rf.workspace().project("moneycounter-4qp4a")
            model = project.version(2).model

            # infer on a local image
            response = model.predict(image_path, confidence=40, overlap=30).json()

            print(model.predict(image_path, confidence=40, overlap=30).json())

            # Process the prediction results
            for pred in response['predictions']:
                if pred['class'] == "One Thousand":
                    sum = sum + 1000;
                if pred['class'] == "Five Hundred":
                    sum = sum + 500;
                if pred['class'] == "Two Hundred":
                    sum = sum + 200;
                if pred['class'] == "One Hundred":
                    sum = sum + 100;
                if pred['class'] == "Fifty":
                    sum = sum + 50;
                if pred['class'] == "Twenty":
                    sum = sum + 20;
                if pred['class'] == "Ten":
                    sum = sum + 10;
                if pred['class'] == "Five":
                    sum = sum + 5;
                if pred['class'] == "One":
                    sum = sum + 1;

            self.totalCurrency = sum
            #for pred in response['predictions']:
                #currency_class = pred['class']
                #currency_value = self.get_currency_value(currency_class)
                #self.totalCurrency += currency_value

            # Update the screen to display the image and total currency
            self.ids.image_display.source = image_path
            self.update_currency_label()

            # Speak the total currency
            #self.convert_to_speak(self.totalCurrency)

        except Exception as e:
            # Handle exceptions, you might want to show an error message on the screen
            print(f"Error processing image: {e}")

    def get_currency_value(self, currency_class):
        # Define a mapping of currency classes to their values
        currency_values = {
            "One Thousand": 1000,
            "Five Hundred": 500,
            "Two Hundred": 200,
            "One Hundred": 100,
            "Fifty": 50,
            "Twenty": 20,
            "Ten": 10,
            "Five": 5,
            "One": 1,
        }
        return currency_values.get(currency_class, 0)

    def update_currency_label(self):
        # Display the total currency on the screen
        #currency_label = Label(text={self.totalCurrency})
        total_currency_label = self.ids.totalCurrency
        if self.totalCurrency == 0:
            self.fontSize = 38
            total_currency_label.text = f"No detected Money"
        else:
            total_currency_label.text = f"{self.totalCurrency} PESOS"

    #def convert_to_speak(self, totalCurrency):
        #def speak(command):
            #self.engine.say(command)
            #self.engine.runAndWait()

        #speak(totalCurrency)
class CaptureScreen(Screen):
    def __init__(self, **kwargs):
        super(CaptureScreen, self).__init__(**kwargs)

        self.mycamera = self.ids.camera
        self.myimage = Image()

    def capture(self):
        outputFolder = 'Image'
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        timenow = time.strftime("%Y%m%d_%H%M%S")

        #self.mycamera.export_to_png("myimage_{}.png".format(timenow))

        # Capture the image from the camera
        #self.mycamera.export_to_png(os.path.join(outputFolder, "myimage_{}.png".format(timenow)))
        #self.myimage.source = "myimage_{}.png".format(timenow)
        # Capture the image from the camera
        image_path = os.path.join(outputFolder, "myimage_{}.png".format(timenow))
        self.mycamera.export_to_png(image_path)

        self.myimage.source = image_path

        # Switch to ResultPage and pass the image path
        self.manager.current = 'resultScreen'
        self.manager.get_screen('resultScreen').process_image(image_path)

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        self.engine = pyttsx3.init()

    # Volume
    def vol(self, value):
        self.engine.setProperty("volume", value)


class HomeScreen(Screen):
    pass

class WelcomePage(Screen):
    pass

class TapAndListen(MDApp):

    bg_color = ObjectProperty([0, .2784, .2431, 1])
    bar_color = ObjectProperty([1, 1, 1, 1])
    slider_thumb_color = ObjectProperty([0.980, 1, 0, 1])
    slider_color = ObjectProperty([0.980, 1, 0, 1])
    settings_box_color = ObjectProperty([0, 0, 0, 1])
    fontSize = ObjectProperty(40)
    result_card_color = ObjectProperty([0, 1, 0.87450980392, 1])
    font_color_result = ObjectProperty([0.98039215686, 1, 0, 1])
    engine = pyttsx3.init()

    def build(self):
        Builder.load_file('userinterface.kv')

        self.home_screen = HomeScreen(name='homeScreen')
        self.settings_screen = SettingsScreen(name='settingsScreen')
        self.capture_screen = CaptureScreen(name='captureScreen')
        self.welcome_screen = WelcomePage(name='welcomePage')
        self.result_screen = ResultScreen(name='resultScreen')

        screen_manager.add_widget(self.home_screen)
        screen_manager.add_widget(self.settings_screen)
        screen_manager.add_widget(self.capture_screen)
        screen_manager.add_widget(self.welcome_screen)
        screen_manager.add_widget(self.result_screen)

        return screen_manager

    def on_start(self):
        screen_manager.current = "welcomePage"

    def convert_to_speak(self, totalCurrency):
        def speak(command):
            self.engine.say(command)
            self.engine.runAndWait()

        speak(totalCurrency)

    def normal_color(self):
        app = App.get_running_app()

        self.bg_color = [0, .2784, .2431, 1]
        self.bar_color = [1, 1, 1, 1]
        self.slider_color = [0.980, 1, 0, 1]
        self.slider_thumb_color = [0.980, 1, 0, 1]
        self.settings_box_color = [0, 0, 0, 1]
        self.result_card_color = [0, 1, 0.87450980392, 1]
        self.font_color_result = [0.98039215686, 1, 0, 1]

        #Home_Screen
        app.home_screen.ids.capture_img.source = "Assets/Icons/Capture Button (1).png"
        app.home_screen.ids.settings_img.source = "Assets/Icons/Settings Button (1).png"
        app.home_screen.ids.homePage_img.source = "Assets/Icons/HOME PAGE.png"

        #Capture_Screen
        app.capture_screen.ids.backC_img.source = "Assets/Icons/Back Button.png"
        app.capture_screen.ids.flashButton_img.source = "Assets/Icons/Flash Button.png"
        app.capture_screen.ids.repeat_img.source = "Assets/Icons/Repeat Button.png"
        app.capture_screen.ids.capturePage_img.source = "Assets/Icons/CAPTURE PAGE.png"
        app.capture_screen.ids.tapCapture.source = "Assets/Icons/DOUBLE TAP TO CAPTURE.png"


        #Settings_Screen
        app.settings_screen.ids.settingsPage_img.source = "Assets/Icons/SETTINGS PAGE.png"
        app.settings_screen.ids.back_img.source = "Assets/Icons/Back Button.png"
        app.settings_screen.ids.fontSizeNote_img.source = "Assets/Icons/Font size notes.png"
        app.settings_screen.ids.soundVolumeNote_img.source = "Assets/Icons/Sound volume note.png"
        app.settings_screen.ids.contrastNote_img.source = "Assets/Icons/Contrast note.png"
        app.settings_screen.ids.fontSize_img.source = "Assets/Icons/Font size.png"
        app.settings_screen.ids.soundVolume_img.source = "Assets/Icons/Volume.png"
        app.settings_screen.ids.contrast_img.source = "Assets/Icons/Contrast.png"
        app.settings_screen.ids.normal.source = "Assets/Icons/Normal Button.png"
        app.settings_screen.ids.high_contrast.source = "Assets/Icons/High Contrast.png"
        app.settings_screen.ids.invert.source = "Assets/Icons/Invert Colors.png"
        app.settings_screen.ids.grayscale.source = "Assets/Icons/Grayscale.png"

        if (app.settings_screen.ids.forty.source == "Assets/Icons/40 pt.png" or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt High.png"
                or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt Gray.png" or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt invert normal.png"
                or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt Invert.png"):

            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt.png"

        elif (app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt normal clicked.png" or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt high clicked.png"
              or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt invert normal clicked.png" or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt invert high clicked.png"
              or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt grayscale clicked.png"):

            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt normal clicked.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt.png"

        elif (app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt normal clicked.png" or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt high clicked.png"
              or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt imvert normal clicked.png" or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt invert high clicked.png"
              or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt grayscale clicked.png"):

            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt normal clicked.png"

        #Result page
        app.result_screen.ids.capturePage_img.source = "Assets/Icons/RESULT PAGE.png"
        app.result_screen.ids.detected_currency.source = "Assets/Icons/DETECTED CURRENCIES.png"
        app.result_screen.ids.total_currency.source = "Assets/Icons/Total Currency.png"
        app.result_screen.ids.homeButton_img.source = "Assets/Icons/Home Button.png"
        app.result_screen.ids.settings_img.source = "Assets/Icons/Settings Button.png"
        app.result_screen.ids.backR_img.source = "Assets/Icons/Back Button.png"

    def high_contrast(self):
        app = App.get_running_app()

        self.bg_color = [0.050196, 1, 0.87451, 1]
        self.bar_color = [0.76862745098, 1, 0, 1]
        self.slider_color = [0.08235294117, 0, 1, 1]
        self.slider_thumb_color = [1, 0, 0.08235294117, 1]
        self.settings_box_color = [0, 0, 0, 1]
        self.result_card_color = [1, 0, 0.08235294117, 1]
        self.font_color_result = [0.050196, 1, 0.87451, 1]

        #Home_Screen
        app.home_screen.ids.capture_img.source = "Assets/Icons/Capture Button High.png"
        app.home_screen.ids.settings_img.source = "Assets/Icons/Settings Button High.png"
        app.home_screen.ids.homePage_img.source = "Assets/Icons/HOME PAGE.png"

        #Capture_Screen
        app.capture_screen.ids.backC_img.source = "Assets/Icons/Back Button High.png"
        app.capture_screen.ids.flashButton_img.source = "Assets/Icons/Flash Button High.png"
        app.capture_screen.ids.repeat_img.source = "Assets/Icons/Repeat Button High.png"
        app.capture_screen.ids.capturePage_img.source = "Assets/Icons/CAPTURE PAGE.png"
        app.capture_screen.ids.tapCapture.source = "Assets/Icons/DOUBLE TAP TO CAPTURE HIGH.png"

        #Settings_Screen
        app.settings_screen.ids.settingsPage_img.source = "Assets/Icons/SETTINGS PAGE.png"
        app.settings_screen.ids.back_img.source = "Assets/Icons/Back Button High.png"
        app.settings_screen.ids.fontSizeNote_img.source = "Assets/Icons/Font Size intro high.png"
        app.settings_screen.ids.soundVolumeNote_img.source = "Assets/Icons/Volume intro high.png"
        app.settings_screen.ids.contrastNote_img.source = "Assets/Icons/Contrast high.png"
        app.settings_screen.ids.fontSize_img.source = "Assets/Icons/Font size.png"
        app.settings_screen.ids.soundVolume_img.source = "Assets/Icons/Volume.png"
        app.settings_screen.ids.contrast_img.source = "Assets/Icons/Contrast.png"
        app.settings_screen.ids.normal.source = "Assets/Icons/Normal Button High.png"
        app.settings_screen.ids.high_contrast.source = "Assets/Icons/High Contrast High.png"
        app.settings_screen.ids.invert.source = "Assets/Icons/Invert Colors High.png"
        app.settings_screen.ids.grayscale.source = "Assets/Icons/Grayscale High.png"

        if (
                app.settings_screen.ids.forty.source == "Assets/Icons/40 pt.png" or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt High.png"
                or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt Gray.png" or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt invert normal.png"
                or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt Invert.png"):

            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt High.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt High.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt High.png"

        elif (
                app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt normal clicked.png" or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt high clicked.png"
                or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt invert normal clicked.png" or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt invert high clicked.png"
                or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt grayscale clicked.png"):

            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt high not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt high clicked.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt High.png"

        elif (
                app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt normal clicked.png" or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt high clicked.png"
                or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt imvert normal clicked.png" or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt invert high clicked.png"
                or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt grayscale clicked.png"):

            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt high not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt High.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt high clicked.png"


        # Result page
        app.result_screen.ids.capturePage_img.source = "Assets/Icons/RESULT PAGE.png"
        app.result_screen.ids.detected_currency.source = "Assets/Icons/DETECTED CURRENCIES HIGH.png"
        app.result_screen.ids.total_currency.source = "Assets/Icons/Total Currency high.png"
        app.result_screen.ids.homeButton_img.source = "Assets/Icons/Home Button Result high.png"
        app.result_screen.ids.settings_img.source = "Assets/Icons/Settings Button Result high.png"
        app.result_screen.ids.backR_img.source = "Assets/Icons/Back Button High.png"

    def invert_color(self):
        app = App.get_running_app()

        if(self.bg_color == [0.050196, 1, 0.87451, 1]):
            self.bg_color = [0.49803921568, 0, 0.12549019607, 1]
            self.bar_color = [0.23137254902, 0, 0.99607843137, 1]
            self.slider_color = [0.91764705882, 0.99607843137, 0, 1]
            self.slider_thumb_color = [0, 1, 0.91764705882, 1]
            self.settings_box_color = [1, 1, 1, 1]
            self.result_card_color = [0, 1, 0.87450980392, 1]
            self.font_color_result = [0.49803921568, 0, 0.12549019607, 1]

            # Home_Screen
            app.home_screen.ids.capture_img.source = "Assets/Icons/Capture Button (1).png"
            app.home_screen.ids.settings_img.source = "Assets/Icons/Settings Button (1).png"
            app.home_screen.ids.homePage_img.source = "Assets/Icons/HOME PAGE INVERT.png"

            # Capture_Screen
            app.capture_screen.ids.backC_img.source = "Assets/Icons/Back Button invert normal.png"
            app.capture_screen.ids.flashButton_img.source = "Assets/Icons/Flash Button invert normal.png"
            app.capture_screen.ids.repeat_img.source = "Assets/Icons/Repeat Button invert normal.png"
            app.capture_screen.ids.capturePage_img.source = "Assets/Icons/CAPTURE PAGE INVERT.png"
            app.capture_screen.ids.tapCapture.source = "Assets/Icons/DOUBLE TAP TO CAPTURE INVERT HIGH.png"

            # Settings_Screen
            app.settings_screen.ids.settingsPage_img.source = "Assets/Icons/SETTINGS PAGE INVERT.png"
            app.settings_screen.ids.back_img.source = "Assets/Icons/Back Button invert normal.png"
            app.settings_screen.ids.fontSizeNote_img.source = "Assets/Icons/Font size notes.png"
            app.settings_screen.ids.soundVolumeNote_img.source = "Assets/Icons/Sound volume note.png"
            app.settings_screen.ids.contrastNote_img.source = "Assets/Icons/Contrast note.png"
            app.settings_screen.ids.fontSize_img.source = "Assets/Icons/Font size Invert.png"
            app.settings_screen.ids.soundVolume_img.source = "Assets/Icons/Volume Invert.png"
            app.settings_screen.ids.contrast_img.source = "Assets/Icons/Contrast Invert.png"
            app.settings_screen.ids.normal.source = "Assets/Icons/Normal Button invert normal.png"
            app.settings_screen.ids.high_contrast.source = "Assets/Icons/High Contrast invert normal.png"
            app.settings_screen.ids.invert.source = "Assets/Icons/Invert Colors invert normal.png"
            app.settings_screen.ids.grayscale.source = "Assets/Icons/Grayscale invert normal.png"

            if (
                    app.settings_screen.ids.forty.source == "Assets/Icons/40 pt.png" or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt High.png"
                    or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt Gray.png" or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt invert normal.png"
                    or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt Invert.png"):

                app.settings_screen.ids.forty.source = "Assets/Icons/40 pt invert normal.png"
                app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt invert normal.png"
                app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt invert normal.png"

            elif (
                    app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt normal clicked.png" or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt high clicked.png"
                    or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt invert normal clicked.png" or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt invert high clicked.png"
                    or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt grayscale clicked.png"):

                app.settings_screen.ids.forty.source = "Assets/Icons/40 pt invert higt not clicked.png"
                app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt invert high clicked.png"
                app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt invert normal.png"

            elif (
                    app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt normal clicked.png" or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt high clicked.png"
                    or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt imvert normal clicked.png" or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt invert high clicked.png"
                    or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt grayscale clicked.png"):

                app.settings_screen.ids.forty.source = "Assets/Icons/40 pt invert higt not clicked.png"
                app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt invert normal.png"
                app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt invert high clicked.png"

            # Result page
            app.result_screen.ids.capturePage_img.source = "Assets/Icons/RESULT PAGE WHITE.png"
            app.result_screen.ids.detected_currency.source = "Assets/Icons/DETECTED CURRENCIES INVERT HIGH.png"
            app.result_screen.ids.total_currency.source = "Assets/Icons/Total Currency invert high.png"
            app.result_screen.ids.homeButton_img.source = "Assets/Icons/Home Button result invert high.png"
            app.result_screen.ids.settings_img.source = "Assets/Icons/Settings Button result invert high.png"
            app.result_screen.ids.backR_img.source = "Assets/Icons/Back Button invert normal.png"


        elif(self.bg_color == [0, .2784, .2431, 1]):
            self.bg_color = [1, 0.72157, 0.75686, 1]
            self.bar_color = [0, 0, 0, 1]
            self.slider_color = [0, 0, 0, 1]
            self.slider_thumb_color = [0.01960784313, 0, 1, 1]
            self.settings_box_color = [1, 1, 1, 1]
            self.result_card_color = [1,0, 0.08235294117, 1]
            self.font_color_result = [0.01960784313, 0, 1, 1]

            #Home_Screen
            app.home_screen.ids.capture_img.source = "Assets/Icons/Capture Button High.png"
            app.home_screen.ids.settings_img.source = "Assets/Icons/Settings Button High.png"
            app.home_screen.ids.homePage_img.source = "Assets/Icons/HOME PAGE INVERT.png"

            #Capture_Screen
            app.capture_screen.ids.backC_img.source = "Assets/Icons/Back Button Invert.png"
            app.capture_screen.ids.flashButton_img.source = "Assets/Icons/Flash Button Invert.png"
            app.capture_screen.ids.repeat_img.source = "Assets/Icons/Repeat Button Invert.png"
            app.capture_screen.ids.capturePage_img.source = "Assets/Icons/CAPTURE PAGE INVERT.png"
            app.capture_screen.ids.tapCapture.source = "Assets/Icons/DOUBLE TAP TO CAPTURE INVERT NORMAL.png"

            #Settings_Screen
            app.settings_screen.ids.settingsPage_img.source = "Assets/Icons/SETTINGS PAGE INVERT.png"
            app.settings_screen.ids.back_img.source = "Assets/Icons/Back Button Invert.png"
            app.settings_screen.ids.fontSizeNote_img.source = "Assets/Icons/Font Size intro high.png"
            app.settings_screen.ids.soundVolumeNote_img.source = "Assets/Icons/Volume intro high.png"
            app.settings_screen.ids.contrastNote_img.source = "Assets/Icons/Contrast high.png"
            app.settings_screen.ids.fontSize_img.source = "Assets/Icons/Font size Invert.png"
            app.settings_screen.ids.soundVolume_img.source = "Assets/Icons/Volume Invert.png"
            app.settings_screen.ids.contrast_img.source = "Assets/Icons/Contrast Invert.png"
            app.settings_screen.ids.normal.source = "Assets/Icons/Normal Button Invert.png"
            app.settings_screen.ids.high_contrast.source = "Assets/Icons/High Contrast Invert.png"
            app.settings_screen.ids.invert.source = "Assets/Icons/Invert Colors Invert.png"
            app.settings_screen.ids.grayscale.source = "Assets/Icons/Grayscale Invert.png"

            if (
                    app.settings_screen.ids.forty.source == "Assets/Icons/40 pt.png" or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt High.png"
                    or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt Gray.png" or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt invert normal.png"
                    or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt Invert.png"):

                app.settings_screen.ids.forty.source = "Assets/Icons/40 pt Invert.png"
                app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt Invert.png"
                app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt Invert.png"

            elif (
                    app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt normal clicked.png" or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt high clicked.png"
                    or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt invert normal clicked.png" or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt invert high clicked.png"
                    or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt grayscale clicked.png"):

                app.settings_screen.ids.forty.source = "Assets/Icons/40 pt inver normal not clicked.png"
                app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt invert normal clicked.png"
                app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt Invert.png"

            elif (
                    app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt normal clicked.png" or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt high clicked.png"
                    or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt imvert normal clicked.png" or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt invert high clicked.png"
                    or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt grayscale clicked.png"):

                app.settings_screen.ids.forty.source = "Assets/Icons/40 pt inver normal not clicked.png"
                app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt Invert.png"
                app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt imvert normal clicked.png"

            # Result page
            app.result_screen.ids.capturePage_img.source = "Assets/Icons/RESULT PAGE WHITE.png"
            app.result_screen.ids.detected_currency.source = "Assets/Icons/DETECTED CURRENCIES INVERT NORMAL.png"
            app.result_screen.ids.total_currency.source = "Assets/Icons/Total Currency invert normal.png"
            app.result_screen.ids.homeButton_img.source = "Assets/Icons/Home Button Result Invert Normal.png"
            app.result_screen.ids.settings_img.source = "Assets/Icons/Settings Button Invert Normal.png"
            app.result_screen.ids.backR_img.source = "Assets/Icons/Back Button Invert.png"

        else:
            self.bg_color = [1, 0.72157, 0.75686, 1]
            self.bar_color = [0, 0, 0, 1]
            self.slider_color = [0, 0, 0, 1]
            self.slider_thumb_color = [0.01960784313, 0, 1, 1]
            self.settings_box_color = [1, 1, 1, 1]
            self.result_card_color = [1, 0, 0.08235294117, 1]
            self.font_color_result = [0.01960784313, 0, 1, 1]

            # Home_Screen
            app.home_screen.ids.capture_img.source = "Assets/Icons/Capture Button High.png"
            app.home_screen.ids.settings_img.source = "Assets/Icons/Settings Button High.png"
            app.home_screen.ids.homePage_img.source = "Assets/Icons/HOME PAGE INVERT.png"

            # Capture_Screen
            app.capture_screen.ids.backC_img.source = "Assets/Icons/Back Button Invert.png"
            app.capture_screen.ids.flashButton_img.source = "Assets/Icons/Flash Button Invert.png"
            app.capture_screen.ids.repeat_img.source = "Assets/Icons/Repeat Button Invert.png"
            app.capture_screen.ids.capturePage_img.source = "Assets/Icons/CAPTURE PAGE INVERT.png"
            app.capture_screen.ids.tapCapture.source = "Assets/Icons/DOUBLE TAP TO CAPTURE INVERT NORMAL.png"

            # Settings_Screen
            app.settings_screen.ids.settingsPage_img.source = "Assets/Icons/SETTINGS PAGE INVERT.png"
            app.settings_screen.ids.back_img.source = "Assets/Icons/Back Button Invert.png"
            app.settings_screen.ids.fontSizeNote_img.source = "Assets/Icons/Font Size intro high.png"
            app.settings_screen.ids.soundVolumeNote_img.source = "Assets/Icons/Volume intro high.png"
            app.settings_screen.ids.contrastNote_img.source = "Assets/Icons/Contrast high.png"
            app.settings_screen.ids.fontSize_img.source = "Assets/Icons/Font size Invert.png"
            app.settings_screen.ids.soundVolume_img.source = "Assets/Icons/Volume Invert.png"
            app.settings_screen.ids.contrast_img.source = "Assets/Icons/Contrast Invert.png"
            app.settings_screen.ids.normal.source = "Assets/Icons/Normal Button Invert.png"
            app.settings_screen.ids.high_contrast.source = "Assets/Icons/High Contrast Invert.png"
            app.settings_screen.ids.invert.source = "Assets/Icons/Invert Colors Invert.png"
            app.settings_screen.ids.grayscale.source = "Assets/Icons/Grayscale Invert.png"

            if (
                    app.settings_screen.ids.forty.source == "Assets/Icons/40 pt.png" or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt High.png"
                    or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt Gray.png" or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt invert normal.png"
                    or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt Invert.png"):

                app.settings_screen.ids.forty.source = "Assets/Icons/40 pt Invert.png"
                app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt Invert.png"
                app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt Invert.png"

            elif (
                    app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt normal clicked.png" or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt high clicked.png"
                    or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt invert normal clicked.png" or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt invert high clicked.png"
                    or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt grayscale clicked.png"):

                app.settings_screen.ids.forty.source = "Assets/Icons/40 pt inver normal not clicked.png"
                app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt invert normal clicked.png"
                app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt Invert.png"

            elif (
                    app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt normal clicked.png" or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt high clicked.png"
                    or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt imvert normal clicked.png" or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt invert high clicked.png"
                    or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt grayscale clicked.png"):

                app.settings_screen.ids.forty.source = "Assets/Icons/40 pt inver normal not clicked.png"
                app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt Invert.png"
                app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt imvert normal clicked.png"

            # Result page
            app.result_screen.ids.capturePage_img.source = "Assets/Icons/RESULT PAGE WHITE.png"
            app.result_screen.ids.detected_currency.source = "Assets/Icons/DETECTED CURRENCIES INVERT NORMAL.png"
            app.result_screen.ids.total_currency.source = "Assets/Icons/Total Currency invert normal.png"
            app.result_screen.ids.homeButton_img.source = "Assets/Icons/Home Button Result Invert Normal.png"
            app.result_screen.ids.settings_img.source = "Assets/Icons/Settings Button Invert Normal.png"
            app.result_screen.ids.backR_img.source = "Assets/Icons/Back Button Invert.png"

    def grayscale_color(self):
        app = App.get_running_app()

        self.bg_color = [0.85098, 0.85098, 0.85098, 1]
        self.bar_color = [1, 1, 1, 1]
        self.slider_color = [0, 0, 0, 1]
        self.slider_thumb_color = [0.34509803921, 0.34509803921, 0.34509803921, 1]
        self.settings_box_color = [0, 0, 0, 1]
        self.result_card_color = [0.52156862745, 0.52156862745, 0.52156862745, 1]
        self.font_color_result = [1, 1, 1, 1]

        #Home_Screen
        app.home_screen.ids.capture_img.source = "Assets/Icons/Capture Button Grayscale.png"
        app.home_screen.ids.settings_img.source = "Assets/Icons/Settings Button Grayscale.png"
        app.home_screen.ids.homePage_img.source = "Assets/Icons/HOME PAGE.png"

        #Capture_Screen
        app.capture_screen.ids.backC_img.source = "Assets/Icons/Back Button.png"
        app.capture_screen.ids.flashButton_img.source = "Assets/Icons/Flash Button Grayscale.png"
        app.capture_screen.ids.repeat_img.source = "Assets/Icons/Repeat Button Grayscale.png"
        app.capture_screen.ids.capturePage_img.source = "Assets/Icons/CAPTURE PAGE.png"
        app.capture_screen.ids.tapCapture.source = "Assets/Icons/DOUBLE TAP TO CAPTURE GRAYSCALE.png"

        #Settings_Screen
        app.settings_screen.ids.settingsPage_img.source = "Assets/Icons/SETTINGS PAGE.png"
        app.settings_screen.ids.back_img.source = "Assets/Icons/Back Button.png"
        app.settings_screen.ids.fontSizeNote_img.source = "Assets/Icons/Font Size intro high.png"
        app.settings_screen.ids.soundVolumeNote_img.source = "Assets/Icons/Volume intro high.png"
        app.settings_screen.ids.contrastNote_img.source = "Assets/Icons/Contrast high.png"
        app.settings_screen.ids.fontSize_img.source = "Assets/Icons/Font size.png"
        app.settings_screen.ids.soundVolume_img.source = "Assets/Icons/Volume.png"
        app.settings_screen.ids.contrast_img.source = "Assets/Icons/Contrast.png"
        app.settings_screen.ids.normal.source = "Assets/Icons/Normal Button Gray.png"
        app.settings_screen.ids.high_contrast.source = "Assets/Icons/High Contrast Gray.png"
        app.settings_screen.ids.invert.source = "Assets/Icons/Invert Colors Gray.png"
        app.settings_screen.ids.grayscale.source = "Assets/Icons/Grayscale Gray.png"

        if (
                app.settings_screen.ids.forty.source == "Assets/Icons/40 pt.png" or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt High.png"
                or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt Gray.png" or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt invert normal.png"
                or app.settings_screen.ids.forty.source == "Assets/Icons/40 pt Invert.png"):

            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt Gray.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt Gray.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt Gray.png"

        elif (
                app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt normal clicked.png" or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt high clicked.png"
                or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt invert normal clicked.png" or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt invert high clicked.png"
                or app.settings_screen.ids.forty_eight.source == "Assets/Icons/48 pt grayscale clicked.png"):

            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt grayscale not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt grayscale clicked.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt Gray.png"

        elif (
                app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt normal clicked.png" or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt high clicked.png"
                or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt imvert normal clicked.png" or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt invert high clicked.png"
                or app.settings_screen.ids.fifty_six.source == "Assets/Icons/56 pt grayscale clicked.png"):

            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt grayscale not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt Gray.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt grayscale clicked.png"

        # Result page
        app.result_screen.ids.capturePage_img.source = "Assets/Icons/RESULT PAGE.png"
        app.result_screen.ids.detected_currency.source = "Assets/Icons/DETECTED CURRENCIES.png"
        app.result_screen.ids.total_currency.source = "Assets/Icons/Total Currency.png"
        app.result_screen.ids.homeButton_img.source = "Assets/Icons/Home Button Result Grayscale.png"
        app.result_screen.ids.settings_img.source = "Assets/Icons/Settings Button Result Grayscale.png"
        app.result_screen.ids.backR_img.source = "Assets/Icons/Back Button.png"

    def forty_button(self):
        app = App.get_running_app()
        self.fontSize = 40

        if(self.bg_color == [0, .2784, .2431, 1]):
            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt.png"

        elif(self.bg_color == [0.050196, 1, 0.87451, 1]):
            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt High.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt High.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt High.png"

        elif(self.bg_color == [0.49803921568, 0, 0.12549019607, 1]):
            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt invert normal.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt invert normal.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt invert normal.png"

        elif(self.bg_color == [1, 0.72157, 0.75686, 1]):
            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt Invert.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt Invert.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt Invert.png"

        elif(self.bg_color == [0.85098, 0.85098, 0.85098, 1]):
            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt Gray.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt Gray.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt Gray.png"



    def fortyeight_button(self):
        app = App.get_running_app()
        self.fontSize = 48

        if (self.bg_color == [0, .2784, .2431, 1]):
            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt normal clicked.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt.png"

        elif (self.bg_color == [0.050196, 1, 0.87451, 1]):
            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt high not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt high clicked.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt High.png"

        elif (self.bg_color == [0.49803921568, 0, 0.12549019607, 1]):
            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt invert higt not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt invert high clicked.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt invert normal.png"

        elif (self.bg_color == [1, 0.72157, 0.75686, 1]):
            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt inver normal not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt invert normal clicked.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt Invert.png"


        elif (self.bg_color == [0.85098, 0.85098, 0.85098, 1]):
            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt grayscale not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt grayscale clicked.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt Gray.png"

    def fiftysix_button(self):
        app = App.get_running_app()
        self.fontSize = 56

        if (self.bg_color == [0, .2784, .2431, 1]):
            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt normal clicked.png"

        elif (self.bg_color == [0.050196, 1, 0.87451, 1]):
            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt high not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt High.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt high clicked.png"

        elif (self.bg_color == [0.49803921568, 0, 0.12549019607, 1]):
            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt invert higt not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt invert normal.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt imvert normal clicked.png"

        elif (self.bg_color == [1, 0.72157, 0.75686, 1]):
            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt inver normal not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt Invert.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt imvert normal clicked.png"

        elif (self.bg_color == [0.85098, 0.85098, 0.85098, 1]):
            app.settings_screen.ids.forty.source = "Assets/Icons/40 pt grayscale not clicked.png"
            app.settings_screen.ids.forty_eight.source = "Assets/Icons/48 pt Gray.png"
            app.settings_screen.ids.fifty_six.source = "Assets/Icons/56 pt grayscale clicked.png"


TapAndListen().run()
