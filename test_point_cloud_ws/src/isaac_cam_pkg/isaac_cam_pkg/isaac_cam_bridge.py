import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from project_interfaces.srv import GetSimCameraData

class IsaacCameraBridge(Node):
    def __init__(self):
        super().__init__('isaac_camera_bridge')

        # Create service
        self.service = self.create_service(
            GetSimCameraData,
            '/get_simulated_camera_data',
            self.handle_get_camera_data
        )

        # Subscribed image streams from Isaac Sim
        self.color_img = None
        self.depth_img = None

        self.color_sub = self.create_subscription(Image, '/rgb_image', self.color_callback, 10)
        self.depth_sub = self.create_subscription(Image, '/depth_image', self.depth_callback, 10)

        self.get_logger().info("IsaacCameraBridge initialized and listening to Isaac Sim topics.")

    def color_callback(self, msg):
        self.color_img = msg

    def depth_callback(self, msg):
        self.depth_img = msg

    def handle_get_camera_data(self, request, response):
        if self.color_img is None or self.depth_img is None:
            self.get_logger().warn("No camera images received yet.")
            return response

        # Attach latest images
        response.color_image = self.color_img
        response.depth_image = self.depth_img

        camera_info = CameraInfo()

        # Depth intrinsics:
        camera_info.k = [
            652.79352, 0.0,   640.0,
            0.0,    359.16418, 360.0,
            0.0,    0.0,   1.0
        ]
        
        # RGB intrinsics:
        """
        camera_info.k = [
            634.0862399675711, 0.0,   640.0,
            0.0,    634.0862399675711, 360.0,
            0.0,    0.0,   1.0
        ]
        """
        # Old:
        """
            camera_info.k = [
            634.22, 0.0,   640.0,
            0.0,    566.44, 360.0,
            0.0,    0.0,   1.0
        ]
        """
        response.camera_info = camera_info

        self.get_logger().info("Responded with latest simulated camera data.")
        return response

def main(args=None):
    rclpy.init(args=args)
    node = IsaacCameraBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
