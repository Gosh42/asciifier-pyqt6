from asciifier import Asciifier
from resizeable import Resizeable
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QTextEdit, \
    QSlider, QPushButton, QFileDialog, QSpinBox, QHBoxLayout, QVBoxLayout, QCheckBox
from PyQt6.QtCore import QSize, Qt, QStandardPaths
from PyQt6.QtGui import QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ascii: Asciifier | None = None
        self.file_path = ''
        self.size_is_linked: bool = False
        self.size = Resizeable(1, 1)
        self.letters_per_pixel: int = 2

        self.setWindowTitle('Asciifier')
        self.setMinimumSize(QSize(640, 360))

        self.result_text = QTextEdit("hi")
        self.result_text.setFont(QFont("Consolas"))
        self.result_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.result_text.setMinimumSize(320, 360)

        self.font_slider = QSlider(Qt.Orientation.Horizontal)
        self.font_slider.setMinimum(1)
        self.font_slider.setMaximum(30)
        self.font_slider.setValue(10)
        self.set_result_font_size(10)
        self.font_slider.valueChanged.connect(self.set_result_font_size)

        # self.path_text = QLineEdit("File path")
        # self.path_text.setReadOnly(True)
        self.path_text = QTextEdit("File path")
        self.path_text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.path_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.path_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.path_text.setMaximumHeight(32)
        self.path_text.setReadOnly(True)

        self.btn_open = QPushButton("Open")
        self.btn_open.released.connect(self.open_file_dialog)

        self.width_selector = QSpinBox()
        self.width_selector.setMinimum(1)
        self.width_selector.setMaximum(2**16)
        self.width_selector.valueChanged.connect(self.on_width_changed)

        self.height_selector = QSpinBox()
        self.height_selector.setMinimum(1)
        self.height_selector.setMaximum(2**16)
        self.height_selector.valueChanged.connect(self.on_height_changed)

        self.link_button = QPushButton("oo")
        self.link_button.setMaximumWidth(48)
        self.link_button.released.connect(self.toggle_link)

        self.size_correction_check = QCheckBox("Correct width by doubling the letters per pixel")
        self.size_correction_check.setChecked(True)
        self.size_correction_check.toggled.connect(self.change_letters_per_pixel)

        self.reverse_gradient_check = QCheckBox("Reverse gradient (dark mode)")
        self.reverse_gradient_check.toggled.connect(self.gradient_reversal)


        self.resize_button = QPushButton("Refresh")
        self.resize_button.released.connect(self.resize_image_to_selected_size)

        self.btn_save = QPushButton("Save")
        self.btn_save.released.connect(self.save_file_dialog)

        # Layouts:
        # Left half vertical layout
        vl_left = QVBoxLayout()
        vl_left.addWidget(self.result_text)
        vl_left.addWidget(self.font_slider)

        # Open file horizontal layout
        hl_open_file = QHBoxLayout()
        hl_open_file.addWidget(self.path_text)
        hl_open_file.addWidget(self.btn_open)

        # Size hl
        hl_size = QHBoxLayout()
        hl_size.addWidget(self.width_selector)
        hl_size.addWidget(self.link_button)
        hl_size.addWidget(self.height_selector)

        # Right half vertical layout
        vl_right = QVBoxLayout()
        vl_right.addLayout(hl_open_file)
        vl_right.addLayout(hl_size)
        vl_right.addWidget(self.size_correction_check)
        vl_right.addWidget(self.reverse_gradient_check)
        vl_right.addWidget(self.resize_button)
        vl_right.addWidget(self.btn_save)

        # Both halves
        entire_layout = QHBoxLayout()
        entire_layout.addLayout(vl_left)
        entire_layout.addLayout(vl_right)

        #grid_layout = QGridLayout()
        #grid_layout.setVerticalSpacing(0)
        #grid_layout.addWidget(self.result_text, 0, 0, 3, 1)
        #grid_layout.addWidget(self.font_slider, 3, 0)
        #grid_layout.addLayout(h_layout_open_file, 0, 1, 1, -1)
        #grid_layout.addWidget(self.width_selector, 1, 1)
        #grid_layout.addWidget(self.link_button, 1, 2)
        #grid_layout.addWidget(self.height_selector, 1, 3)
        #grid_layout.addWidget(self.resize_button, 2, 1)
        #grid_layout.addWidget(self.btn_save, 3, 1, 1, -1)

        container = QWidget()
        container.setLayout(entire_layout)

        self.setMinimumSize(QSize(640, 360))
        self.setCentralWidget(container)

    def open_file_dialog(self):
        path: str = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation),
            "All Files (*);; PNG Files (*.png)"
        )[0]
        print(path)
        self.change_file_path(path)

    def change_file_path(self, path: str):
        if path != '':
            self.file_path = path
            self.path_text.setText(path)
            self.ascii = Asciifier(path)

            if self.ascii.original_image.size[0] > 80:
                self.ascii.resize_image(80, 0)
            elif self.ascii.original_image.size[0] > 81:
                self.ascii.resize_image(0, 80)

            link_temp = self.size_is_linked
            self.size_is_linked = False
            self.width_selector.setValue(self.ascii.img.width)
            self.height_selector.setValue(self.ascii.img.height)
            self.size_is_linked = link_temp

            self.result_text.setText(self.ascii.make_ascii(self.letters_per_pixel))

    def save_file_dialog(self):
        path: str = QFileDialog.getSaveFileName(
            self,
            "Open Image",
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation),
            "All Files (*);; TXT Files (*.txt)"
        )[0]
        if path != "":
            self.ascii.save_to_file(path)

    def set_result_font_size(self, value):
        self.result_text.setStyleSheet("QTextEdit{font-size: %spt;}" % value)

    def resize_image_to_selected_size(self):
        if self.ascii is not None:
            self.ascii.resize_image(self.size.get_int_width(), self.size.get_int_height())
            self.result_text.setText(self.ascii.make_ascii(self.letters_per_pixel))

    def toggle_link(self):
        self.size_is_linked = not self.size_is_linked
        if self.size_is_linked:
            self.link_button.setText("∞")
        else:
            self.link_button.setText("oo")

    def on_width_changed(self, new_width):
        if self.size_is_linked:
            self.size.resize_by_width(new_width)

            self.height_selector.valueChanged.disconnect(self.on_height_changed)
            self.height_selector.setValue(self.size.get_int_height())
            self.height_selector.valueChanged.connect(self.on_height_changed)
        else:
            self.size.width = new_width

    def on_height_changed(self, new_height):
        if self.size_is_linked:
            self.size.resize_by_height(new_height)

            self.width_selector.valueChanged.disconnect(self.on_width_changed)
            self.width_selector.setValue(self.size.get_int_width())
            self.width_selector.valueChanged.connect(self.on_width_changed)
        else:
            self.size.height = new_height

    def change_letters_per_pixel(self, value: bool):
        self.letters_per_pixel = 2 if value else 1

    def gradient_reversal(self):
        self.ascii.reverse_gradient()

    def mouseDoubleClickEvent(self, e):
        print(self.size)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()  # QWidget()
    window.show()

    app.exec()
