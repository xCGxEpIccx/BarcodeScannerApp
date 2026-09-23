from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.camera import Camera

class BarcodeScannerApp(App):
    def build(self):
        self.products = {}
        self.mode = "add"

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Startet die Kamera direkt nativ über das System
        try:
            self.camera = Camera(play=True, resolution=(640, 480))
            main_layout.add_widget(self.camera)
        except Exception:
            main_layout.add_widget(Label(text="Kamera konnte nicht geladen werden"))

        self.status_label = Label(
            text="Modus: Hinzufügen (+) | Bereit zum Scannen",
            size_hint_y=None,
            height=40,
            color=(0, 1, 0, 1)
        )
        main_layout.add_widget(self.status_label)

        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.btn_add = Button(text="Hinzufügen (+)", background_color=(0, 0.7, 0, 1))
        self.btn_add.bind(on_press=self.set_add_mode)
        
        self.btn_remove = Button(text="Entfernen (-)", background_color=(0.7, 0, 0, 1))
        self.btn_remove.bind(on_press=self.set_remove_mode)
        
        btn_layout.add_widget(self.btn_add)
        btn_layout.add_widget(self.btn_remove)
        main_layout.add_widget(btn_layout)

        scroll = ScrollView()
        self.list_label = Label(
            text="Dein Bestand ist leer.",
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.list_label.bind(texture_size=self.list_label.setter('size'))
        scroll.add_widget(self.list_label)
        main_layout.add_widget(scroll)

        return main_layout

    def set_add_mode(self, instance):
        self.mode = "add"
        self.status_label.text = "Modus: Hinzufügen (+) | Bereit zum Scannen"

    def set_remove_mode(self, instance):
        self.mode = "remove"
        self.status_label.text = "Modus: Entfernen (-) | Bereit zum Scannen"

if __name__ == '__main__':
    BarcodeScannerApp().run()
