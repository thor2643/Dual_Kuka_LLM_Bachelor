#include "geometry_msgs/msg/pose.hpp"
#include "sensor_msgs/msg/joint_state.hpp"
#include "moveit/move_group_interface/move_group_interface.h"
#include "moveit/robot_state/robot_state.h"
#include "moveit/robot_model_loader/robot_model_loader.h"
#include "rclcpp/rclcpp.hpp"
#include "project_interfaces/srv/plan_move_command.hpp"
#include "project_interfaces/srv/execute_move_command.hpp"
#include "project_interfaces/srv/get_current_pose.hpp"
#include "project_interfaces/srv/gripper_moveit.hpp"

//#include <moveit_visual_tools/moveit_visual_tools.h>
#include <string>
#include <sstream>
#include <map>
#include <cmath> 
#include <fstream>
#include <nlohmann/json.hpp>

using namespace Eigen;

class RobotControllerService : public rclcpp::Node{
public:
  RobotControllerService() : Node("robot_controller_service") {
    this->declare_parameter<std::string>("model", "default_model");
    std::string model;
    this->get_parameter("model", model);

    RCLCPP_INFO(this->get_logger(), "Creating MoveGroupInterface for right arm");
    moveit::planning_interface::MoveGroupInterface::Options options_right("right_arm", "robot_description", "");   
    move_group_interface_right = std::make_shared<moveit::planning_interface::MoveGroupInterface>(std::make_shared<rclcpp::Node>(this->get_name()), options_right); 

    RCLCPP_INFO(this->get_logger(), "Creating MoveGroupInterface for left arm");
    moveit::planning_interface::MoveGroupInterface::Options options_left("left_arm", "robot_description", "");
    move_group_interface_left = std::make_shared<moveit::planning_interface::MoveGroupInterface>(std::make_shared<rclcpp::Node>(this->get_name()), options_left);

    RCLCPP_INFO(this->get_logger(), "Creating MoveGroupInterface for 3f gripper");
    moveit::planning_interface::MoveGroupInterface::Options options_3f("3f_gripper", "robot_description", "");
    move_group_3f = std::make_shared<moveit::planning_interface::MoveGroupInterface>(std::make_shared<rclcpp::Node>(this->get_name()), options_3f);

    RCLCPP_INFO(this->get_logger(), "Creating MoveGroupInterface for 2f gripper");
    moveit::planning_interface::MoveGroupInterface::Options options_2f("2f_gripper", "robot_description", "");
    move_group_2f = std::make_shared<moveit::planning_interface::MoveGroupInterface>(std::make_shared<rclcpp::Node>(this->get_name()), options_2f);

    // Fix bug in MoveGroupInterface
    ee_link_right = move_group_interface_right->getEndEffectorLink();
    ee_link_left = move_group_interface_left->getEndEffectorLink();


    RCLCPP_INFO(this->get_logger(), "End effector link for right arm: %s", ee_link_right.c_str());
    RCLCPP_INFO(this->get_logger(), "End effector link for left arm: %s", ee_link_left.c_str());

    auto current_pose_right = move_group_interface_right->getCurrentPose(ee_link_right);
    auto current_pose_left = move_group_interface_left->getCurrentPose(ee_link_left);

    RCLCPP_INFO(this->get_logger(), "Current position for right arm: x=%f, y=%f, z=%f", 
          current_pose_right.pose.position.x, 
          current_pose_right.pose.position.y, 
          current_pose_right.pose.position.z);

    RCLCPP_INFO(this->get_logger(), "Current position for left arm: x=%f, y=%f, z=%f", 
          current_pose_left.pose.position.x, 
          current_pose_left.pose.position.y, 
          current_pose_left.pose.position.z);

    //getPoseReferenceFrame = move_group_interface_right->getPoseReferenceFrame();
    //RCLCPP_INFO(this->get_logger(), "Received request to plan a trajectory");
       
    // Pass the options and the shared pointer of the current node
    planner_service = this->create_service<project_interfaces::srv::PlanMoveCommand>(
        "plan_move_command", std::bind(&RobotControllerService::handle_planner_service, this, std::placeholders::_1, std::placeholders::_2));

    execute_service = this->create_service<project_interfaces::srv::ExecuteMoveCommand>(
        "execute_move_command", std::bind(&RobotControllerService::handle_execute_service, this, std::placeholders::_1, std::placeholders::_2));

    get_pose_service = this->create_service<project_interfaces::srv::GetCurrentPose>(
        "get_pose", std::bind(&RobotControllerService::handle_pose_request_service, this, std::placeholders::_1, std::placeholders::_2));
    
    gripper_service = this->create_service<project_interfaces::srv::GripperMoveit>(
        "gripper_moveit", std::bind(&RobotControllerService::handle_gripper_service, this, std::placeholders::_1, std::placeholders::_2));

    joint_state_subscriber = this->create_subscription<sensor_msgs::msg::JointState>(
      "joint_states", 1, std::bind(&RobotControllerService::joint_state_callback, this, std::placeholders::_1));

  
    // Print the pose
    //RCLCPP_INFO(this->get_logger(), "End effector pose:\n%s", end_effector_state.matrix().format(Eigen::IOFormat()).c_str());
  }

private:
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface_right;
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface_left;
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_3f;
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_2f;
  rclcpp::Service<project_interfaces::srv::PlanMoveCommand>::SharedPtr planner_service;
  rclcpp::Service<project_interfaces::srv::ExecuteMoveCommand>::SharedPtr execute_service;
  rclcpp::Service<project_interfaces::srv::GetCurrentPose>::SharedPtr get_pose_service;
  rclcpp::Service<project_interfaces::srv::GripperMoveit>::SharedPtr gripper_service;
  rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr joint_state_subscriber;
  
