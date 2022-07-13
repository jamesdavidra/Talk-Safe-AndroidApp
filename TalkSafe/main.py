from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from passlib.exc import ExpectedStringError

from gpshelper import GpsHelper
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


WordSave = []
Email_List = []


class LoginScreen(Screen):
    pass


class ButtonWindow(Screen):
    dialog = None

    def on_start(self, obj):
        Clock.schedule_interval(self.search, 5.5)
        self.dialog.dismiss()

    def act_btn(self, widget):
        if widget.state == "normal":
            widget.text = "Activate"
            widget.background_color = 0, 0.5, 0.2, 1
            Clock.unschedule(self.search)

        else:
            widget.text = "Deactivate"
            widget.background_color = 1, 0, 0, 1
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Voice Capture",
                    text="Allow speech recognition?",
                    buttons=[
                        MDFlatButton(
                            text="No",
                            on_release=self.close_dialog
                        ),
                        MDRectangleFlatButton(
                            text="Yes",
                            on_release=self.on_start
                        ),
                    ],
                )

            self.dialog.open()

    def search(self, *args):
        from SpeechRecog import recognize
        from SendingEmail import SendEmail
        from Database import c
        from passlib.context import CryptContext

        def email_list():
            c.execute("SELECT email FROM Contact")
            for email in c.fetchall():
                email = email[0]
                Email_List.append(email)
            return Email_List

        pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

        c.execute("SELECT pass_key FROM Keyword")
        keyword = recognize()
        for data in c.fetchall():
            if pwd_cxt.verify(keyword, data[0]):
                contacts = email_list()
                SendEmail(contacts)
                Email_List.clear()
            else:
                Email_List.clear()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def show_location(self, *args, **kwargs):
        my_lat = kwargs['lat']
        my_lon = kwargs['lon']
        from SendingEmail import SendGPS

        lat = str(my_lat)
        lon = str(my_lon)

        def email_list():
            from Database import c

            c.execute("SELECT email FROM Contact")
            for email in c.fetchall():
                email = email[0]
                Email_List.append(email)
            return Email_List

        contacts = email_list()

        SendGPS(lat, lon, contacts)
        Email_List.clear()

    def switch_click(self, switch_Value):
        from plyer import gps
        if switch_Value:
            gps.configure(on_location=self.show_location, on_status=None)
            gps.start(minTime=1800000, minDistance=0)

        else:
            gps.stop()


class AddKeyword(Screen):
    dialog = None

    def animate(self, widget, *args):
        animation = Animation(user_font_size=70, duration=.4) + Animation(user_font_size=75, duration=.4)
        animation.start(widget)
        animation.bind(on_complete=self.keyword)
        self.ids.record_label.text = "Recording..."

    def keyword(self, *args):
        from SpeechRecog import recognize
        key = recognize()
        self.ids.record_label.text = "Press Record"
        err_one = "No word/s recognized, Try again."
        err_two = "Please try again."
        if (key != err_one) & (key != err_two):
            WordSave.append(key)

        self.ids.keyword_label.text = key
        return WordSave

    def reset(self, *args):
        if len(WordSave) != 0:
            WordSave.clear()

        self.ids.record_label.text = "Press Record"
        self.ids.keyword_label.text = ""

    def save(self, *args):
        from Database import connection, c
        from passlib.context import CryptContext

        pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
        password = ""
        if len(WordSave) != 0:
            password = pwd_cxt.hash(WordSave[0])
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Keyword Register",
                    text="Do you want to register a keyword again?",
                    buttons=[
                        MDFlatButton(
                            text="Back",
                            on_release=self.close_dialog
                        ),
                        MDRectangleFlatButton(
                            text="Okay",
                            on_release=self.agree_dialog
                        ),
                    ],
                )

            self.dialog.open()

            c.execute("INSERT INTO Keyword (pass_key) VALUES(?)", (password,))
            connection.commit()
        else:
            self.ids.keyword_label.text = "No word/s can be saved"

    def close_dialog(self, obj):
        self.dialog.dismiss()
        self.ids.record_label.text = "Press Record"
        self.ids.keyword_label.text = ""

    def agree_dialog(self, obj):
        self.dialog.dismiss()
        self.ids.record_label.text = "Press Record"
        self.ids.keyword_label.text = ""


class AddContact(Screen):
    dialog = None

    def save(self):
        from Database import connection, c

        fullname = self.ids.name.text
        email = self.ids.email.text
        phone_number = self.ids.number.text

        if (fullname != "") & (email != "") & (phone_number != ""):
            self.ids.fields_required.text = ""
            c.execute("INSERT INTO Contact(full_name, email, contact_number) VALUES(?,?,?)",
                      (fullname, email, phone_number))
            connection.commit()
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Contact Registered",
                    text="Do you want to register a contact again?",
                    buttons=[
                        MDFlatButton(
                            text="Back",
                            on_release=self.close_dialog
                        ),
                        MDRectangleFlatButton(
                            text="Okay",
                            on_release=self.agree_dialog
                        ),
                    ],
                )

            self.dialog.open()
        else:
            self.ids.fields_required.text = "All fields are required!"

    def close_dialog(self, obj):
        self.dialog.dismiss()
        self.ids.fields_required.text = ""
        self.ids.name.text = ""
        self.ids.email.text = ""
        self.ids.number.text = ""

    def agree_dialog(self, obj):
        self.dialog.dismiss()
        self.ids.fields_required.text = ""
        self.ids.name.text = ""
        self.ids.email.text = ""
        self.ids.number.text = ""


class MapViewUser(Screen):
    def on_start(self):
        GpsHelper().run()


class MainApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = 'BlueGray'

    def change_screen(self, screen_name, direction):
        screen_manager = self.root
        screen_manager.transition.direction = direction
        screen_manager.current = screen_name


MainApp().run()
