from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import os
from kivy.uix.image import Image
import requests
import time
from kivy.garden.graph import Graph, MeshLinePlot


class UserStatusApp(Screen):
    def __init__(self, **kwargs):
        super(UserStatusApp, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=50, padding=50)

        # Create buttons
        self.already_user_button = Button(text="Already a User", on_press=self.show_login_popup)
        self.new_user_button = Button(text="New User", on_press=self.show_registration_popup)

        # Add buttons to the layout
        self.layout.add_widget(Label(text='LOGN TO ADD YOUR PULSE VALUES', font_size=27, bold=True, height=40))
        self.layout.add_widget(self.already_user_button)
        self.layout.add_widget(self.new_user_button)

        self.add_widget(self.layout)

    def show_login_popup(self, instance):
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Create text inputs for name and password
        name_input = TextInput(hint_text='Enter your name')
        password_input = TextInput(hint_text='Enter your password', password=True)

        # Create a login button
        login_button = Button(text="Existng User Login", on_press=lambda x: self.login(name_input.text, password_input.text))

        # Add widgets to the popup layout
        popup_layout.add_widget(Label(text='Login'))
        popup_layout.add_widget(name_input)
        popup_layout.add_widget(password_input)
        popup_layout.add_widget(login_button)

        # Create the popup
        login_popup = Popup(title='Login', content=popup_layout, size_hint=(None, None), size=(600, 400))

        # Open the popup
        login_popup.open()        # Your existing login popup code goes here

    def show_registration_popup(self, instance):
        registration_layout = BoxLayout(orientation = 'vertical',padding = 10, spacing = 10)

        # Labels
        name_label = Label(text = "Name:", font_size = 17)
        email_label = Label(text = "Email:", font_size = 17)
        password_label = Label(text = "Password:", font_size = 17)
        confirm_label = Label(text = "Confirm Password:", font_size = 17)

        # Login Button
        register_button = Button(text="Register", on_press=lambda x: self.register(self.name_input.text, self.email_input.text, self.password_input.text))
        
        #Taking Input
        self.name_input = TextInput(multiline = False, font_size = 15)
        self.email_input = TextInput(multiline = False, font_size = 15)
        self.password_input = TextInput(multiline = False, font_size = 15, password = True)
        self.confirm_input = TextInput(multiline = False, font_size = 15, password = True)

        #Displayed Labels
        registration_layout.add_widget(name_label)
        registration_layout.add_widget(self.name_input)
        registration_layout.add_widget(email_label)
        registration_layout.add_widget(self.email_input)
        registration_layout.add_widget(password_label)
        registration_layout.add_widget(self.password_input)
        registration_layout.add_widget(confirm_label)
        registration_layout.add_widget(self.confirm_input)
        registration_layout.add_widget(register_button)

        # Create the popup
        registration_popup = Popup(title='New User Registration', content=registration_layout, size_hint=(None, None), size=(1050, 750))

        # Open the popup
        registration_popup.open()
        # Your existing registration popup code goes here

    def val(self, instance):
        name = self.name_input.text
        email = self.email_input.text
        password = self.password_input.text
        confirm  =  self.confirm_input.text

        if name.strip() == '' or email.strip() == '' or password.strip() == '' or confirm.strip() == '':
            message = "Please Fill in all the Details"

        elif password != confirm:
            message = "Passwords Do not Match"

        elif name.isalpha() == False:
            message = "Enter a proper name"

        else:
            filename = name+ '.txt'
            with open(filename, 'w') as file:
                file.write('Name: {}\n'.format(name))
                file.write('Email: {}\n'.format(email))
                file.write('Password: {}\n'.format(password))

            message = 'Login Successfull'

        popup = Popup(title = "Login Status", content=Label(text=message),size_hint = (None,None), size = (400,200))
        popup.open()

    def register(self, name, email, password):

        name = self.name_input.text
        email = self.email_input.text
        password = self.password_input.text
        confirm  =  self.confirm_input.text
        user_file_path = f"{name}_credentials.txt"

        if name.strip() == '' or email.strip() == '' or password.strip() == '' or confirm.strip() == '':
            message = "Please Fill in all the Details"

        elif password != confirm:
            message = "Passwords Do not Match"

        elif name.isalpha() == False:
            message = "Enter a proper name"
            
        
        elif os.path.exists(user_file_path):
            print("User already exists. Please choose a different name.")
        else:
            with open(user_file_path, 'w') as file:
                file.write(f"{password}\n")
                file.write('The above mentioned is your password\n')
                file.write('Name: {}\n'.format(name))
                file.write('Email: {}\n'.format(email))
                 
            print(f"Registration successful for {name}!")
            message = 'Login Successfull'

        popup = Popup(title = "Login Status", content=Label(text=message),size_hint = (None,None), size = (400,200))
        popup.open()
    
    def login(self,name,password):
        user_file_path = f"{name}_credentials.txt"
        if os.path.exists(user_file_path):
            with open(user_file_path, 'r') as file:
                stored_password = file.readline().strip()
                if stored_password == password:
                    print(f"Welcome back, {name}!")
                    popup = Popup(title = "Login Status", content=Label(text='Welcome back! Opening your file'),size_hint = (None,None), size = (400,200))
                    popup.open()
                    self.open_text_file(user_file_path)
                    self.manager.current = 'visualization'

                    

                else:
                    popup = Popup(title = "Login Status", content=Label(text='Incorrect password. Please try again.'),size_hint = (None,None), size = (400,200))
                    popup.open()
                    
                    
        else:
            print("User not found. Please check your name or register as a new user.")

    def open_text_file(self, file_path):
        # Open the text file using the default system application
        os.system(f'start notepad "{file_path}"')

    def show_error_popup(self, message):
        # Display an error popup
        popup = Popup(title="Login Status", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

class VisualizationScreen(Screen):
    # Your existing VisualizationScreen class remains unchanged
    def __init__(self, **kwargs):
       
        super(VisualizationScreen, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        graph_layout = BoxLayout(orientation='horizontal', spacing=10) 

        # Create buttons
        self.start_button = Button(text="Start", on_press=self.start_visualization,size_hint=(0.3, None))
        self.stop_button = Button(text="Stop", on_press=self.stop_visualization,size_hint=(0.3, None) )
        self.save_button = Button(text="Save", on_press=self.save_pulse_values,size_hint=(0.3, None))
        
        buttons_layout.add_widget(self.start_button)
        buttons_layout.add_widget(self.stop_button)
        buttons_layout.add_widget(self.save_button)

        self.layout.add_widget(buttons_layout)

        self.graph = Graph(xlabel='Time', ylabel='Values', x_ticks_minor=200,
                           x_ticks_major=1000, y_ticks_minor=5000,
                           y_ticks_major=25000, y_grid_label=True, x_grid_label=True,
                           padding=5, x_grid=True, y_grid=True, xmin=0, xmax=500, ymin=0, ymax=100000)
        
        # MeshLinePlot for each value (Vaata, Pitta, Kapha)
        self.vaata_plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.pitta_plot = MeshLinePlot(color=[0, 1, 0, 1])
        self.kapha_plot = MeshLinePlot(color=[0, 0, 1, 1])

        self.graph.add_plot(self.vaata_plot)
        self.graph.add_plot(self.pitta_plot)
        self.graph.add_plot(self.kapha_plot)
        # Add buttons to the layout
        graph_layout.add_widget(self.graph)
   
        self.layout.add_widget(graph_layout)
        self.add_widget(self.layout)

        # Initialize pulse values
        self.vaata_values = []
        self.pitta_values = []
        self.kapha_values = []

        # Initialize visualization flag
        self.visualization_active = False

        # Schedule the visualization update function
        self.update_interval = None


    def start_visualization(self, instance):
        self.visualization_active = True
        self.update_interval = Clock.schedule_interval(self.update_visualization, 0.1)  # Update every 0.1 seconds
        self.stop_button.disabled = False
        self.start_button.disabled = True

    def stop_visualization(self, instance):
        self.visualization_active = False
        if self.update_interval:
            self.update_interval.cancel()
        self.stop_button.disabled = True
        self.start_button.disabled = False

    def save_pulse_values(self,name, instance):
        # Save pulse values to a text file
        login_screen = self.manager.get_screen('login')
        user_name = login_screen.name_input.text
        user_file_path = f"{name}_credentials.txt"
        if os.path.exists(user_file_path):
            with open(user_file_path, 'w') as file:
                    file.write("Vaata, Pitta, Kapha\n")
                    for vaata, pitta, kapha in zip(self.vaata_values, self.pitta_values, self.kapha_values):
                        file.write(f"{vaata}, {pitta}, {kapha}\n")
                    self.show_message_popup(f"Pulse values saved to {name}_credentials.txt")
        

        
        

    def update_visualization(self, dt):
        # Simulated pulse values received from Arduino (replace with actual implementation)
        vaata, pitta, kapha = self.receive_pulse_values_from_arduino()

        # Update pulse values
        self.vaata_values.append(vaata)
        self.pitta_values.append(pitta)
        self.kapha_values.append(kapha)


        # Update the pulse waveform image
        self.vaata_plot.points = [(i, val) for i, val in enumerate(self.vaata_values)]
        self.pitta_plot.points = [(i, val) for i, val in enumerate(self.pitta_values)]
        self.kapha_plot.points = [(i, val) for i, val in enumerate(self.kapha_values)]

    def receive_pulse_values_from_arduino(self):
        # Simulated pulse values (replace with actual implementation)
        url = "http://192.168.132.66/"  # Replace with the URL of the website
        while True:
            response = requests.get(url)
            
            if response.status_code == 200:
                content = response.text
                print(f"Response: {content}")
                values = content.split(",")  # Split values by comma
                
                if len(values) == 3:
                    try:
                        
                        vaata = float(values[0])
                        pitta = float(values[1])
                        kapha = float(values[2])
                        return vaata, pitta, kapha  # Return parsed values
                    except ValueError:
                        pass

            else:
                print(f"Error: {response.status_code}")
            
            time.sleep(0.01)
        
    

    def show_error_popup(self, message):
        # Display an error popup
        popup = Popup(title="Error", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def show_message_popup(self, message):
        # Display a message popup
        popup = Popup(title="Info", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()    

class PulseVisualizationApp(App):
    def build(self):
        self.title = "Pulse Waveform Visualization"
        self.screen_manager = ScreenManager()

        # Add Login Screen
        login_screen = UserStatusApp(name='login')
        self.screen_manager.add_widget(login_screen)

        # Add Visualization Screen
        visualization_screen = VisualizationScreen(name='visualization')
        self.screen_manager.add_widget(visualization_screen)

        return self.screen_manager

# Run the Kivy application
if __name__ == '__main__':
    PulseVisualizationApp().run()
