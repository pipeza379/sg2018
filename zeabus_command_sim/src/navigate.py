#!/usr/bin/python2
import rospy
from std_msgs.msg import String, Float64 ,Bool
# from zeabus_vision_example.msg import vision_gate
from aicontrol import AIControl
import constants as cons

class Gate(object):
    def __init__(self):
        rospy.init_node('mission_gate', anonymous=True)

        print 'now do gate'
        
        ## vision service 

        # print 'gate_srv start'    
        # self.detect = self.detect_gate.data_gate
        self.aicontrol = AIControl()

    # def run(self):
    #     auv = self.aicontrol
    #     print "start drive_z"
    #     auv.depthAbs(cons.AUV_DEPTH)
    #     print "drive z complete"
    #     rospy.loginfo('x: %f\ny: %f\nz: %f'%(auv.auv_state[0], auv.auv_state[1], auv.auv_state[2]))
        
    #     print "start find gate"
    #     while not self.check_gate:
    #         self.check_gate = self.detect_gate.data_gate.check
    #         self.aicontrol.move('forward',cons.AUV_SPEED)
    #     print "found gate"
    #     self.aicontrol.stop()
    #     ## found gate    
                
    #     print "start turning"     
    #     count = cons.GATE_COUNT
    #     self.green_old = self.red_old = 0
                
    #     while not rospy.is_shutdown() and not self.aicontrol.isFail(count):
    #         count -= 1    
    #         if self.area_red > self.area_green or self.area_red == None:
    #             auv.turnRelative(1)
    #             if self.area_red == None and green_old > self.area_green*cons.GATE_POLE:
    #                 break
    #             elif self.area_red <= self.area_green*cons.GATE_POLE:
    #                 break               
    #             self.green_old = self.area_green                
    #         elif self.area_red < self.area_green or self.area_green == None:
    #             auv.turnRelative(-1)
    #             red_old = 0
    #             if self.area_green == None and red_old > self.area_red*cons.GATE_POLE:
    #                 break          
    #             elif self.area_red*cons.GATE_POLE >= self.area_green:
    #                 break
    #             red_old = self.area_red               
    #         ## rotate to gate
    #     auv.stop()
    #     print "turning complete"

    #     print "find center"
    #     count = cons.GATE_COUNT        
    #     while not rospy.is_shutdown() and not self.aicontrol.isFail(count) :
    #         self.pos_center = self.detect_gate.data_gate.pos_black
    #         if self.pos_center >= cons.SCREEN_WIDTH/2*0.9 and self.pos_center <= cons.SCREEN_WIDTH/2*1.1:
    #             print("good aim")
    #             break
    #         elif self.pos_center < cons.SCREEN_WIDTH/2*0.9:
    #             auv.move('right',cons.AUV_SPEED)
    #         elif self.pos_center > cons.SCREEN_WIDTH/2*1.1:
    #             auv.move('left',cons.AUV_SPEED)
    #         count -= 1
    #         ## move to center
    #     print "find center complete"

    #     auv.move('forward',cons.AUV_SPEED)
    #     ## elapse gate
    #     auv.stop()

    def run2(self,data):
        auv = self.aicontrol
        print "start drive_z"
        auv.depthAbs(cons.GATE_DEPTH)
        print "drive z complete"
        rospy.loginfo('x: %f\ny: %f\nz: %f'%(auv.auv_state[0], auv.auv_state[1], auv.auv_state[2]))

        count = cons.GATE_FRONT
        while not rospy.is_shutdown() and not auv.isFail(count):
            count -=1
            auv.moveToPos(3.5, 0, 0)
        auv.stop()
        print "stop at front gate"

        print "start find gate"  
        while not rospy.is_shutdown() and not self.data.check_top:
            if not self.data.check_l and not self.data.check_top:
                auv.move(cons.GATE_POS,cons.GATE_SPEED)
            elif not self.data.check_r and not self.data.check_top:
                auv.move(cons.GATE_POS,cons.GATE_SPEED)
        auv.stop()
        print "found gate"

        print 'move to center'
        count = cons.GATE_COUNT 
        while not rospy.is_shutdown() and not auv.isFail(count) :
            self.pos_center = self.data.top_x
            if self.pos_center >= cons.SCREEN_WIDTH/2*0.9 and self.pos_center <= cons.SCREEN_WIDTH/2*1.1:
                print("good aim")
                break
            elif self.pos_center < cons.SCREEN_WIDTH/2*0.9:
                auv.move('right',cons.GATE_SPEED)
            elif self.pos_center > cons.SCREEN_WIDTH/2*1.1:
                auv.move('left',cons.GATE_SPEED)
            count -= 1
            ## move to center
        auv.stop()
        print 'at center'

        print "move forward"
        count = cons.GATE_ELAPSE
        while not rospy.is_shutdown and not auv.isFail(count):
            auv.move('forward',cons.GATE_SPEED)
            if self.data.right_area == None or self.data.left_area == None or self.data.left_area == None :
                count -=1
        auv.stop()
        print "elapse gate"

if __name__ == '__main__':
    mission_gate = Gate()
    #mission_gate.run()
    rospy.Subscriber('/vision_mission_gate', vision_gate, mission_gate.run2)
    # mission_gate.run2()
    print "finish gate"
