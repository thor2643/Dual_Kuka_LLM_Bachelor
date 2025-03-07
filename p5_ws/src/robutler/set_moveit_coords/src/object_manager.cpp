#include <rclcpp/rclcpp.hpp>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/msg/collision_object.hpp>
#include <moveit_msgs/msg/attached_collision_object.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <shape_msgs/msg/solid_primitive.hpp>

// This class is a simple wrapper around the MoveIt PlanningSceneInterface
// It provides methods to add and remove objects from the planning scene
class ObjectManager : public rclcpp::Node {
    public:
        ObjectManager() : Node("object_manager") {
            planning_scene_interface_ = std::make_shared<moveit::planning_interface::PlanningSceneInterface>();
        }

        void addBox(const std::string &id, const geometry_msgs::msg::PoseStamped &pose, const std::vector<double> &size) {
            moveit_msgs::msg::CollisionObject box;
            box.id = id;
            box.header = pose.header;
            box.primitives.resize(1);
            box.primitives[0].type = shape_msgs::msg::SolidPrimitive::BOX;
            box.primitives[0].dimensions.assign(size.begin(), size.end());

            box.primitive_poses.push_back(pose.pose);
            box.operation = moveit_msgs::msg::CollisionObject::ADD;

            planning_scene_interface_->applyCollisionObject(box);
            RCLCPP_INFO(this->get_logger(), "Added object %s", id.c_str());
        }

        void removeBox(const std::string &id) {
            planning_scene_interface_->removeCollisionObjects({id});
            RCLCPP_INFO(this->get_logger(), "Removed object %s", id.c_str());
        }

    private:
        std::shared_ptr<moveit::planning_interface::PlanningSceneInterface> planning_scene_interface_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<ObjectManager>();

    geometry_msgs::msg::PoseStamped pose;
    pose.header.frame_id = "world";
    pose.pose.position.x = 0.5;
    pose.pose.position.y = 0.0;
    pose.pose.position.z = 0.5;
    pose.pose.orientation.w = 1.0;

    node->addBox("test_object", pose, {0.1, 0.1, 0.1});
    rclcpp::sleep_for(std::chrono::seconds(5));
    node->removeBox("test_object");

    rclcpp::shutdown();
    return 0;
}
