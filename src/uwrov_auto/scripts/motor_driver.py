import pigpio
import rospy
import threading
import time
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import MultiArrayDimension
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import String

listen_topic = '/nautilus/motors/pwm'
arm_topic = '/nautilus/motors/arm'

dims = [MultiArrayDimension('data', 6, 16)]
layout = MultiArrayLayout(dim=dims, data_offset=0)
lock = threading.Lock()

pi = pigpio.pi("main", 8888)
# thruster order: ['forward_left', 'forward_right', 'forward_top', 'sideways_top', 'up_left', 'up_right']
thruster_pins = {
        'forward_left': 19,         # Port Bow
        'forward_right': 20,        # Starboard Bow
        'forward_top': 21,          # Stern
        'sideways_top': 12,         # Bow
        'up_left': 26,              # Port
        'up_right': 16              # Starboard
        }

pins = list(thruster_pins.values())

def pwm_apply_callback(msg):
    if not lock.locked():
        for pin, pwm in zip(pins, msg.data):
            pi.set_servo_pulsewidth(pin, pwm)

def arm_motors(msg):
    if not lock.locked():
        t = threading.Thread(target=arm_thread)
        t.start()

def arm_thread():
    lock.acquire()
    for key, val in thruster_pins:
        pi.set_servo_pulsewidth(key, 0)
        time.sleep(0.25)
        pi.set_servo_pulsewidth(key, 1500)
        time.sleep(0.25)
    lock.release()
    # kill thread?


def main():
    print("Starting Motor Drivers")
    print('subscribing to:', listen_topic)

    rospy.init_node('motor_driver')
    rospy.Subscriber(listen_topic, Int16MultiArray, pwm_apply_callback)
    rospy.Subscriber(arm_topic, String, arm_motors)
    rospy.on_shutdown(shutdown_fn)
    rospy.spin()


def shutdown_fn():
    pi.stop()
    print('shutting down motor driver')


if __name__ == '__main__':
    main()
