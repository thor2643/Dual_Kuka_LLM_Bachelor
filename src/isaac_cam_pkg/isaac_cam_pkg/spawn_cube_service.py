import rclpy
from rclpy.node import Node
from project_interfaces.srv import SpawnCube


class SpawnCubeService(Node):
    def __init__(self):
        super().__init__('isaac_cube_spawner')
        self.service = self.create_service(SpawnCube, '/spawn_cube', self.handle_spawn_request)
        self.get_logger().info("✅ Spawn Cube Service is running...")

    def handle_spawn_request(self, request, response):
        self.get_logger().info(f"Received request to spawn cube at ({request.x}, {request.y}, {request.z}) with size {request.size}")
        response.success = True
        response.message = f"Cube spawned at ({request.x}, {request.y}, {request.z}) with size {request.size}"
        return response

def main(args=None):
    rclpy.init(args=args)
    node = SpawnCubeService()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
