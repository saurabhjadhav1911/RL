using System.Collections;
using System.Collections.Generic;
using UnityEngine; 

public class basic : MonoBehaviour {

    void Start() 
    {


        HingeJoint2D hinge = GetComponent<HingeJoint2D>();
        JointMotor2D motor=hinge.motor;

        motor.motorSpeed = 10;
        motor.
        hinge.motor=motor;
        hinge.useMotor = true;

        }
    void Update(){

    }

}
