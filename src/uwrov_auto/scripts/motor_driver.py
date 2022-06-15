from asyncio.windows_events import NULL
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
        'forward_right': {'pin': 21, 'reversed': True},     # Port Bow
        'forward_right': {'pin': 16. 'reversed': True},     # Starboard Bow
        'forward_top': {'pin': 19, 'reversed': False},      # Stern
        'sideways_top': {'pin': 12, 'reversed': True},      # Bow
        'up_left': {'pin': 26, 'reversed': False},          # Port
        'up_right': {'pin': 20, 'reversed': False}          # Starboard
        }


pins = list(thruster_pins.values())

def pwm_apply_callback(msg):
    if not lock.locked():
        for pin, pwm in zip(pins, msg.data):
            if pin['reversed']:
                pwm = reverse_pwm(pwm)
            pi.set_servo_pulsewidth(pin['pin'], pwm)


def reverse_pwm(pwm):
    new_pwm = pwm - 1500
    return 1500 - new_pwm


def arm_motors():
    if not lock.locked():
        t = threading.Thread(target=arm_thread)
        t.start()

def arm_thread():
    lock.acquire()
    for key in thruster_pins:
        pi.set_servo_pulsewidth(thruster_pins[key]['pin'], 0)
        time.sleep(0.25)
        pi.set_servo_pulsewidth(thruster_pins[key]['pin'], 1500)
        time.sleep(0.25)
    lock.release()
    # kill thread?


def main():
    print("Starting Motor Drivers")
    print("subscribing to:", listen_topic)

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
