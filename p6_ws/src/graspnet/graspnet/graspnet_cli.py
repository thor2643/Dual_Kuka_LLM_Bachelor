from project_interfaces.srv import GetObjectInfo
from project_interfaces.msg import Grasp6D, DetectedObject, TransformMatrix
import rclpy
from rclpy.node import Node


class GraspClient(Node):
    def __init__(self):
        super().__init__('minimal_grasp_client')
        self.cli = self.create_client(GetObjectInfo, 'get_grasp_anygrasp')

        self.req = GetObjectInfo.Request()

    def send_request(self):
        self.req.gripper = "right"
        self.req.object_name = "book"
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        
        results = self.future.result()
        return results


def main(args=None):
    rclpy.init(args=args)
    minimal_grasp_client = GraspClient()
    response = minimal_grasp_client.send_request()
    print(response.object_count)
    print(response.detected_objects)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
