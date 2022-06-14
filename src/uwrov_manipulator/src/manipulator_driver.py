import pigpio
import rospy
from std_msgs.msg import Int32

LISTEN_TOPIC = "/nautilus/manipulator/pwm"

MANIPULATOR_PIN = 52

RANGE = [0, 1500]
PERCENTAGE_RANGE = [0, 100]

pi = pigpio.pi("main", 8888)

def apply_percentage(msg):
    value = msg.data
    if value > PERCENTAGE_RANGE[1]: value = PERCENTAGE_RANGE[1]
    if value < PERCENTAGE_RANGE[0]: value = PERCENTAGE_RANGE[0]
    calculated_value = ((RANGE[1] - RANGE[0]) * value / 100) + RANGE[0]
    pi.set_servo_pulsewidth(MANIPULATOR_PIN, calculated_value)


def main():
    print("Starting Manipulator Drivers")
    print('subscribing to:', LISTEN_TOPIC)

    rospy.init_node('manipulator_driver')
    rospy.Subscriber(LISTEN_TOPIC, Int32, pwm_apply_callback)
    rospy.on_shutdown(shutdown_fn)
    rospy.spin()


def shutdown_fn():
    pi.stop()
    print('shutting down manipulator driver')


if __name__ == '__main__':
    main()
