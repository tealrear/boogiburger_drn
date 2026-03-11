import sys
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np
import json

class CameraGUI(Node):
    def __init__(self):
        super().__init__('camera_gui')
        self.bridge = CvBridge()

        # 카메라 이미지 구독
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # 객체 bbox 구독 (예: JSON 형태)
        self.bbox_sub = self.create_subscription(
            # 실제로는 String 메시지로 bbox 수신
            # {"bboxes":[{"coords":[x1,y1,x2,y2],"label":"person"}]}
            Image,  # 필요시 String으로 바꾸세요
            '/detected_objects',
            self.bbox_callback,
            10
        )

        self.frame = None
        self.bboxes = []

        # PyQt5 GUI 초기화
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QLabel("Waiting for camera...")
        self.window.resize(640, 480)
        self.window.setAlignment(QtCore.Qt.AlignCenter)
        self.window.show()

        # Timer로 GUI 업데이트
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(30)  # 30ms -> 약 33fps

    def image_callback(self, msg):
        self.frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

    def bbox_callback(self, msg):
        # 실제로는 String 메시지로 bbox 수신
        try:
            data = json.loads(msg.data)
            self.bboxes = data.get('bboxes', [])
        except Exception:
            self.bboxes = []

    def update_gui(self):
        if self.frame is None:
            return

        img = self.frame.copy()
        # bbox 그리기
        for bbox in self.bboxes:
            x1, y1, x2, y2 = bbox['coords']
            label = bbox.get('label', '')
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 1)

        # OpenCV BGR -> RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img.shape
        qimg = QtGui.QImage(img.data, w, h, ch * w, QtGui.QImage.Format_RGB888)
        self.window.setPixmap(QtGui.QPixmap.fromImage(qimg))

    def run(self):
        sys.exit(self.app.exec_())

def main(args=None):
    rclpy.init(args=args)
    node = CameraGUI()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
