from project_interfaces.srv import GetImage
import rclpy
from rclpy.node import Node

import cv2
from cv_bridge import CvBridge


class ImageCaptureClient(Node):
    def __init__(self):
        super().__init__('minimal_image_client')
        self.cli = self.create_client(GetImage, 'get_image_from_rviz')
        self.bridge = CvBridge()

        self.req = GetImage.Request()

    def send_request(self):
        self.req.execute = True
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)

        image = self.bridge.imgmsg_to_cv2(self.future.result().image, desired_encoding='bgr8')
        return image


def main(args=None):
    rclpy.init(args=args)

    minimal_image_client = ImageCaptureClient()

    response = minimal_image_client.send_request()

    # Remember to remove these lines, as we don't want to visualise the image in the final version.
    cv2.imshow('Image Captured', response)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    minimal_image_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()