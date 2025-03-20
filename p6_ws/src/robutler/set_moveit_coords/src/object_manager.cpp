#include <rclcpp/rclcpp.hpp>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/msg/collision_object.hpp>
#include <moveit_msgs/msg/attached_collision_object.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <shape_msgs/msg/solid_primitive.hpp>

#include <ament_index_cpp/get_package_share_directory.hpp>
#include <tinyxml2.h>
#include <vector>
#include <string>

// This class is a simple wrapper around the MoveIt PlanningSceneInterface
// It provides methods to add and remove objects from the planning scene
class ObjectManager : public rclcpp::Node {
    public:
        ObjectManager() : Node("object_manager") {
            planning_scene_interface_ = std::make_shared<moveit::planning_interface::PlanningSceneInterface>();
        }

        // Following this format, we should be able to add any shape from shape_msgs::msg::SolidPrimitive
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

        void addCircle(const std::string &id, const geometry_msgs::msg::PoseStamped &pose, const std::vector<double> &size) {
            moveit_msgs::msg::CollisionObject circle;
            circle.id = id;
            circle.header = pose.header;
            circle.primitives.resize(1);
            circle.primitives[0].type = shape_msgs::msg::SolidPrimitive::SPHERE;
            circle.primitives[0].dimensions.assign(size.begin(), size.end());

            circle.primitive_poses.push_back(pose.pose);
            circle.operation = moveit_msgs::msg::CollisionObject::ADD;

            planning_scene_interface_->applyCollisionObject(circle);
            RCLCPP_INFO(this->get_logger(), "Added object %s", id.c_str());
        }

        // Not used in this script, but can be used to remove objects if the ID is known.
        void removeBox(const std::string &id) {
            planning_scene_interface_->removeCollisionObjects({id});
            RCLCPP_INFO(this->get_logger(), "Removed object %s", id.c_str());
        }

        void clearPlanningScene() {
            auto objects = planning_scene_interface_->getKnownObjectNames();
            planning_scene_interface_->removeCollisionObjects(objects);
            RCLCPP_INFO(this->get_logger(), "Cleared planning scene, removed %ld objects", objects.size());
        }

    private:
        std::shared_ptr<moveit::planning_interface::PlanningSceneInterface> planning_scene_interface_;
};

// Function to parse XML and add objects to planning scene
void parseXMLAndSpawnObjects(const std::string &selected_task, int selected_scenario, 
    std::shared_ptr<ObjectManager> node) {

    std::string file_path = ament_index_cpp::get_package_share_directory("set_moveit_coords") + "/config/" + "cellsetups.xml";

    tinyxml2::XMLDocument doc;
    doc.LoadFile(file_path.c_str());
    tinyxml2::XMLElement *root = doc.FirstChildElement("gpx");

    // Massive sanity check to ensure the user knows which tasks and scenarios are available:
    std::map<std::string, std::set<int>> task_scenario_map;
    bool task_found = false;
    bool scenario_found = false;

    // Parse available tasks and scenarios
    for (tinyxml2::XMLElement *trk = root->FirstChildElement("trk"); trk; trk = trk->NextSiblingElement("trk")) {
        tinyxml2::XMLElement *taskElement = trk->FirstChildElement("Task");
        tinyxml2::XMLElement *scenarioElement = trk->FirstChildElement("Scenario");

        if (!taskElement || !scenarioElement) {
            continue;  // Skip invalid entries
        }

        std::string task = taskElement->GetText();
        int scenario = scenarioElement->IntText();

        task_scenario_map[task].insert(scenario);

        if (task == selected_task) {
            task_found = true;
            if (scenario == selected_scenario) {
                scenario_found = true;
            }
        }
    }

    // If the task or scenario is invalid, print all available options and exit
    if (!task_found || !scenario_found) {
        RCLCPP_ERROR(node->get_logger(), "Invalid task or scenario.");
        RCLCPP_ERROR(node->get_logger(), "Available tasks and their scenarios:");

        for (const auto &task_entry : task_scenario_map) {
            std::string task_name = task_entry.first;
            std::string scenario_list;
            for (int scenario : task_entry.second) {
                scenario_list += std::to_string(scenario) + " ";
            }
            RCLCPP_ERROR(node->get_logger(), "  - %s: [%s]", task_name.c_str(), scenario_list.c_str());
        }

        return;
    }
    // NOTE: Sanity check ends here

    // Remove any existing objects - Used when running the script multiple times
    node->clearPlanningScene();

    int obj_id = 0;
    for (tinyxml2::XMLElement *trk = root->FirstChildElement("trk"); trk; trk = trk->NextSiblingElement("trk")) {
        // Read the Task and Scenario
        tinyxml2::XMLElement *taskElement = trk->FirstChildElement("Task");
        tinyxml2::XMLElement *scenarioElement = trk->FirstChildElement("Scenario");

        std::string task = taskElement->GetText();
        int scenario = scenarioElement->IntText();

        // Check if the task and scenario match the user input.
        if (task != selected_task || scenario != selected_scenario) {
            continue;  // Skip this <trk> if it doesn't match the user input - Not the most optimal solution?
        }

        // Check if the task and scenario are defined, if not inform the user of their options and exit.
        if (task == "" || scenario == 0) {
            RCLCPP_ERROR(node->get_logger(), "Task or Scenario not defined in XML file.");
            return;
        }

        // Parse and add objects
        for (tinyxml2::XMLElement *trkpt = trk->FirstChildElement("trkpt"); trkpt; trkpt = trkpt->NextSiblingElement("trkpt")) {
            // Start by retrieving the object type and pose, needed for all object types.
            std::string type = trkpt->Attribute("type");
            double x = trkpt->DoubleAttribute("x");
            double y = trkpt->DoubleAttribute("y");
            double z = trkpt->DoubleAttribute("z");
            double w = trkpt->DoubleAttribute("w");
            
            geometry_msgs::msg::PoseStamped pose;
            pose.header.frame_id = "world";
            pose.pose.position.x = x;
            pose.pose.position.y = y;
            pose.pose.position.z = z;
            pose.pose.orientation.w = w;

            // Recive type specific attributes and add the object to the planning scene
            if (type == "box") {
                double a = trkpt->DoubleAttribute("a");
                double b = trkpt->DoubleAttribute("b");
                double h = trkpt->DoubleAttribute("h");
                node->addBox("box_" + std::to_string(obj_id++), pose, {a, b, h});
            }
            if (type == "circle") {
                double r = trkpt->DoubleAttribute("r");
                node->addCircle("circle_" + std::to_string(obj_id++), pose, {r});
            }
        }
    }
}


// To the best of my knowlage, x = 0.035, y = 0.035 & z = 0.86 is the absoulute closet we can get to the "0,0,0 edge" - Oversized collision boxes?
// - Values above are for a box with size 0.1, 0.1, 0.1, so scale accordingly. (a, b, h - Rectangle)
int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<ObjectManager>();

    // Ensure the user has provided the correct arguments.
    if (argc < 3) {
        RCLCPP_ERROR(node->get_logger(), "Usage: object_manager <task_name> <scenario_number>");
        return 1;
    }

    std::string task_name = argv[1];
    int scenario_number = std::stoi(argv[2]);

    parseXMLAndSpawnObjects(task_name, scenario_number, node);

    rclcpp::shutdown();
    return 0;
}