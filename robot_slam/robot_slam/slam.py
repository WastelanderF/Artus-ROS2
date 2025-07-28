#!/usr/bin/env python3
import rclpy                                     # ROS2 Python Interface
from rclpy.node import Node                      # ROS2 Node
from sensor_msgs.msg import LaserScan
import math

class slam_node(Node):
    def __init__(self, name):
        super().__init__(name)                     # ROS2 Node Parent Class initialize
        self.subscription = self.create_subscription(
          LaserScan,
          '/scan',
          self.scan_callback,
          10)
        self.get_logger().info("Node started, listening to /scan")

    def scan_callback(self, msg: LaserScan):
        self.get_logger().info('Scan callback triggered')    
        valid_ranges = [r for r in msg.ranges if not math.isinf(r) and not math.isnan(r)]
        if valid_ranges:
            min_distance = min(valid_ranges)
            self.get_logger().info(f'min_distance type: {type(min_distance)}, value: {min_distance}')
        else:
            self.get_logger().warn('No valid range data received!')

def main(args=None):                               # ROS2 Node main
    rclpy.init(args=args)                          # ROS2 Python initialize
    node = slam_node("node_slam")                  # create ROS2 Node and initialize
    rclpy.spin(node)                               # in loop waiting ROS 2 to quit
    node.destroy_node()                            # destroy Node 
    rclpy.shutdown()                               # close ROS2 Python Interface

if __name__ == '__main__':
    main()