from project_interfaces.srv import GetGrasp
import rclpy
from rclpy.node import Node

import logging
logging.getLogger().setLevel(logging.ERROR) # Supress warnings


class GraspClient(Node):
    def __init__(self):
        super().__init__('minimal_grasp_client')
        self.cli = self.create_client(GetGrasp, 'get_grasp_anygrasp')

        self.req = GetGrasp.Request()

    def send_request(self):
        self.req.request = True
        self.req.gripper = "right"
        self.req.object_name = "book"
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        
        results = self.future.result().grasp_candidates
        return results


def main(args=None):
    rclpy.init(args=args)
    minimal_grasp_client = GraspClient()
    response = minimal_grasp_client.send_request()
    print(response)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
