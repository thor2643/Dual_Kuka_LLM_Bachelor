# Imports for image capturing & processing
import cv2
import numpy as np
import pyautogui
from cv_bridge import CvBridge

# Imports for ROS2
import rclpy
from rclpy.node import Node

# Imports for ROS2 messages
from project_interfaces.srv import GetImage

class ImageCaptureService(Node):
    def __init__(self):
        super().__init__('easy_image_capture')
        self.srv = self.create_service(GetImage, 'get_image_from_rviz', self.take_image)
        self.bridge = CvBridge()

    def take_image(self, request, response):
        img = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Determine the location of the simulation window, and crop the image to that location
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Threshold the image to get a binary image (white pixels become white, others become black)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        thresh = cv2.bitwise_not(thresh)

        # Find contours & choose the largest contour (the simulation window)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = max(contours, key=cv2.contourArea)

        # Get bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Cut the image to the bounding box
        img = img[y:y+h, x:x+w]

        # Use rosbridge to convert the image to a ROS2 message    
        ros_image = self.bridge.cv2_to_imgmsg(img, encoding="bgr8")

        response.log = 'Image Captured Successfully'
        response.image = ros_image

        return response


def main(args=None):
    rclpy.init(args=args)

    easy_image_capture = ImageCaptureService()

    rclpy.spin(easy_image_capture)

    rclpy.shutdown()

if __name__ == "__main__":
    main()