  moveit::planning_interface::MoveGroupInterface::Plan plan_right;
  moveit::planning_interface::MoveGroupInterface::Plan plan_left;
  const moveit::core::JointModelGroup* joint_model_group_right;
  const moveit::core::JointModelGroup* joint_model_group_left;
  moveit::core::RobotModelPtr kinematic_model;

  moveit::planning_interface::MoveGroupInterface::Plan plan_3f_closed;
  moveit::planning_interface::MoveGroupInterface::Plan plan_3f_open;
  moveit::planning_interface::MoveGroupInterface::Plan plan_2f_closed;
  moveit::planning_interface::MoveGroupInterface::Plan plan_2f_open;

  sensor_msgs::msg::JointState::SharedPtr current_joint_state;

  std::string ee_link_right;
  std::string ee_link_left;

  bool plan_available_right = false;
  bool plan_available_left = false;

  std::vector<double> joint_values_right;
  std::vector<double> joint_values_left;
  std::vector<double> _3f_joint_values_mock;
  std::vector<double> _2f_joint_values_mock;
  
  void joint_state_callback(const sensor_msgs::msg::JointState::SharedPtr msg)
    {
        //current_joint_state = msg->position;
        joint_values_right.clear();
        joint_values_left.clear();
        _3f_joint_values_mock.clear();
        _2f_joint_values_mock.clear();

        joint_values_right.resize(7);
        joint_values_left.resize(7);
        _3f_joint_values_mock.resize(11);
        _2f_joint_values_mock.resize(3);

        for (size_t i = 0; i < msg->name.size(); ++i) {
            if (msg->name[i].find("right_") != std::string::npos) {
              if (msg->name[i] == "right_A1") joint_values_right[0] = msg->position[i];
              else if (msg->name[i] == "right_A2") joint_values_right[1] = msg->position[i];
              else if (msg->name[i] == "right_A3") joint_values_right[2] = msg->position[i];
              else if (msg->name[i] == "right_A4") joint_values_right[3] = msg->position[i];
              else if (msg->name[i] == "right_A5") joint_values_right[4] = msg->position[i];
              else if (msg->name[i] == "right_A6") joint_values_right[5] = msg->position[i];
              else if (msg->name[i] == "right_A7") joint_values_right[6] = msg->position[i];

            } else if (msg->name[i].find("left_") != std::string::npos) {
              if (msg->name[i] == "left_A1") joint_values_left[0] = msg->position[i];
              else if (msg->name[i] == "left_A2") joint_values_left[1] = msg->position[i];
              else if (msg->name[i] == "left_A3") joint_values_left[2] = msg->position[i];
              else if (msg->name[i] == "left_A4") joint_values_left[3] = msg->position[i];
              else if (msg->name[i] == "left_A5") joint_values_left[4] = msg->position[i];
              else if (msg->name[i] == "left_A6") joint_values_left[5] = msg->position[i];
              else if (msg->name[i] == "left_A7") joint_values_left[6] = msg->position[i];
              else if (msg->name[i] == "left_2f_robotiq_85_left_knuckle_joint") _2f_joint_values_mock[0] = msg->position[i];
              else if (msg->name[i] == "left_2f_robotiq_85_left_finger_tip_joint") _2f_joint_values_mock[1] = msg->position[i];
              else if (msg->name[i] == "left_2f_robotiq_85_left_finger_joint") _2f_joint_values_mock[2] = msg->position[i];
              
            }
            if (msg->name[i].find("a_") != std::string::npos) {
              if (msg->name[i] == "a_3f_palm_finger_1_joint") _3f_joint_values_mock[0] = msg->position[i];
              else if (msg->name[i] == "a_3f_finger_middle_joint_3") _3f_joint_values_mock[1] = msg->position[i];
              else if (msg->name[i] == "a_3f_finger_2_joint_3") _3f_joint_values_mock[2] = msg->position[i];
              else if (msg->name[i] == "a_3f_finger_2_joint_1") _3f_joint_values_mock[3] = msg->position[i];
              else if (msg->name[i] == "a_3f_finger_middle_joint_1") _3f_joint_values_mock[4] = msg->position[i];
              else if (msg->name[i] == "a_3f_finger_2_joint_2") _3f_joint_values_mock[5] = msg->position[i];
              else if (msg->name[i] == "a_3f_palm_finger_2_joint") _3f_joint_values_mock[6] = msg->position[i];
              else if (msg->name[i] == "a_3f_finger_1_joint_3") _3f_joint_values_mock[7] = msg->position[i];
              else if (msg->name[i] == "a_3f_finger_1_joint_1") _3f_joint_values_mock[8] = msg->position[i];
              else if (msg->name[i] == "a_3f_finger_middle_joint_2") _3f_joint_values_mock[9] = msg->position[i];
              else if (msg->name[i] == "a_3f_finger_1_joint_2") _3f_joint_values_mock[10] = msg->position[i];
            }
        }
    }
  
