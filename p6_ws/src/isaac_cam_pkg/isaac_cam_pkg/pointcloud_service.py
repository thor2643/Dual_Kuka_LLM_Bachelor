import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_srvs.srv import Trigger

class PointCloudService(Node):
    def __init__(self):
        super().__init__('pointcloud_service')

        self.subscription = self.create_subscription(
            PointCloud2,
            '/depth_data',
            self.pointcloud_callback,
            10
        )

        self.publisher = self.create_publisher(PointCloud2, '/filtered_depth_data', 10)
        self.service = self.create_service(Trigger, 'send_pointcloud', self.handle_request)

        self.latest_msg = None
        self.get_logger().info("PointCloud relay ready (waiting for service calls)")

    def pointcloud_callback(self, msg):
        self.latest_msg = msg

    def handle_request(self, request, response):
        if self.latest_msg:
            self.publisher.publish(self.latest_msg)
            response.success = True
            response.message = "✅ Published latest point cloud to /filtered_depth_data"
        else:
            response.success = False
            response.message = "❌ No point cloud received yet from /depth_data"
        return response

def main(args=None):
    rclpy.init(args=args)
    node = PointCloudService()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
