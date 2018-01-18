using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class localrotate : MonoBehaviour {

	// Use this for initialization
	void start () {
		 transform.RotateAround(Vector3.zero, Vector3.up,0);
	}
	// Update is called once per frame
	void Update () {
		 transform.RotateAround(Vector3.zero, Vector3.up,);
	}
}