  // Callback to plan the trajectory to the target pose
  void handle_planner_service(const std::shared_ptr<project_interfaces::srv::PlanMoveCommand::Request> request,
                      const std::shared_ptr<project_interfaces::srv::PlanMoveCommand::Response> response) {

    RCLCPP_INFO(this->get_logger(), "Received request to plan a trajectory");

    std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface;
    moveit::planning_interface::MoveGroupInterface::Plan *plan;
    bool *plan_available;
    
    // Joint names
    std::string right_array[7] = {"right_A1", "right_A2", "right_A3", "right_A4", "right_A5", "right_A6", "right_A7"};
    std::string left_array[7] = {"left_A1", "left_A2", "left_A3", "left_A4", "left_A5", "left_A6", "left_A7"};
    // Pointer to point to the chosen array
    //std::string (*linkArray)[7] = nullptr;

    // Check if the request is for the right or left arm
    if (request->arm == "right") {
      RCLCPP_INFO(this->get_logger(), "Planning for right arm");
      move_group_interface = move_group_interface_right;
      plan = &plan_right;
      plan_available = &plan_available_right;
      //linkArray = &right_array;
    } else if (request->arm == "left") {
      RCLCPP_INFO(this->get_logger(), "Planning for left arm");
      move_group_interface = move_group_interface_left;
      plan = &plan_left;
      plan_available = &plan_available_left;
      //linkArray = &left_array;
    } else {
      RCLCPP_ERROR(this->get_logger(), "Invalid arm specified");
      response->log = "Invalid arm specified";
      response->success = false;
      return;
    }

    // Workspace reachability check (XY distance from base of robot to target pose)
    double base_x, base_y;
    double min_reach_threshold = 0.3; // This value prevents the system from planning to locations where objects are too close to the base of the robot.
    double max_reach_threshold = 0.8; // Increase this value to increase the radius that the manipulator can reach objects within.

    if (request->arm == "right") {
      base_x = 0.14518;
      base_y = 0.79431;
    } else {
      base_x = 0.79518;
      base_y = 0.79431;
    }

    double dx = request->position.x - base_x;
    double dy = request->position.y - base_y;
    double distance = std::sqrt(dx * dx + dy * dy);

    if (distance < min_reach_threshold || distance > max_reach_threshold) {
      RCLCPP_ERROR(this->get_logger(), "Target position is out of reach for %s arm (distance: %.3f m)", request->arm.c_str(), distance);
      response->log = "Target position is out of reach for " + request->arm + " arm. Consider using the other arm.";
      response->success = false;
      return;
    }


    // --- Constraint the planner so the end effector link (3f_tool0 and 2f_tool0) is always inside a box ---
    // Link to this constraint code: https://moveit.picknik.ai/main/doc/how_to_guides/using_ompl_constrained_planning/ompl_constrained_planning.html
    moveit_msgs::msg::PositionConstraint box_constraint;
    box_constraint.header.frame_id = move_group_interface->getPoseReferenceFrame(); // This is the link world, as set in the xacro.
    box_constraint.link_name = move_group_interface->getEndEffectorLink(); // Find the end effector link for planner group, which is 3f_tool0 for right arm, and 2f_tool0 for left arm

    // Create the box and set its dimensions
    shape_msgs::msg::SolidPrimitive box;
    box.type = shape_msgs::msg::SolidPrimitive::BOX;  
    box.dimensions = { 1.5, 1.2, 1.2 };
    box_constraint.constraint_region.primitives.emplace_back(box);

    // Set position of the box 
    geometry_msgs::msg::Pose box_pose; 
    box_pose.position.x = 0.465;
    box_pose.position.y = 0.2995;
    box_pose.position.z = 1.40945;
    box_pose.orientation.w = 1; 
    box_constraint.constraint_region.primitive_poses.emplace_back(box_pose); // The box position is at it's center
    box_constraint.weight = 1.0;

    // We make a generic constraint, and add box_constraint to the position_constraints.
    moveit_msgs::msg::Constraints constraints;
    //constraints.position_constraints.emplace_back(box_constraint);

    // Visualize the box constraint
    /*
    auto moveit_visual_tools = moveit_visual_tools::MoveItVisualTools{ node_ptr, "world", rviz_visual_tools::RVIZ_MARKER_TOPIC, move_group_interface.getRobotModel()};
    Eigen::Vector3d box_point_1(box_pose.position.x - box.dimensions[0] / 2, box_pose.position.y - box.dimensions[1] / 2,
                                box_pose.position.z - box.dimensions[2] / 2);
    Eigen::Vector3d box_point_2(box_pose.position.x + box.dimensions[0] / 2, box_pose.position.y + box.dimensions[1] / 2,
                                box_pose.position.z + box.dimensions[2] / 2);
    moveit_visual_tools.publishCuboid(box_point_1, box_point_2, rviz_visual_tools::TRANSLUCENT_DARK);
    moveit_visual_tools.trigger();
    */

    // --- Set joint constraints ---    
    /*
    moveit_msgs::msg::JointConstraint joint_constraint1;
    joint_constraint1.joint_name = (*linkArray)[0]; // The first joint
    joint_constraint1.position = 0.0;       // Center of the allowed range
    joint_constraint1.tolerance_above = 0;  // +0 degrees in radians
    joint_constraint1.tolerance_below = 2.9;  // -170 degrees in radians
    joint_constraint1.weight = 1.0;         // Weight of the constraint
    // We add joint constraints to the generic constraints
    constraints.joint_constraints.push_back(joint_constraint1);
    
    
    moveit_msgs::msg::JointConstraint joint_constraint2;
    joint_constraint2.joint_name = (*linkArray)[1]; // The second joint
    joint_constraint2.position = 0.0;    // Center of the allowed range
    joint_constraint2.tolerance_above = 0;  // +0 degrees in radians
    joint_constraint2.tolerance_below = 2; // -120 degrees in radians
    joint_constraint2.weight = 1.0;         // Weight of the constraint
    constraints.joint_constraints.push_back(joint_constraint2);
    */
    
    
        
    /*
    moveit_msgs::msg::JointConstraint joint_constraint4;
    joint_constraint4.joint_name = "A4"; // The fourth joint
    joint_constraint4.position = 0.0;       // Center of the allowed range
    joint_constraint4.tolerance_above = 0.87;  // +50 degrees in radians
    joint_constraint4.tolerance_below = 0.87;  // -50 degrees in radians
    joint_constraint4.weight = 1.0;         // Weight of the constraint
    constraints.joint_constraints.push_back(joint_constraint4);
    */

    /*
    moveit_msgs::msg::JointConstraint joint_constraint5;
    joint_constraint5.joint_name = (*linkArray)[4]; // The fifth joint
    joint_constraint5.position = 0.0;       // Center of the allowed range
    joint_constraint5.tolerance_above = 1.57;  // +90 degrees in radians
    joint_constraint5.tolerance_below = 1.57;  // -90 degrees in radians
    joint_constraint5.weight = 1.0;         // Weight of the constraint
    constraints.joint_constraints.push_back(joint_constraint5);
    */
    
    /*
    moveit_msgs::msg::JointConstraint joint_constraint6;
    joint_constraint6.joint_name = "A6"; // The sixth joint
    joint_constraint6.position = 0.0;       // Center of the allowed range
    joint_constraint6.tolerance_above = 1.57;  // +90 degrees in radians
    joint_constraint6.tolerance_below = 1.57;  // -90 degrees in radians
    joint_constraint6.weight = 1.0;         // Weight of the constraint
    constraints.joint_constraints.push_back(joint_constraint6);
    */

    geometry_msgs::msg::Pose target_pose;
    target_pose.orientation.x = request->orientation.x; //0.707; //request->orientation.x;
    target_pose.orientation.y = request->orientation.y; //0.707; //request->orientation.y;
    target_pose.orientation.z = request->orientation.z; //0; //request->orientation.z;
    target_pose.orientation.w = request->orientation.w; //0; //request->orientation.w;
    target_pose.position.x = request->position.x; // Example usage of request data
    target_pose.position.y = request->position.y;
    target_pose.position.z = request->position.z;

    // Planning parameters
    move_group_interface->setNumPlanningAttempts(3);
    move_group_interface->setPathConstraints(constraints);
    move_group_interface->setStartStateToCurrentState(); // Ensure that the planner has the current state of the robot

    // Speed limit
    if(load_use_sim()) {
      move_group_interface->setMaxVelocityScalingFactor(0.5); // 50% of the max velocity
      move_group_interface->setMaxAccelerationScalingFactor(0.5); // 50% of the max acceleration
    } else {
      move_group_interface->setMaxVelocityScalingFactor(0.1); // 10% of the max velocity
      move_group_interface->setMaxAccelerationScalingFactor(0.1); // 10% of the max acceleration
    }
    
    // Cartesian path planning
    std::vector<geometry_msgs::msg::Pose> waypoints;
    waypoints.push_back(target_pose);
    double eef_step = 0.005;  // Step size for end-effector
    double jump_threshold = 5; // If the jump is bigger than this, it will be considered invalid
    
    moveit_msgs::msg::RobotTrajectory trajectory;

    // Fraction is how big a precentage of the path that was successfully planned
    double fraction = move_group_interface->computeCartesianPath(
    waypoints,           // Waypoints to follow
    eef_step,            // Step size
    jump_threshold,      // Jump threshold
    trajectory           // Resulting trajectory
    );

    moveit::core::MoveItErrorCode error_code;

    if (fraction > 0.95) {
      RCLCPP_INFO(this->get_logger(), "Cartesian path computed successfully");
      plan->trajectory_ = trajectory;
      *plan_available = true;
      response->log = "The trajectory has been planned succesfully (Cartesian path)";
      response->success = true;

    } else {
      RCLCPP_ERROR(this->get_logger(), "Failed to compute Cartesian path, using OMPL planner instead");

      move_group_interface->setPlanningTime(5);
      move_group_interface->setPlannerId("RRTconnect"); // Other options in ompl_planning.yaml
      move_group_interface->setPoseTarget(target_pose);

      for (int i = 0; i < 3; ++i) {
        error_code = move_group_interface->plan(*plan);

        if (error_code == moveit::core::MoveItErrorCode::SUCCESS) {
          RCLCPP_INFO(this->get_logger(), "The trajectory has been planned succesfully");
          *plan_available = true;
          response->log = "The trajectory has been planned succesfully";
          response->success = true;
          break;
        }
      
        if (i == 2) {
          RCLCPP_ERROR(this->get_logger(), "The planner was unable to find a valid trajectory after 3 attempts.");
          response->success = false;

          if (error_code == moveit::core::MoveItErrorCode::FAILURE){
            RCLCPP_ERROR(this->get_logger(), "The planning failed due to an unspecified error.");
            response->log = "The planning failed due to an unspecified error. This can be caused by one of the following issues: The other arm is in the way, The target position is unreachable by that arm. Perhaps move the other arm away or use it to grasp instead.";
            
          } else if (error_code == moveit::core::MoveItErrorCode::PLANNING_FAILED){
            RCLCPP_ERROR(this->get_logger(), "The planner was unable to find a valid trajectory.");
            response->log = "The planner was unable to find a valid trajectory.";
          
          } else if (error_code == moveit::core::MoveItErrorCode::MOTION_PLAN_INVALIDATED_BY_ENVIRONMENT_CHANGE){
            RCLCPP_ERROR(this->get_logger(), "The motion plan was invalidated by an environment change");
            response->log = "The motion plan was invalidated by an environment change";
  
          } else if (error_code == moveit::core::MoveItErrorCode::INVALID_MOTION_PLAN){
            RCLCPP_ERROR(this->get_logger(), "INVALID_MOTION_PLAN, the motion plan collided with the environment");
            response->log = "The planner was unable to find a valid trajectory after 3 attempts, since it collided with the environment.";

          } else if (error_code == moveit::core::MoveItErrorCode::TIMED_OUT){
            RCLCPP_ERROR(this->get_logger(), "The motion planner timed out.");
            response->log = "The motion planner timed out, it is not possible to move to the desired position., it is likely that the other arm is in the way";
            
          } else {
            RCLCPP_ERROR(this->get_logger(), "UNKNOWN PLANNER ERROR IN ROBOT CONTROLLER SERVICE");
            response->log = "UNKNOWN PLANNER ERROR";
          }

        } else {
          RCLCPP_INFO(this->get_logger(), "Retrying planning...");
        }
        
      } 
      
    }

  }

