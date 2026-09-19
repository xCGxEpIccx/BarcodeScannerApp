import cv2
from pyzbar.pyzbar import decode
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image


class BarcodeListApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_list = {}
        self.scan_mode = "add"
        self.main_layout = None
        self.mode_layout = None
        self.btn_add = None
        self.btn_remove = None
        self.camera_view = None
        self.status_label = None
        self.scroll_view = None
        self.list_label = None
        self.capture = None

    def build(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.mode_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)

        self.btn_add = ToggleButton(text="Hinzufügen (+)", state="down", group="mode", font_size='18sp')
        self.btn_add.bind(on_press=self.set_mode_add)

        self.btn_remove = ToggleButton(text="Entfernen (-)", state="normal", group="mode", font_size='18sp')
        self.btn_remove.bind(on_press=self.set_mode_remove)

        self.mode_layout.add_widget(self.btn_add)
        self.mode_layout.add_widget(self.btn_remove)
        self.main_layout.add_widget(self.mode_layout)

        self.camera_view = Image(size_hint_y=0.4)
        self.main_layout.add_widget(self.camera_view)

        self.status_label = Label(text="Kamera startet...", size_hint_y=0.1, color=(1, 1, 0, 1), font_size='16sp')
        self.main_layout.add_widget(self.status_label)

        self.scroll_view = ScrollView(size_hint_y=0.4)
        self.list_label = Label(text="Die Liste ist aktuell leer.", size_hint_y=None, halign='left', valign='top',
                                font_size='16sp')
        self.list_label.bind(texture_size=self.list_label.setter('size'))
        self.scroll_view.add_widget(self.list_label)
        self.main_layout.add_widget(self.scroll_view)

        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update_camera, 1.0 / 30.0)

        return self.main_layout

    def set_mode_add(self, instance):
        self.scan_mode = "add"
        self.status_label.text = "Modus: Hinzufügen aktiv"

    def set_mode_remove(self, instance):
        self.scan_mode = "remove"
        self.status_label.text = "Modus: Entfernen aktiv"

    def update_camera(self, dt):
        ret, frame = self.capture.read()
        if ret:
            barcodes = decode(frame)
            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                self.process_barcode(barcode_data)

            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.camera_view.texture = texture

    def process_barcode(self, code):
        if self.scan_mode == "add":
            if code in self.item_list:
                self.item_list[code] += 1
            else:
                self.item_list[code] = 1
            self.status_label.text = f"Gescannt (+): {code}"

        elif self.scan_mode == "remove":
            if code in self.item_list:
                self.item_list[code] -= 1
                if self.item_list[code] <= 0:
                    del self.item_list[code]
                self.status_label.text = f"Entfernt (-): {code}"
            else:
                self.status_label.text = f"Fehler: {code} nicht in der Liste!"

        self.update_list_display()

    def update_list_display(self):
        if not self.item_list:
            self.list_label.text = "Die Liste ist aktuell leer."
            return

        display_text = "Aktuelle Liste:\n"
        for item, count in self.item_list.items():
            display_text += f"• Code: {item} | Anzahl: {count}\n"
        self.list_label.text = display_text

    def on_stop(self):
        if self.capture:
            self.capture.release()


if __name__ == '__main__':
    BarcodeListApp().run()
