from pytronlinks import Client as Pytron

from os.path import dirname, join
from os import listdir
from time import time
from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.storage.dictstore import DictStore
from kivy.storage.jsonstore import JsonStore
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.video import Video


class MainScreen(Screen):
    """ In charge of drawing the main screens. Should be left as is. """
    fullscreen = BooleanProperty(False)
    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(MainScreen, self).add_widget(*args)


class Jarvis(Pytron):
    """ Jarvis Pytron class """

    def __init__(self, name, **kwargs):
        super(Jarvis, self).__init__(**kwargs)
        self.name = name

# class Clients(Screen):
#     pass

# class Interact(Screen):
#     pass

class LinksApp(App):

    HOME_SCREEN = 'About'
    icon = StringProperty(None)
    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    listed_screen_names = ListProperty([])
    hierarchy = ListProperty([])
    default_client = StringProperty()
    active_client = ObjectProperty()
    client_list = ListProperty([])
    client_name = StringProperty()
    client_ip = StringProperty()
    client_port = StringProperty()
    client_key = StringProperty()    
    available_screens = ListProperty([])
    client_storage = JsonStore("clients.json")
    client_settings = JsonStore("clientsettings.json")

    def build(self):

        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.initialize()


    def initialize(self):
        
        _curdir = dirname(__file__)
        self.icon = _curdir + '\data\media\logo.png'
        self.title = 'Jarvis'

        if not self.client_settings.exists('DefaultClient'):
            self.client_settings.put("DefaultClient", name="DefaultAI")
            print "TODO: Set default for first use"
        self.default_client = str(self.client_settings.get('DefaultClient')['name'])
        print "Default client name: %s" % self.client_settings.get('DefaultClient')['name']

        self.set_active_client(self.default_client)
        print "Active client info __>"
        # print (str(self.active_client.name), str(self.active_client.ip), str(self.active_client.port), str(self.active_client.key))

        self.screens = {}
        self.refresh_client_list()
        # print "Client list: %s \n\n" % self.client_list

        # Populates the dropdown menu with the.kv files  
        # located in the ./data/screens/ directory.
        self.screen_names = [i[:-3].capitalize() for i in listdir(join(_curdir, 'data', 'screens')) if '.kv' in i]
        self.available_screens = [join(_curdir, 'data', 'screens', '{}.kv'.format(fn)) for fn in self.screen_names]
        print "Available screens: %s \n\n" % self.available_screens
        print "Screen names: %s \n\n" % self.screen_names
        self.nav_home()


    def set_active_client(self, client_name=None):
        if not client_name:
            client_name = self.default_client
        print "Set active client name: %s" % client_name
        print "Client storage %s" % self.client_storage
        for i in self.client_storage:
            print i

        client_data = self.client_storage.get(str(client_name))
        print "Setting active client: {} {}".format(client_name, client_data)
        self.client_name=client_name
        self.client_ip=client_data['ip']
        self.client_port=client_data['port']
        self.client_key=client_data['linkskey']

        
        self.active_client = Jarvis(self.client_name,
                                    ip=self.client_ip,
                                    port=self.client_port,
                                    key=self.client_key)
        print "New active client name: %s \n\n" % self.active_client.name
        self.refresh_client_list()
        return self.active_client


    def get_client_list(self):
        return [i for i in self.client_storage]


    def refresh_client_list(self):
        print "Before client_list refresh: %s \n\n" % self.client_list
        self.client_list = self.get_client_list()
        print "After client_list refresh: %s \n\n" % self.client_list
        active_client = self.active_client
        self.active_client = active_client


    def set_default_client(self, client_name):
        self.client_storage.put("DefaultClient", client_name)


    def get_active_client_info(self, arg):
        if arg.lower() == 'ip':
            print "IP Match"
            return self.active_client.ip
        if arg.lower() == 'port':
            print "PORT Match"
            return self.active_client.port
        if arg.lower() == 'key':
            print "KEY Match"
            return self.active_client.key                          
        return self.active_client.name


    def save_client(self, name, ip, port, linkskey, overwrite=False):
        print name, ip, port, linkskey
        if overwrite or name not in self.client_storage.keys():
            print "OVERWRITING!!"
            self.client_storage.put(str(name), ip=str(ip), port=str(port), linkskey=str(linkskey))
            print "Success.."
            print "Save client NAME: %s" % name
            self.set_active_client(name)
            self.refresh_client_list()
        else:
            self.show_error("There is already a client named %s" % name)


    def delete_client(self, name):
        print "Delete client name: %s" % name
        print "Default client: %s" % self.default_client
        if name == self.default_client:
            print "Cannot delete default client"
            return
        print self.client_storage.keys()
        if self.client_storage.exists(name):
            print "Before delete: %s" % self.client_storage.keys()
            self.client_storage.delete(name)
            print "After delete: %s" % self.client_storage.keys()
            self.set_active_client()
            self.refresh_client_list()

            return True
        self.set_active_client()


    def nav_home(self, swipe_direction='left'):
        self.nav_to(self.HOME_SCREEN, swipe_direction)


    def nav_to(self, screen_name, swipe_direction='left'):
        """ Use to navigate to a screen by name. """
        idx = self.screen_names.index(screen_name)
        self.go_screen(idx, dir=swipe_direction)


    def go_screen(self, idx, dir='left'):
        """ Navigate forward to screen by index. S """
        self.index = idx
        print "Go screen index {}".format(self.index)
        self.root.ids.sm.switch_to(self.load_screen(idx), direction=dir)
        screen = self.load_screen(self.index)
        self.current_title = screen.name
        self.update_sourcecode()


    def go_previous_screen(self):
        """ Swipes screen to the right. 
            Simulates a "go back" style animation.
 
        """
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        self.update_sourcecode()


    def go_hierarchy_previous(self):
        """ This method contains the functionality of the "back" Button
            on the main action bar.

        """
        ahr = self.hierarchy
        if len(ahr) == 1:
            return
        if ahr:
            ahr.pop()
        if ahr:
            idx = ahr.pop()
            self.go_screen(idx, dir='right')


    def load_screen(self, index):
        """ Checks if screen exists and load. """

        print "Load screen index: %s" % index
        if index in self.screens:
            return self.screens[index]
        # screen = Builder.load_file(self.available_screens[index])
        screen = Builder.load_file(self.available_screens[index].lower())
        print "Load screen: {}".format(screen)
        self.screens[index] = screen
        return screen


    def go_next_screen(self):
        """ Swipes screen to the left. Only used once in build method.. """

        self.index = (self.index + 1) % len(self.available_screens)
        print "Go next screen index: {}".format(self.index)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        print "Screen name: {}".format(screen.name)
        self.current_title = screen.name
        print "Current title: {}".format(self.current_title)
        self.update_sourcecode()


    def on_enter(instance, value):
        """ Callback """
        print('Instance: ', vars(instance))
        print('Value: ', value.text)


    def on_text(self, instance, value):
        """ Callback """
        print('Typing: ', value)


    def read_sourcecode(self):
        """ Callback """
        fn = self.available_screens[self.index].lower()
        with open(fn) as fd:
            return fd.read()


    def toggle_source_code(self):
        """ Callback """        
        self.show_sourcecode = not self.show_sourcecode
        if self.show_sourcecode:
            height = self.root.height * .3
        else:
            height = 0

        Animation(height=height, d=.3, t='out_quart').start(
                self.root.ids.sv)

        self.update_sourcecode()


    def update_sourcecode(self):
        """ Callback """        
        if not self.show_sourcecode:
            self.root.ids.sourcecode.focus = False
            return
        self.root.ids.sourcecode.text = self.read_sourcecode()
        self.root.ids.sv.scroll_y = 1


    def show_error(self, e):
        self.info_label.text = str(e).encode('utf-8')
        self.anim = Animation(top=190.0, opacity=1, d=2, t='in_back') +\
            Animation(top=190.0, d=3) +\
            Animation(top=0, opacity=0, d=2)
        self.anim.start(self.info_label)


    # def on_current_title(self, instance, value):
    #     """  """
    #     print "Current title value: {}".format(value)
    #     self.root.ids.spnr.text = value


    def _update_clock(self, dt):
        """ Handles clock cycles """
        self.time = time()


    def on_pause(self):
        """ For internal use """
        return True


    def on_resume(self):
        """ For internal use """
        pass

        
if __name__ == '__main__':
    LinksApp().run()
