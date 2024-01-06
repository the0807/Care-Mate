#!/usr/bin/env python
import rospy
import actionlib
import collections
import os
import multiprocessing as mp
import subprocess
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from random import sample
from math import pow, sqrt
from std_msgs.msg import Header
import pyautogui
import time

# bringup
def bringup():
    os.system("roslaunch turtlebot3_bringup turtlebot3_robot.launch")

# map load and open rviz
def launch_nav():
    os.system("roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml")

class MultiNav():
    def __init__(self):
        rospy.init_node('MultiNav', anonymous=True)
        rospy.on_shutdown(self.shutdown)

        # How long in seconds should the robot pause at each location?
        self.rest_time = rospy.get_param("~rest_time", 10)

        # Are we running in the fake simulator?
        self.fake_test = rospy.get_param("~fake_test", False)

        # Goal state return values
        goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED','SUCCEEDED',
                       'ABORTED', 'REJECTED','PREEMPTING', 'RECALLING',
                       'RECALLED','LOST']

        #goal
        locations = collections.OrderedDict()
        locations['point-1'] = Pose(Point(2.0, 1.2, 0), Quaternion(0.000, 0.000, 0.000, 1.000))
        locations['point-2'] = Pose(Point(-0.2, 0, 0), Quaternion(0.000, 0.000, 0.000, 1.000))

        # Publisher to manually control the robot (e.g. to stop it)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)

        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")

        # Wait 60 seconds for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(60))
        rospy.loginfo("Connected to move base server")

        # A variable to hold the initial pose of the robot to be set by the user in RViz
        initial_pose = PoseWithCovarianceStamped()

        # Variables to keep track of success rate, running time, and distance traveled
        n_locations = len(locations)
        n_goals = 0
        n_successes = 0
        i = 0
        distance_traveled = 0
        start_time = rospy.Time.now()
        running_time = 0
        location = ""
        last_location = ""
        # Get the initial pose from the user
        subprocess.call(["python3", "publishInitialPos.py"])
        self.last_location = Pose()

        rospy.sleep(3)
        # 1 to continue, 0 to exit
        keyinput = int(input("Input 1 to continue or 0 to exit\n"))
        while keyinput != 1:
            exit()

        # Make sure we have the initial pose
        while initial_pose.header.stamp == "":
            rospy.sleep(1)
        rospy.loginfo("Starting navigation test")

        # Begin the main loop and run through a sequence of locations
        for location in locations.keys():
            rospy.loginfo("Updating current pose.")
            distance = sqrt(pow(locations[location].position.x
                           - initial_pose.pose.pose.position.x, 2) +
                           pow(locations[location].position.y -
                           initial_pose.pose.pose.position.y, 2))
            initial_pose.header.stamp = ""

            # Store the last location for distance calculations
            last_location = location

            # Increment the counters
            i += 1
            n_goals += 1

            # Set up the next goal location
            self.goal = MoveBaseGoal()
            self.goal.target_pose.pose = locations[location]
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()

            # Let the user know where the robot is going next
            rospy.loginfo("Going to: " + str(location))
            # Start the robot toward the next location
            self.move_base.send_goal(self.goal)

            # Allow 5 minutes to get there
            finished_within_time = self.move_base.wait_for_result(rospy.Duration(300))

            # Check for success or failure
            if not finished_within_time:
                self.move_base.cancel_goal()
                rospy.loginfo("Timed out achieving goal")
            else:
                state = self.move_base.get_state()
                if state == GoalStatus.SUCCEEDED:
                    rospy.loginfo("Goal succeeded!")
                    n_successes += 1
                    distance_traveled += distance
                else:
                    rospy.loginfo("Goal failed with error code: " + str(goal_states[state]))

            # How long have we been running?
            running_time = rospy.Time.now() - start_time
            running_time = running_time.secs / 60.0

            # Print a summary success/failure, distance traveled and time elapsed
            rospy.loginfo("Success so far: " + str(n_successes) + "/" +
                          str(n_goals) + " = " + str(100 * n_successes/n_goals) + "%")
            rospy.loginfo("Running time: " + str(trunc(running_time, 1)) +
                          " min Distance: " + str(trunc(distance_traveled, 1)) + " m")
            rospy.sleep(self.rest_time)

            if (n_goals == n_locations):
                rospy.sleep(3)
                for i in range(0, 1):
                    pyautogui.hotkey('ctrl', 'c')

    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.move_base.cancel_goal()
        rospy.sleep(2)
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)

def trunc(f, n):
    # Truncates/pads a float f to n decimal places without rounding
    slen = len('%.*f' % (n, f))
    return float(str(f)[:slen])

if __name__ == '__main__':
    try:
        # multiprocessing bringup
        bringup_process = mp.Process(target=bringup, name="p1")
        bringup_process.start()
        rospy.sleep(10)

        # multiprocessing start rviz
        rviz_process = mp.Process(target=launch_nav, name="p2")
        rviz_process.start()

        MultiNav()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("AMCL navigation test finished.")

