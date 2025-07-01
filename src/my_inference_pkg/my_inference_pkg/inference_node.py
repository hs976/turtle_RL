import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np
from stable_baselines3 import PPO

class InferenceNode(Node):
    def __init__(self):
        super().__init__('inference_node')

        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )

        model_path = '/home/ubuntu/ros2_ws/src/my_inference_pkg/models/ppo_lidar_model.zip'
        self.model = PPO.load(model_path)
        self.get_logger().info('✅ モデル読み込み完了')

    def scan_callback(self, msg):
        scan_data = np.array(msg.ranges)
        scan_data = np.clip(scan_data, 0.0, 3.5)
        scan_data = scan_data[::24]
        scan_data = scan_data.astype(np.float32).reshape(1, -1)

        action, _ = self.model.predict(scan_data, deterministic=True)

        raw_linear = float(action[0][0])
        raw_angular = float(action[0][1])

        # ✅ より遅い速度（0.02〜0.1 m/s）、回転も控えめ
        linear = np.clip(raw_linear * 0.05, 0.02, 0.1)
        angular = np.clip(raw_angular * 1.0, -1.0, 1.0)

        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular
        self.publisher.publish(twist)

        self.get_logger().info(f"📡 Published Twist: linear={linear:.2f}, angular={angular:.2f}")

def main():
    rclpy.init()
    node = InferenceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