  // Callback to execute the planned trajectory
  void handle_execute_service(const std::shared_ptr<project_interfaces::srv::ExecuteMoveCommand::Request> request,
                      const std::shared_ptr<project_interfaces::srv::ExecuteMoveCommand::Response> response) {
    
    RCLCPP_INFO(this->get_logger(), "Received request to execute planned trajectory for %s arm", request->arm.c_str());

    std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface;
    moveit::planning_interface::MoveGroupInterface::Plan *plan;
    bool *plan_available;

    // Check if the request is for the right or left arm
    if (request->arm == "right") {
      RCLCPP_INFO(this->get_logger(), "Planning for right arm");
      move_group_interface = move_group_interface_right;
      plan = &plan_right;
      plan_available = &plan_available_right;
    } else if (request->arm == "left") {
      RCLCPP_INFO(this->get_logger(), "Planning for left arm");
      move_group_interface = move_group_interface_left;
      plan = &plan_left;
      plan_available = &plan_available_left;
    } else {
      RCLCPP_ERROR(this->get_logger(), "Invalid arm specified");
      response->log = "Invalid arm specified. Use 'left' or 'right'.";
      response->success = false;
      return;
    }

    if (*plan_available)
    {
      RCLCPP_INFO(this->get_logger(), "The planned trajectory is being executed");

      move_group_interface->execute(*plan);

      RCLCPP_INFO(this->get_logger(), "The plan has been executed");
      *plan_available = false;
      response->success = true;
    } else {
      RCLCPP_ERROR(this->get_logger(), "No plan available for %s arm", request->arm.c_str());
      response->log = "No plan available for " + request->arm + " arm";
      response->success = false;
    }

  }

