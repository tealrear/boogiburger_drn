import rclpy, cv2, json, threading, queue, numpy as np
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String
from ultralytics import YOLO


class ObjectDetectionNode(Node):
    def __init__(self):
        super().__init__('object_detection_node')

        self.model = YOLO("yolov8n.pt")
        self.img_queue = queue.Queue(maxsize=1)

        self.sub = self.create_subscription(
            CompressedImage,
            '/image_raw/compressed',
            self.image_callback,
            10
        )

        self.pub = self.create_publisher(
            String,
            '/detected_objects',
            10
        )

        threading.Thread(
            target=self.inference_worker,
            daemon=True
        ).start()

    def image_callback(self, msg):
        if self.img_queue.empty():
            self.img_queue.put(msg)

    def inference_worker(self):
        while rclpy.ok():
            try:
                msg = self.img_queue.get(timeout=1.0)
                np_arr = np.frombuffer(msg.data, np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                results = self.model(frame)

                data = [
                    {
                        "class": self.model.names[int(b.cls[0])],
                        "bbox": b.xyxy[0].tolist()
                    }
                    for r in results
                    for b in r.boxes
                ]

                self.pub.publish(String(data=json.dumps(data)))

            except queue.Empty:
                continue


def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetectionNode()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
