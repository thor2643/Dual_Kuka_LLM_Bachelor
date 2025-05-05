import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np
import cv2

class RGBSubscriber(Node):
    def __init__(self):
        super().__init__('rgb_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/rgb_image',
            self.listener_callback,
            10)
        self.get_logger().info("RGB Subscriber Node Started!")

    def listener_callback(self, msg):
        # Convert bytes to numpy array
        img_array = np.frombuffer(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, 3))
        
        # Optionally convert from RGB to BGR if you want accurate OpenCV colors
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Display the image
        cv2.imshow('RGB Image', img_bgr)
        cv2.waitKey(1)  # Needed to refresh the OpenCV window

def main(args=None):
    rclpy.init(args=args)
    node = RGBSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
