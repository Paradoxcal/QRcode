import io
import sys
import qrcode
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox,
    QSpinBox, QPushButton, QFileDialog, QGridLayout
)
from PyQt5.QtGui import QImage, QPixmap

class QRCodeMaker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Generator")
        self.setFixedSize(600, 400)
        self._setup_ui()

    def _setup_ui(self):
        layout = QGridLayout(self)

        # Input content
        layout.addWidget(QLabel("Content:"), 0, 5)
        self.input_text = QLineEdit("USYD")
        layout.addWidget(self.input_text, 0, 6, 1, 3)

        # Version selection
        layout.addWidget(QLabel("Version:"), 1, 5)
        self.version_box = QComboBox()
        for i in range(1, 41):
            self.version_box.addItem(str(i))
        layout.addWidget(self.version_box, 1, 6)

        # Size selection
        layout.addWidget(QLabel("Size:"), 2, 5)
        self.size_box = QComboBox()
        for i in range(8, 40, 2):
            self.size_box.addItem(f"{i*29} * {i*29}")
        layout.addWidget(self.size_box, 2, 6)

        # Margin setting
        layout.addWidget(QLabel("Margin:"), 3, 5)
        self.margin_box = QSpinBox()
        layout.addWidget(self.margin_box, 3, 6)

        # Buttons
        self.btn_generate = QPushButton("Generate QR Code")
        self.btn_save = QPushButton("Save QR Code")
        layout.addWidget(self.btn_generate, 4, 5, 1, 2)
        layout.addWidget(self.btn_save, 5, 5, 1, 2)

        # Image display area
        layout.addWidget(QLabel("Preview:"), 0, 0)
        self.image_label = QLabel()
        self.image_label.setScaledContents(True)
        self.image_label.setMaximumSize(200, 200)
        layout.addWidget(self.image_label, 0, 0, 5, 5)

        # Style sheet
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #d1f0ff, stop:1 #ffffff);
                font-family: Segoe UI, sans-serif;
                font-size: 18px;
            }
            QLineEdit, QComboBox, QSpinBox {
                background: rgba(255, 255, 255, 0.8);
                border: 1px solid #99ccff;
                border-radius: 6px;
                padding: 4px;
            }
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                  stop:0 #ccf2ff, stop:1 #66ccff);
                border: 2px solid #3399cc;
                border-radius: 10px;
                padding: 6px 12px;
                font-weight: bold;
                color: #00334d;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                  stop:0 #e6faff, stop:1 #99e6ff);
                border: 2px solid #33bbee;
            }
            QPushButton:pressed {
                background-color: #66c2ff;
                border: 2px inset #007acc;
            }
            QLabel {
                font-weight: bold;
                color: #00334d;
            }
        """)

        # Signal connections
        self.btn_generate.clicked.connect(self._generate_qr)
        self.btn_save.clicked.connect(self._save_qr)
        self.margin_box.valueChanged.connect(self._generate_qr)

        self._generate_qr()

    def _generate_qr(self):
        content = self.input_text.text()
        size = int(self.size_box.currentText().split("*")[0])
        try:
            margin = int(self.margin_box.text())
        except:
            margin = 0

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size // 29,
            border=margin,
        )
        qr.add_data(content)
        self.qr_image = qr.make_image()

        buffer = io.BytesIO()
        self.qr_image.save(buffer, "BMP")
        img = QImage()
        img.loadFromData(buffer.getvalue(), "BMP")
        self.image_label.setPixmap(QPixmap.fromImage(img))

    def _save_qr(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save", "./qrcode.png", "Images (*.png *.bmp)")
        if path:
            self.qr_image.save(path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeMaker()
    window.show()
    sys.exit(app.exec_())
