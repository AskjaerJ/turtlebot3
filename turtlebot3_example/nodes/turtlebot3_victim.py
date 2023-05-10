import rospy
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import time  # time module
import smbus  # led sensor

VICTIM_COUNT = 0


class Victim():

    def __init__(self):
        self.check_for_victim()
        
    def check_for_victim():
        # LED
        # Get I2C bus
        bus = smbus.SMBus(1)

        # ISL29125 address, 0x44(68)
        # Select configuation-1register, 0x01(01)
        # 0x0D(13) Operation: RGB, Range: 360 lux, Res: 16 Bits
        bus.write_byte_data(0x44, 0x01, 0x05)
        
        t_end = time.time() + 120  # time_time returns time since 1st jan 1970
        
        while time.time() < t_end:
            # read LED data
            data = bus.read_i2c_block_data(0x44, 0x09, 6)

            # Convert the data to green, red and blue int values
            green = 256*data[1] + data[0]
            red = 256*data[3] + data[2]
            blue = 256*data[5] + data[4]

            # count red
            if red > green and red > blue:  # red
                red_count = red_count + 1
                rospy.loginfo('VICTIM!, new victim count : %f', red_count)


def main():
    rospy.init_node('turtlebot3_victim')
    try:
        victim = Victim()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()