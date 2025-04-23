import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2  # Use this for accessing point cloud data

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        self.subscription = self.create_subscription(
            PointCloud2,
            '/depth_data',  # Replace with the actual topic from Isaac Sim
            self.callback,
            10)
        self.get_logger().info("✅ Camera Subscriber Node Started!")

    def callback(self, msg):
        self.get_logger().info(f"✅ Received PointCloud with {msg.width} points.")

        # Unpack just the first 5 points to make sure it looks good
        from sensor_msgs_py import point_cloud2
        gen = point_cloud2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True)
        
        for i, pt in enumerate(gen):
            self.get_logger().info(f"🔹 Point {i}: x={pt[0]:.3f}, y={pt[1]:.3f}, z={pt[2]:.3f}")
            if i >= 4:
                break



def main(args=None):
    rclpy.init(args=args)
    node = CameraSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
