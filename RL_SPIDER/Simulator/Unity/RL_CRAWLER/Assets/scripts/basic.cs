using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class basic : MonoBehaviour {

    void Start() 
    {
        HingeJoint2D hinge = GetComponent<HingeJoint2D>();
        HingeJoint2D.motor motor=hinge.motor;

        motor.force = 10;
        motor.targetVelocity = 90;
        motor.freeSpin = false;
        hinge.motor = motor;
        hinge.useMotor = true;

        }
    void Update(){

    }

}
