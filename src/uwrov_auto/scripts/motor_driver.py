import pigpio
import rospy
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import MultiArrayDimension
from std_msgs.msg import MultiArrayLayout

listen_topic = '/nautilus/motors/pwm'

dims = [MultiArrayDimension('data', 6, 16)]
layout = MultiArrayLayout(dim=dims, data_offset=0)

pi = pigpio.pi("main", 8888)
# thruster order: ['forward_left', 'forward_right', 'forward_top', 'sideways_top', 'up_left', 'up_right']
thruster_pins = {
        'forward_left': 21, # Port Bow
        'forward_right': 20, # Starboard Bow
        'forward_top': 16, # Stern
        'sideways_top': 12, # Bow
        'up_left': 26, # Port
        'up_right': 19 # Starboard
        }

pins = list(thruster_pins.values())

def pwm_apply_callback(msg):
    for pin, pwm in zip(pins, msg.data):
        pi.set_servo_pulsewidth(pin, pwm)


def main():
    print("Starting Motor Drivers")
    print('subscribing to:', listen_topic)

    rospy.init_node('motor_driver')
    rospy.Subscriber(listen_topic, Int16MultiArray, pwm_apply_callback)
    rospy.on_shutdown(shutdown_fn)
    rospy.spin()


def shutdown_fn():
    pi.stop()
    print('shutting down motor driver')


if __name__ == '__main__':
    main()
