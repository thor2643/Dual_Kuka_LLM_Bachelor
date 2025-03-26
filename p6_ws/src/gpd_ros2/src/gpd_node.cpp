
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>

#include <gpd/grasp_detector.h>
#include <gpd/util/cloud.h>
#include <gpd/util/config_file.h>
#include <gpd/util/plot.h>
#include <gpd/candidate/hand.h>

#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_types.h>
#include <pcl/filters/voxel_grid.h>

#include <Eigen/Dense>
#include <memory>

#include <visualization_msgs/msg/marker_array.hpp>
#include <visualization_msgs/msg/marker.hpp>



class GpdGraspNode : public rclcpp::Node
{
public:
  GpdGraspNode()
  : Node("gpd_node")
  {
    this->declare_parameter<std::string>("config_path", "");
    this->declare_parameter<std::string>("weights_file", "");
    this->declare_parameter<std::string>("image_geometry_filename", "");

    this->get_parameter("config_path", config_path_);
    this->get_parameter("weights_file", weights_file_);
    this->get_parameter("image_geometry_filename", image_geometry_file_);

    if (config_path_.empty()) {
      RCLCPP_ERROR(this->get_logger(), "No config_path parameter set!");
      rclcpp::shutdown();
      return;
    }

    RCLCPP_INFO(this->get_logger(), "Using config: %s", config_path_.c_str());

    grasp_detector_ = std::make_unique<gpd::GraspDetector>(config_path_);

    view_points_.resize(3, 1);
    view_points_ << 0.0, 0.0, 1.0;

    cloud_sub_ = this->create_subscription<sensor_msgs::msg::PointCloud2>(
      "/camera/camera/depth/color/points", 10,
      std::bind(&GpdGraspNode::cloudCallback, this, std::placeholders::_1));

    pose_pub_ = this->create_publisher<geometry_msgs::msg::PoseStamped>("grasp_pose", 10);
    marker_pub_ = this->create_publisher<visualization_msgs::msg::MarkerArray>("grasp_markers", 10);

    RCLCPP_INFO(this->get_logger(), "GPD grasp node started.");
  }

private:
  void cloudCallback(const sensor_msgs::msg::PointCloud2::SharedPtr msg)
  {
    RCLCPP_INFO(this->get_logger(), "Received cloud callback");
    RCLCPP_INFO(this->get_logger(), "Received point cloud with size: %d x %d", msg->height, msg->width);

        if (msg->height == 0 || msg->width == 0) {
        RCLCPP_ERROR(this->get_logger(), "Received an empty point cloud.");
        return;
    }

    // Check the fields in the PointCloud2 message
    bool has_x = false, has_y = false, has_z = false, has_rgb = false;
    for (auto &field : msg->fields) {
        if (field.name == "x") has_x = true;
        if (field.name == "y") has_y = true;
        if (field.name == "z") has_z = true;
        if (field.name == "rgb") has_rgb = true;
    }

    if (!has_x || !has_y || !has_z || !has_rgb) {
        RCLCPP_ERROR(this->get_logger(), "PointCloud2 message missing required fields.");
        return;
    }

    RCLCPP_INFO(this->get_logger(), "PointCloud2 message is valid.");


    pcl::PointCloud<pcl::PointXYZRGB>::Ptr pcl_cloud_rgb(new pcl::PointCloud<pcl::PointXYZRGB>);
    pcl::fromROSMsg(*msg, *pcl_cloud_rgb);

    if (pcl_cloud_rgb->empty()) {
      RCLCPP_WARN(this->get_logger(), "Received empty RGB cloud.");
      return;
    }

    for (auto &point : pcl_cloud_rgb->points) {
        if (std::isnan(point.x) || std::isnan(point.y) || std::isnan(point.z)) {
            RCLCPP_WARN(this->get_logger(), "NaN values found in point cloud data.");
            return;
        }
    }

    pcl::PointCloud<pcl::PointXYZRGBA>::Ptr pcl_cloud_rgba(new pcl::PointCloud<pcl::PointXYZRGBA>);
    pcl::copyPointCloud(*pcl_cloud_rgb, *pcl_cloud_rgba);

    if (pcl_cloud_rgba->empty()) {
      RCLCPP_WARN(this->get_logger(), "Conversion to RGBA failed (empty cloud).");
      return;
    }

    pcl::VoxelGrid<pcl::PointXYZRGBA> voxel;
    voxel.setInputCloud(pcl_cloud_rgba);
    voxel.setLeafSize(0.01f, 0.01f, 0.01f);
    pcl::PointCloud<pcl::PointXYZRGBA>::Ptr filtered(new pcl::PointCloud<pcl::PointXYZRGBA>);
    voxel.filter(*filtered);

    RCLCPP_INFO(this->get_logger(), "Before voxel: %lu", pcl_cloud_rgba->size());
    //RCLCPP_INFO(this->get_logger(), "After voxel: %lu", filtered->size());

    if (pcl_cloud_rgba->empty()) { // was filtered instead of pcl_cloud_rgba
      RCLCPP_WARN(this->get_logger(), "Voxel filter produced an empty cloud. Try adjusting voxel size.");
      return;
    }

    gpd::util::Cloud input_cloud(pcl_cloud_rgba, 0, view_points_); // was filtered instead of pcl_cloud_rgba
    input_cloud.calculateNormals(10, 0.06); // 2 is the number of neighbors, 0.06 is the radius

    RCLCPP_INFO(this->get_logger(), "Starting grasp detection with %zu points", filtered->size());
    RCLCPP_INFO(this->get_logger(), "About to call detectGrasps...");
    auto grasps = grasp_detector_->detectGrasps(input_cloud);
    RCLCPP_INFO(this->get_logger(), "detectGrasps completed.");
    RCLCPP_INFO(this->get_logger(), "Detected %lu grasps.", grasps.size());

    if (!grasps.empty()) {
      const auto& top_grasp = grasps[0];

      geometry_msgs::msg::PoseStamped pose;
      pose.header.stamp = this->now();
      pose.header.frame_id = msg->header.frame_id;

      Eigen::Matrix3d frame = top_grasp->getFrame();
      Eigen::Vector3d pos = top_grasp->getPosition();
      Eigen::Quaterniond q(frame);

      pose.pose.position.x = pos(0);
      pose.pose.position.y = pos(1);
      pose.pose.position.z = pos(2);
      pose.pose.orientation.x = q.x();
      pose.pose.orientation.y = q.y();
      pose.pose.orientation.z = q.z();
      pose.pose.orientation.w = q.w();

      pose_pub_->publish(pose);
      RCLCPP_INFO(this->get_logger(), "Published top grasp pose.");
    } 
    else {
      RCLCPP_WARN(this->get_logger(), "No grasps detected.");
    }

    RCLCPP_INFO(this->get_logger(), "Finished processing callback");

    // Clear all data from this callback to avoid errors
    grasps.clear();
    filtered.reset();
    pcl_cloud_rgba.reset();
    pcl_cloud_rgb.reset();
    RCLCPP_WARN(this->get_logger(), "reached 1.");

  }

  std::string config_path_;
  std::string weights_file_;
  std::string image_geometry_file_;

  

  Eigen::Matrix3Xd view_points_;
  std::unique_ptr<gpd::GraspDetector> grasp_detector_;

  rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr cloud_sub_;
  rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr pose_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr marker_pub_;
};



int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<GpdGraspNode>());
  rclcpp::shutdown();

  return 0;
}