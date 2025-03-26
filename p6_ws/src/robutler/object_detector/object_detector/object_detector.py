#Yolo World
from ultralytics import YOLOWorld    #pip install ultralytics

#SAM
from ultralytics import SAM

#Image processing
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
import json
import os



#ROS stuff
from project_interfaces.srv import GetObjectInfo
from project_interfaces.srv import DefineObjectInfo
from geometry_msgs.msg import Point
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseArray



#the following is the ros2 launch command for the realsense camera with user settings
"""
ros2 launch realsense2_camera rs_launch.py 

IF THIS DOES NOT WORK, TRY THE FOLLOWING:
Check if secure boot is disabled in the BIOS or else it will not work!!!

If you want to chance any parameters do it in the launch file and remember to colcon build the package after you have made the changes.

"""

class RealSenseCamera(Node):
    def __init__(self):
        super().__init__('my_subscriber_node')
        
        # Create a subscriber to the topic 
        self.subscription = self.create_subscription(
            Image,  # Message type
            '/camera/camera/aligned_depth_to_color/image_raw',  # Topic name
            self.convert_to_depth_img,  # Callback function
            10  # Queue size
        )
        
         # Create a subscriber to the topic 
        self.subscription = self.create_subscription(
            Image,  # Message type
            '/camera/camera/color/image_raw',  # Topic name
            self.convert_to_color_img,  # Callback function
            10  # Queue size
        )

         # Create a subscriber to the topic 
        self.subscription = self.create_subscription(
            CameraInfo,  # Message type
            '/camera/camera/aligned_depth_to_color/camera_info',  # Topic name
            self.camera_info_callback,  # Callback function
            10  # Queue size
        )
        
        self.subscription  # Prevent unused variable warning
        self.bridge = CvBridge()  

        #Image frames for depth and color
        self.color_img = None
        self.depth_img = None
        self.camera_info = None


        
    def convert_to_depth_img(self, msg):
        try:
            # Convert the ROS Image message to OpenCV image (16-bit single-channel)
            self.depth_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="16UC1")

        except CvBridgeError as e:
            self.get_logger().error(f'Error converting image: {e}')

    def convert_to_color_img(self, msg):
        try:
            # Convert the ROS Image message to an OpenCV image
            color_img_rgb = self.bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")
            
            # Convert RGB to BGR for OpenCV display (OpenCV uses BGR by default)
            self.color_img = cv2.cvtColor(color_img_rgb, cv2.COLOR_RGB2BGR)

        except CvBridgeError as e:
            self.get_logger().error(f'Error converting color image: {e}')

    def camera_info_callback(self, msg):
        self.camera_info = msg.k