  //TODO: Make moveit actually listen to the joint_states topic to make the function below work
  //Alternatively as suggested by a student assistent, listen to the tf topic and calculate the joint states from the tf topic
  /*
  void handle_pose_request_service(const std::shared_ptr<project_interfaces::srv::GetCurrentPose::Request> request,
                      const std::shared_ptr<project_interfaces::srv::GetCurrentPose::Response> response) {
    RCLCPP_INFO(this->get_logger(), "Received request to get current pose for %s arm", request->arm.c_str());

    // Check if the request is for the right or left arm
    if (request->arm == "right") {
      move_group_interface_right->setStartStateToCurrentState();
      geometry_msgs::msg::PoseStamped current_pose = move_group_interface_right->getCurrentPose(ee_link_right); // The end effector link for the right arm

      std::vector<double> joint_values = move_group_interface_right->getCurrentJointValues();	

      for (size_t i = 0; i < joint_values.size(); ++i) {
        RCLCPP_INFO(this->get_logger(), "Joint %zu: %f", i, joint_values[i]);
      }

      response->pose = current_pose.pose;
      response->success = true;
      RCLCPP_INFO(this->get_logger(), "Current pose retrieved successfully");

    } else if (request->arm == "left") {
      geometry_msgs::msg::PoseStamped current_pose = move_group_interface_left->getCurrentPose(ee_link_left); // The end effector link for the left arm

      std::vector<double> joint_values = move_group_interface_left->getCurrentJointValues();	

      for (size_t i = 0; i < joint_values.size(); ++i) {
        RCLCPP_INFO(this->get_logger(), "Joint %zu: %f", i, joint_values[i]);
      }

      response->pose = current_pose.pose;
      response->success = true;
      RCLCPP_INFO(this->get_logger(), "Current pose retrieved successfully");
    } else {
      RCLCPP_ERROR(this->get_logger(), "Invalid arm specified");
      response->log = "Invalid arm specified";
      response->success = false;
      return;
    }
    }
    */

    
    //void load_use_sim() {

