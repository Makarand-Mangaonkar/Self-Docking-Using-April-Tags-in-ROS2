#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from apriltag_msgs.msg import AprilTagDetectionArray
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import time
import math

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/camera/rgb/image_rect_color',
            self.listener_callback,
            10)
        self.detection_subscription = self.create_subscription(
            AprilTagDetectionArray,
            '/detections',
            self.detection_callback,
            10)
        self.camera_info_subscription = self.create_subscription(
            CameraInfo,
            '/camera/rgb/camera_info',
            self.camera_info_callback,
            10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.bridge = CvBridge()
        self.target_detected = False
        self.target_centre = None
        self.target_id = None
        self.image_width = 0
        self.image_height = 0

    def listener_callback(self, data):
        current_frame = self.bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
        if self.target_detected and self.target_centre:
            cv2.circle(current_frame, (int(self.target_centre.x), int(self.target_centre.y)), 10, (0, 0, 255), -1)
        cv2.imshow("Camera Feed", current_frame)
        cv2.waitKey(1)

    def camera_info_callback(self, msg):
        self.image_width = msg.width
        self.image_height = msg.height

    def detection_callback(self, msg):
        if len(msg.detections) > 0:
            detection = msg.detections[0]
            self.target_centre = detection.centre
            self.target_id = detection.id
            self.target_detected = True
            
            # Calculate the tag's area in the image
            tag_width = abs(detection.corners[0].x - detection.corners[2].x)
            tag_height = abs(detection.corners[0].y - detection.corners[2].y)
            tag_area = tag_width * tag_height
            image_area = self.image_width * self.image_height

            if tag_area > 0.2 * image_area:
                # If tag occupies more than 10% of the image, stop
                self.rotate_90_degrees()
                self.move_backwards()




            else:
                # Move towards the detected tag
                self.move_towards_tag()
            
                
        # else:
        #     self.stop()

    def move_towards_tag(self):
        twist = Twist()
        centre_x = self.target_centre.x

        # Proportional control parameters
        linear_speed = 0.1

        # Calculate error from the centre of the image
        error_x = centre_x - (self.image_width / 2)

        # Move towards the tag
        twist.linear.x = linear_speed
        twist.angular.z = -error_x * 0.002  # Adjust gain as necessary
        self.publisher.publish(twist)

    def move_backwards(self):
        twist = Twist()
        twist.linear.x = -0.2  # Move backwards at 0.1 m/s
        self.publisher.publish(twist)  # Send the command before sleeping

        time.sleep(4.0)  # Wait for second

        twist.linear.x = 0.0  # Stop the robot
        self.publisher.publish(twist)  

    def stop(self):
        twist = Twist()
        twist.angular.z = 0.0  # for stopping
        twist.linear.x = 0.0
        self.publisher.publish(twist)

    def rotate_90_degrees(self):
        twist = Twist()
        twist.angular.z = 0.4  # Rotate at 1 rad/s
        self.publisher.publish(twist)

        time.sleep((math.pi/2)*5.4)  # 180-degree rotation takes π (3.14) seconds

        twist.angular.z = 0.0  # Stop rotation
        self.publisher.publish(twist)

    def rotate(self):
        twist = Twist()
        twist.angular.z = 0.1  # for stopping
        self.publisher.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