class ObjectDetector(Node):
    def __init__(self):
        super().__init__('object_detector')
        self.yolo_world_srv = self.create_service(GetObjectInfo, 'get_object_info_yolo', self.get_object_information_yolo)

        self.image_publisher = self.create_publisher(Image, 'video_frames', 10)

        # Instantiate the RealSenseCamera object
        self.realsense_camera = RealSenseCamera()

        # Create a dictionary to store found objects with relevant information
        self.found_objects = {}

        #Frames for depth and color
        self.depth_frame = None   
        self.color_frame = None
        self.camera_info = None

        #YOLO and SAM results
        self.yolo_results = None
        self.sam_result_img = None
        self.sam_masks = None

        # Publish initial image to GUI
        self.retrieve_aligned_frames()
        image = self.get_color_image()
        self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(cv2.rotate(image, cv2.ROTATE_180)))


    def retrieve_aligned_frames(self):      
        # Retrieve aligned frames from the RealSense camera by spinning the node untill new frames are available

        while self.realsense_camera.depth_img is None or self.realsense_camera.color_img is None or self.realsense_camera.camera_info is None:
                rclpy.spin_once(self.realsense_camera)

        while np.array_equal(self.realsense_camera.depth_img, self.depth_frame) or np.array_equal(self.realsense_camera.color_img, self.color_frame):
                rclpy.spin_once(self.realsense_camera)
        
        self.depth_frame = self.realsense_camera.depth_img
        self.color_frame = self.realsense_camera.color_img
        self.camera_info = self.realsense_camera.camera_info
    
    
    #The callback function for the detector service for YOLO World
    def get_object_information_yolo(self, request, response):
        object = request.object_name
        self.get_logger().info(f'Requested to find {object} with Yolo World\n')

        self.retrieve_aligned_frames()
        image = self.get_color_image()
        image = cv2.rotate(image, cv2.ROTATE_180)

        #Apply Yolo World, data is stored in self.yolo_results
        self.apply_yolo_world(image, object, verbose=False)

        if len(self.yolo_results[0].boxes.data) == 0:
            self.get_logger().info(f'No {object} found\n')
            self.apply_yolo_world(image, object, verbose=False, name_objects = True)
            image = self.yolo_results[0].plot()
            self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(image))
            response.object_count = 0
            return response

        for i in range(len(self.yolo_results[0].boxes.data)):
            x_min, y_min, x_max, y_max, _, _ = self.yolo_results[0].boxes.data[i]  #confidence and class
            response.object_count += 1
            cartesian_coordinates = self.get_cartesian_coordinates(int((x_min + x_max) / 2), int((y_min + y_max) / 2))
            #print(cartesian_coordinates)
            #print(type(cartesian_coordinates))
            point = Point()
            point.x = float(cartesian_coordinates[0])
            point.y = float(cartesian_coordinates[1])
            point.z = float(cartesian_coordinates[2])
            response.centers.append(point)
            response.orientations.append(0)
            response.grasp_widths.append(min(x_max - x_min, y_max - y_min))
 

        image_with_bbx = self.yolo_results[0].plot()

        self.get_logger().info(f'Found {response.object_count} {object}\n')

        self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(image_with_bbx))

        #SAM prediction on one object
        if (len(self.yolo_results[0].boxes.data)) == 1:
            self.SAM_predict(image, bboxes=[x_min, y_min, x_max, y_max]) #updates sam_result_img and sam_masks
        
        #GRASP Prediction 6D 



        return response
    
    def SAM_predict(self, img, points = None, bboxes=None, labels = None, **kwargs):
        sam = SAM("sam_b.pt")

        # Stream True= you get predictions as they come, False = all at once better if realtime is not important!!
        # Labels define if a point is in the foreground[1] or background[0],
        # bboxes = [[x_min, y_min, x_max, y_max]]
        # points = [[x, y]] 
        # kwargs = can be additional arguments: mask_threshold=0.7, iou_threshold=0.5
        # info here: https://docs.ultralytics.com/reference/models/sam/model/#ultralytics.models.sam.model.SAM.info
        results = sam.predict(img, stream=False, bboxes=bboxes, points=points, labels=labels,**kwargs)
        
        # for plot(options)= https://docs.ultralytics.com/reference/engine/results/#ultralytics.engine.results.Results.plot
        self.sam_result_img = results[0].plot(conf=True,
                                            line_width=None,
                                            font_size=None,
                                            labels=True,
                                            boxes=True,
                                            masks=True,
                                            probs=True) 
        
        # Publish the image to the GUI
        self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(self.sam_result_img))
        
        masks = results[0].masks.data.cpu().numpy()  # Convert to NumPy format

        for i, mask in enumerate(results[0].masks.data):  
            mask = masks[i]  

            # Convert mask to 8-bit format for OpenCV
            mask = (mask * 255).astype(np.uint8)
            self.sam_masks.append(mask)

    def grasp_prediction(self, img, points = None, bboxes=None, labels = None, **kwargs):
        #TODO  
        pass

   
    def show_depth_map(self):
        cv2.namedWindow("Depth Map", cv2.WINDOW_AUTOSIZE)

        while True:
            self.retrieve_aligned_frames()

            # Convert the depth frame to a NumPy array
            depth_image = np.asanyarray(self.depth_frame)

            #depth_image = cv2.rotate(depth_image, cv2.ROTATE_180)

            if True: #True: gets a tresholded colormap. False all depth data are used in normalisation
                # Define the depth range (in millimeters) to display
                min_depth = 0  # Minimum depth to display  0 m
                max_depth = 3000  # Maximum depth to display 3m

                # 1. Threshold the depth image to the specified range
                # Set values outside the range to 0 (this can be chanced if needed).
                depth_image = np.where((depth_image >= min_depth) & (depth_image <= max_depth),depth_image, 0)

            # Normalize the depth image for display
            depth_image = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX)
            depth_image = np.uint8(depth_image)

            # Apply a colormap to the depth image
            depth_colormap = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)

            # Show the depth map using OpenCV's imshow
            cv2.imshow("Depth Map", depth_colormap)

            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
        cv2.destroyAllWindows()
        
    def show_frame(self):
        cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)
        while True:
            self.retrieve_aligned_frames()

            # Convert the frame to a NumPy array for OpenCV
            color_frame = self.get_color_image()

            # Show the frame using OpenCV's imshow
            cv2.imshow("Image", cv2.rotate(color_frame, cv2.ROTATE_180))

            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def get_color_image(self):
        return np.asanyarray(self.color_frame)

    def show_image(self, image):
        cv2.imshow("Image", cv2.rotate(image, cv2.ROTATE_180))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def apply_yolo_world(self, img, object_name, name_objects = False, verbose = False):
        model = YOLOWorld("yolov8l-world.pt")  # or select yolov8{s/m/l}-world.pt for different sizes

        if name_objects == False:
            model.set_classes([object_name])

        # Execute inference with the YOLOv8l-world model on the specified image
        self.yolo_results = model.predict(img)

        #the following prints the results of the yolo model without the class contrains
        if name_objects:
            objects_found = []
            for i in range(len(self.yolo_results[0].boxes.data)):
                objects_found.append(model.names[int(self.yolo_results[0].boxes.data[i][5])])

            self.get_logger().info(f'No {object_name} were found, but a {objects_found} was located.\n')

    

    def get_cartesian_coordinates(self, pixel_x, pixel_y):
        # The camera info message .K contains the camera intrinsics
        #[ fx   0  cx ]
        #[  0  fy  cy ]
        #[  0   0   1 ]

        # Get the camera intrinsics
        fx = self.camera_info[0]
        fy = self.camera_info[4]
        cx = self.camera_info[2]
        cy = self.camera_info[5]

        if pixel_x < 0 or pixel_x >= self.depth_frame.shape[1] or pixel_y < 0 or pixel_y >= self.depth_frame.shape[0]:
            print("Pixel coordinates out of bounds.")
            return None
        
        if self.depth_frame[pixel_y, pixel_x] == 0:
            print("No depth data available at the selected pixel.")
            return None

        print(f"size of depth frame: {self.depth_frame.shape}")

        # Calculate the x, y, z coordinates
        z = self.depth_frame[pixel_y, pixel_x] / 1000  # Convert to meters
        x = ((pixel_x - cx) * z / fx) 
        y = ((pixel_y - cy) * z / fy) 
        

        return np.array([x, y, z])
        
    def show_cartesian_coordinates(self):
        self.retrieve_aligned_frames()
        color_image = self.get_color_image()

        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_MOUSEMOVE:
                # Adjust the x, y coordinates to reflect a rotated image
                height, width, _ = color_image.shape
                adjusted_x = width - x
                adjusted_y = height - y
                coordinates = self.get_cartesian_coordinates(adjusted_x, adjusted_y)
                if coordinates is not None:
                    print(f"Cartesian coordinates at ({x}, {y}): {coordinates}")

        cv2.namedWindow("Image with Coordinates")
        cv2.setMouseCallback("Image with Coordinates", mouse_callback)

    
        while True:
            cv2.imshow("Image with Coordinates", cv2.rotate(color_image, cv2.ROTATE_180))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()



    def get_user_input(self, prompt):
        """
        Use console input instead of GUI input for simplicity.
        """
        while True:
            try:
                user_input = int(input(prompt))
                return user_input
            except ValueError:
                print("Invalid input. Please enter a number.")

    def save_image(self, save_folder="captured_images"):
        """
        Captures and saves an image in a specified folder with an incremented filename.
        """
        # Ensure the save folder exists
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Retrieve the current frame
        self.retrieve_aligned_frames()
        image = self.get_color_image()

        if image is None:
            print("Failed to capture image from camera.")
            return

        # Find the next available file name
        existing_files = [f for f in os.listdir(save_folder) if f.endswith(".jpg")]
        next_index = len(existing_files) + 1
        file_name = f"image_{next_index}.jpg"
        file_path = os.path.join(save_folder, file_name)

        # Save the image
        cv2.imwrite(file_path, cv2.rotate(image, cv2.ROTATE_180))  # Rotate if needed
        print(f"Image saved: {file_path}")


def main(args=None):
    rclpy.init(args=args)

    # Create an ObjectDetector instance
    detector = ObjectDetector()


    #this was commented out
    rclpy.spin(detector) 

    rclpy.shutdown()


if __name__ == '__main__':
    main()