    //  std::string file_path = 'config.json';
     
    //}
    
    

    void handle_gripper_service(const std::shared_ptr<project_interfaces::srv::GripperMoveit::Request> request,
      const std::shared_ptr<project_interfaces::srv::GripperMoveit::Response> response) {
      // This service is to ensure that the grippers in rviz / moveit mirrors the state of the real grippers.
      RCLCPP_INFO(this->get_logger(), "Received gripper command for: %s, Width: %f", request->gripper_name.c_str(), request->width);

      //moveit::planning_interface::MoveGroupInterface::Plan *gripper_plan;
     
      if (request->gripper_name == "3f") {   
        // The width is between 0 to 167 mm.
        // The first 3 joints span form 0 to 65 degrees 
        // The second 3 joints span form 0 to 17 degrees.
        // The last 3 joints span form 0 to -55 degrees
        
        double angle_1 = 65 * ((167-request->width) / 167) / 180.0 * 3.14;
        double angle_2 = 17 * ((167-request->width) / 167) / 180.0 * 3.14;
        double angle_3 = -55 * ((167-request->width) / 167) / 180.0 * 3.14;
        
        std::map<std::string, double> target_position;
        //Finger 1
        target_position["a_3f_finger_1_joint_1"] = angle_1;
        target_position["a_3f_finger_1_joint_2"] = angle_2;
        target_position["a_3f_finger_1_joint_3"] = angle_3;
        //Finger 2
        target_position["a_3f_finger_2_joint_1"] = angle_1;
        target_position["a_3f_finger_2_joint_2"] = angle_2;
        target_position["a_3f_finger_2_joint_3"] = angle_3;
        //Finger 3
        target_position["a_3f_finger_middle_joint_1"] = angle_1;
        target_position["a_3f_finger_middle_joint_2"] = angle_2;
        target_position["a_3f_finger_middle_joint_3"] = angle_3;

        // To make a pinch
        target_position["a_3f_palm_finger_1_joint"] = -0.139;
        target_position["a_3f_palm_finger_2_joint"] = 0.139;

        // Loop through the joint names and set the target position
        std::vector<std::string> gripper_joint_names = move_group_3f->getJoints();
        for (size_t i = 0; i < gripper_joint_names.size(); ++i) {
          if ( target_position.count(gripper_joint_names[i]) > 0 ){
            move_group_3f->setJointValueTarget(gripper_joint_names[i], target_position[gripper_joint_names[i]]);
          }
        }
        move_group_3f->setStartStateToCurrentState();
        move_group_3f->setMaxVelocityScalingFactor(0.5); // 50% of the max velocity

        /*
        bool success_plan = false;
        // Save the plan for future use 
        if (request->width < 80) {
          gripper_plan = &plan_3f_closed;
        } else {
          gripper_plan = &plan_3f_open;
        }
        if(gripper_plan == nullptr) {
          success_plan = (move_group_3f->plan(*gripper_plan) == moveit::core::MoveItErrorCode::SUCCESS);
        }
        
        if(!success_plan && gripper_plan == nullptr){
          response->success = false;
          response->log = "The gripper failed to plan.";
          return;
        }
        
        move_group_2f->execute(*gripper_plan);
        */
          
        if (move_group_3f->move() == moveit::core::MoveItErrorCode::SUCCESS){
          RCLCPP_INFO(this->get_logger(), "3F gripper move succeeded");
        } else {
          RCLCPP_ERROR(this->get_logger(), "3F gripper move failed");
          response->success = false;
          response->log = "3f gripper move failed";
          return; 
        }
      

      } else if (request->gripper_name == "2f") {
      
        // The main joint in the 2f gripper span form 0 to 45 degrees, and the width is between 0 to 85 mm. We scale the angle with the width
        if (request->width < 5) {
          request->width = 5;
        }
        
        double angle = 45 * ((85-request->width) / 85) / 180.0 * 3.14;
        
        RCLCPP_INFO(this->get_logger(), "Gripper angle %f", angle);
        
        const std::string joint_name = "left_2f_robotiq_85_left_knuckle_joint";
        move_group_2f->setJointValueTarget(joint_name, angle);
        move_group_2f->setStartStateToCurrentState();
        move_group_2f->setMaxVelocityScalingFactor(0.5); // 50% of the max velocity

        /*
        bool success_plan = false;
        // Save the plan for future use 
        if (request->width < 40) {
          gripper_plan = &plan_2f_closed;
        } else {
          gripper_plan = &plan_2f_open;
        }
        if(gripper_plan == nullptr) {
          success_plan = (move_group_2f->plan(*gripper_plan) == moveit::core::MoveItErrorCode::SUCCESS);
        }
        if(!success_plan && gripper_plan == nullptr){
          response->success = false;
          response->log = "The gripper failed to plan.";
          return;
        }
        move_group_2f->execute(*gripper_plan);
        */
       
        if (move_group_2f->move() == moveit::core::MoveItErrorCode::SUCCESS){
          RCLCPP_INFO(this->get_logger(), "2F gripper move succeeded");
        } else {
          RCLCPP_ERROR(this->get_logger(), "2F gripper move failed");
          response->success = false;
          response->log = "2f gripper move failed";
          return;
        }

      } else {
        RCLCPP_ERROR(this->get_logger(), "Invalid gripper specified in robot_controller_service");
        response->success = false;
      }
    }
    
