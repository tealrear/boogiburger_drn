import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import json

class VisualizerNode(Node):
    def __init__(self):
        super().__init__('visualizer')
        self.bridge = CvBridge()
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        self.bbox_sub = self.create_subscription(
            String,
            '/detected_objects',
            self.bbox_callback,
            10
        )
        self.frame = None
        self.bboxes = []

    def image_callback(self, msg):
        self.frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.show_image()

    def bbox_callback(self, msg):
        data = json.loads(msg.data)
        self.bboxes = [data['bbox']] if 'bbox' in data else []
        self.show_image()

    def show_image(self):
        if self.frame is None:
            return

        img = self.frame.copy()
        # bbox 그리기
        for bbox in self.bboxes:
            x1, y1, x2, y2 = bbox
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.imshow("Camera + BBox", img)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = VisualizerNode()
    rclpy.spin(node)
    node.destroy_node()
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
