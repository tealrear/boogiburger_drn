import sys, rclpy, cv2, numpy as np
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import QRect, QTimer
from PySide6.QtGui import QImage, QPixmap


class Ui_Form(object):
    def setupUi(self, Form):
        Form.resize(400, 350)
        self.video_label = QLabel(Form)
        self.video_label.setGeometry(QRect(20, 10, 320, 320))
        self.video_label.setText("Loading...")


class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.node = Node('camera_ui_node')

        self.subscription = self.node.create_subscription(
            CompressedImage,
            '/image_raw/compressed',
            self.image_callback,
            10
        )

        self.timer = QTimer()
        self.timer.timeout.connect(
            lambda: rclpy.spin_once(self.node, timeout_sec=0)
        )
        self.timer.start(66)

    def image_callback(self, msg):
        try:
            # 1. 압축 데이터 변환
            arr = np.frombuffer(msg.data, np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if img is None:
                return

            # 2. GUI용 변환 (BGR to RGB)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, ch = img.shape

            # 3. 중요: bytes()로 복사하여 메모리 안전성 확보
            qimg = QImage(bytes(img.data), w, h, ch * w, QImage.Format_RGB888)
            self.ui.video_label.setPixmap(QPixmap.fromImage(qimg))
        except Exception as e:
            # 오류 무시 (개발 시에는 로깅 권장)
            pass


def main(args=None):
    rclpy.init(args=args)
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()

    try:
        sys.exit(app.exec())
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