    void handle_pose_request_service(const std::shared_ptr<project_interfaces::srv::GetCurrentPose::Request> request,
                      const std::shared_ptr<project_interfaces::srv::GetCurrentPose::Response> response) {
      Matrix4d pose;

      if (request->arm == "left") {
          pose = forward_kinematics_left(joint_values_left);
          RCLCPP_INFO(this->get_logger(), "Calculated pose for left arm");
      } else if (request->arm == "right") {
          pose = forward_kinematics_right(joint_values_right);
          RCLCPP_INFO(this->get_logger(), "Calculated pose for right arm");
      } else {
          RCLCPP_ERROR(this->get_logger(), "Invalid arm specified. Use 'left' or 'right'.");
          response->success = false;
          response->log = "Invalid arm specified. Use 'left' or 'right'.";
          return;
      }

      RCLCPP_INFO(this->get_logger(), "Parsing the pose to the response message");
      response->pose.position.x = pose(0, 3);
      response->pose.position.y = pose(1, 3);
      response->pose.position.z = pose(2, 3);

      RCLCPP_INFO(this->get_logger(), "Position: x=%f, y=%f, z=%f", response->pose.position.x, response->pose.position.y, response->pose.position.z);

      Quaterniond q(pose.block<3,3>(0,0));
      response->pose.orientation.x = q.x();
      response->pose.orientation.y = q.y();
      response->pose.orientation.z = q.z();
      response->pose.orientation.w = q.w();

      RCLCPP_INFO(this->get_logger(), "Orientation: x=%f, y=%f, z=%f, w=%f", response->pose.orientation.x, response->pose.orientation.y, response->pose.orientation.z, response->pose.orientation.w);

      response->success = true;

      return;
    }     

    Matrix4d transformation_matrix(Vector3d rpy, Vector3d xyz) {
    double roll = rpy(0), pitch = rpy(1), yaw = rpy(2);
    //double x = xyz(0), y = xyz(1), z = xyz(2);

    Matrix3d Rx, Ry, Rz;

    Rx << 1, 0, 0,
          0, cos(roll), -sin(roll),
          0, sin(roll), cos(roll);

    Ry << cos(pitch), 0, sin(pitch),
          0, 1, 0,
          -sin(pitch), 0, cos(pitch);

    Rz << cos(yaw), -sin(yaw), 0,
          sin(yaw), cos(yaw), 0,
          0, 0, 1;

    Matrix3d R = Rz * Ry * Rx;

    Matrix4d T = Matrix4d::Identity();
    T.block<3,3>(0,0) = R;
    T.block<3,1>(0,3) = xyz;

    return T;
  }

