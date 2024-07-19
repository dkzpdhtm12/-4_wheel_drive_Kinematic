import rclpy
import math

from rclpy.node import Node
from geometry_msgs.msg import Twist

class Kinematic(Node):
    def __init__(self):
        super().__init__('kinematic')
        self.kinematic = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

    def cmd_vel_callback(self, msg):
        twist_data = msg

        WHEEL_RADIUS = 0.127
        FR_WHEELS_DISTANCE = 1.279
        LR_WHEELS_DISTANCE = 0.741

        motor1, motor2, motor3, motor4 = self.cal_angular_velocity(twist_data, WHEEL_RADIUS, FR_WHEELS_DISTANCE, LR_WHEELS_DISTANCE)

        motor1_rpm = int(self.get_rpm(motor1))
        motor2_rpm = int(self.get_rpm(motor2))
        motor3_rpm = int(self.get_rpm(motor3))
        motor4_rpm = int(self.get_rpm(motor4))

        self.get_logger().info(f"Motor 1 RPM : {motor1_rpm}\tMotor 2 RPM : {motor2_rpm}\tMotor 3 RPM : {motor3_rpm}\tMotor 4 RPM : {motor4_rpm}")

    def cal_angular_velocity(self, twist_data, WHEEL_RADIUS, FR_WHEELS_DISTANCE, LR_WHEELS_DISTANCE):
        motor1 = (twist_data.linear.x - twist_data.linear.y - twist_data.angular.z * (FR_WHEELS_DISTANCE + LR_WHEELS_DISTANCE) / 2) / WHEEL_RADIUS
        motor2 = (twist_data.linear.x + twist_data.linear.y + twist_data.angular.z * (FR_WHEELS_DISTANCE + LR_WHEELS_DISTANCE) / 2) / WHEEL_RADIUS
        motor3 = (twist_data.linear.x + twist_data.linear.y - twist_data.angular.z * (FR_WHEELS_DISTANCE + LR_WHEELS_DISTANCE) / 2) / WHEEL_RADIUS
        motor4 = (twist_data.linear.x - twist_data.linear.y + twist_data.angular.z * (FR_WHEELS_DISTANCE + LR_WHEELS_DISTANCE) / 2) / WHEEL_RADIUS

        return motor1, motor2, motor3, motor4

    def get_rpm(self, motor_angular_velocity):
        return motor_angular_velocity * 60 / (2 * math.pi) * 10

def main(args=None):
    rclpy.init(args=args)

    kinematic = Kinematic()

    rclpy.spin(kinematic)

    kinematic.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()