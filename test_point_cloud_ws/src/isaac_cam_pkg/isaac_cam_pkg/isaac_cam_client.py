import rclpy
from rclpy.node import Node
from project_interfaces.srv import SendDepthData
from project_interfaces.srv import SendRGBData

class IsaacCamClient(Node):
    def __init__(self):
        super().__init__('isaac_cam_client')

        self.depth_client = self.create_client(SendDepthData, 'send_depth_data')
        self.rgb_client = self.create_client(SendRGBData, 'send_rgb_data')

        self.send_both_requests()

    def send_both_requests(self):
        self.get_logger().info("🔎 Checking availability of both services...")

        def check_services():
            depth_ready = self.depth_client.wait_for_service(timeout_sec=0.1)
            rgb_ready = self.rgb_client.wait_for_service(timeout_sec=0.1)

            if not depth_ready:
                self.get_logger().info("⏳ Waiting for /send_depth_data service...")
            if not rgb_ready:
                self.get_logger().info("⏳ Waiting for /send_rgb_data service...")

            if depth_ready and rgb_ready:
                self.get_logger().info("✅ Both services available. Sending requests...")

                # Send depth request
                depth_req = SendDepthData.Request()
                self.depth_future = self.depth_client.call_async(depth_req)

                # Send rgb request
                rgb_req = SendRGBData.Request()
                self.rgb_future = self.rgb_client.call_async(rgb_req)

                self.create_timer(0.5, self.check_response)
                return True
            return False

        # Poll every 0.5 seconds until both are ready
        self.timer = self.create_timer(0.5, lambda: self._try_start(check_services))

    def _try_start(self, checker):
        if checker():
            self.timer.cancel()

    def check_response(self):
        if hasattr(self, 'depth_future') and self.depth_future.done():
            response = self.depth_future.result()
            self.get_logger().info(f"Depth Response: {response.message}")
            del self.depth_future

        if hasattr(self, 'rgb_future') and self.rgb_future.done():
            response = self.rgb_future.result()
            self.get_logger().info(f"RGB Response: {response.message}")
            del self.rgb_future

        # If both are done, shut down
        if not hasattr(self, 'depth_future') and not hasattr(self, 'rgb_future'):
            self.get_logger().info("✅ Done triggering both services")
            rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = IsaacCamClient()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