  Matrix4d forward_kinematics_left(const std::vector<double>& joint_angles) {
    Matrix4d T_mount_left = transformation_matrix(Vector3d(-0.785398163, 0, -1.57079633), Vector3d(0.711114, 0.756691, 1.037203));
    Matrix4d T_left_A1 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0, 0.1475));
    Matrix4d T_left_A2 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, -0.0105, 0.1925));
    Matrix4d T_left_A3 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0105, 0.2075));
    Matrix4d T_left_A4 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0105, 0.1925));
    Matrix4d T_left_A5 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, -0.0105, 0.2075));
    Matrix4d T_left_A6 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, -0.0707, 0.1925));
    Matrix4d T_left_A7 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0707, 0.091));
    Matrix4d T_left_joint_ee = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0, 0, 0.035));

    Matrix4d R_left_A1 = transformation_matrix(Vector3d(0, 0, joint_angles[0]), Vector3d(0, 0, 0));
    Matrix4d R_left_A2 = transformation_matrix(Vector3d(0, joint_angles[1], 0), Vector3d(0, 0, 0));
    Matrix4d R_left_A3 = transformation_matrix(Vector3d(0, 0, joint_angles[2]), Vector3d(0, 0, 0));
    Matrix4d R_left_A4 = transformation_matrix(Vector3d(0, -joint_angles[3], 0), Vector3d(0, 0, 0));
    Matrix4d R_left_A5 = transformation_matrix(Vector3d(0, 0, joint_angles[4]), Vector3d(0, 0, 0));
    Matrix4d R_left_A6 = transformation_matrix(Vector3d(0, joint_angles[5], 0), Vector3d(0, 0, 0));
    Matrix4d R_left_A7 = transformation_matrix(Vector3d(0, 0, joint_angles[6]), Vector3d(0, 0, 0));

    Matrix4d T = T_mount_left * T_left_A1 * R_left_A1 * T_left_A2 * R_left_A2 * T_left_A3 * R_left_A3 * T_left_A4 * R_left_A4 * T_left_A5 * R_left_A5 * T_left_A6 * R_left_A6 * T_left_A7 * R_left_A7 * T_left_joint_ee;

    return T;
  }

  Matrix4d forward_kinematics_right(const std::vector<double>& joint_angles) {
    Matrix4d T_mount_right = transformation_matrix(Vector3d(0.785398163, 0, -1.57079633), Vector3d(0.268524, 0.756691, 1.037203));
    Matrix4d T_right_A1 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0, 0.1475));
    Matrix4d T_right_A2 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, -0.0105, 0.1925));
    Matrix4d T_right_A3 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0105, 0.2075));
    Matrix4d T_right_A4 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0105, 0.1925));
    Matrix4d T_right_A5 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, -0.0105, 0.2075));
    Matrix4d T_right_A6 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, -0.0707, 0.1925));
    Matrix4d T_right_A7 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0707, 0.091));
    Matrix4d T_right_joint_ee = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0, 0, 0.035));

    Matrix4d R_right_A1 = transformation_matrix(Vector3d(0, 0, joint_angles[0]), Vector3d(0, 0, 0));
    Matrix4d R_right_A2 = transformation_matrix(Vector3d(0, joint_angles[1], 0), Vector3d(0, 0, 0));
    Matrix4d R_right_A3 = transformation_matrix(Vector3d(0, 0, joint_angles[2]), Vector3d(0, 0, 0));
    Matrix4d R_right_A4 = transformation_matrix(Vector3d(0, -joint_angles[3], 0), Vector3d(0, 0, 0));
    Matrix4d R_right_A5 = transformation_matrix(Vector3d(0, 0, joint_angles[4]), Vector3d(0, 0, 0));
    Matrix4d R_right_A6 = transformation_matrix(Vector3d(0, joint_angles[5], 0), Vector3d(0, 0, 0));
    Matrix4d R_right_A7 = transformation_matrix(Vector3d(0, 0, joint_angles[6]), Vector3d(0, 0, 0));

    Matrix4d T = T_mount_right * T_right_A1 * R_right_A1 * T_right_A2 * R_right_A2 * T_right_A3 * R_right_A3 * T_right_A4 * R_right_A4 * T_right_A5 * R_right_A5 * T_right_A6 * R_right_A6 * T_right_A7 * R_right_A7 * T_right_joint_ee;

    return T;
  }

  bool load_use_sim(){
    // Reads config.json to determine if the simulation is used
    bool use_sim;
  
    std::ifstream file("src/robutler/config.json"); 
    nlohmann::json json_data;
    file >> json_data;  // Parse the JSON file into a JSON object
  
    // Access JSON data
    if (json_data.contains("use_sim")) {
      bool use_sim = json_data["use_sim"];
      RCLCPP_INFO(rclcpp::get_logger("load_use_sim"), "use_sim: %s", use_sim ? "true" : "false");
    } else {
      RCLCPP_WARN(rclcpp::get_logger("load_use_sim"), "Key 'use_sim' not found in config.json");
      return false;
    }
    
    return use_sim; 
  }

}; // class RobotControllerService
 

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<RobotControllerService>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
