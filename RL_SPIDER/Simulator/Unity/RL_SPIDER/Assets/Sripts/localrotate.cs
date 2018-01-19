using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class localrotate : MonoBehaviour {

	// Use this for initialization
	void start () {
		 //transform.RotateAround(Vector3.zero, Vector3.up,0);
	}
	// Update is called once per frame
	void Update () {
		 //transform.RotateAround(Vector3.zero, Vector3.up,);
		transform.Rotate(Time.deltaTime, 0, 0);
		float minRotation = -45;
         float maxRotation = 45;
         Vector3 currentRotation = transform.localRotation.eulerAngles;
         currentRotation.x = Mathf.Clamp(currentRotation.x, minRotation, maxRotation);
         transform.localRotation = Quaternion.Euler (currentRotation);
	}
}
