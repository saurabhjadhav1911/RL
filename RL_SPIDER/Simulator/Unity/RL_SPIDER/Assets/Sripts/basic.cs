using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class basic : MonoBehaviour {

	// Use this for initialization
	void Start () {
		Debug.Log("start");
	}
	
	// Update is called once per frame
	void OnCollisionEnter(Collision col) {
		Debug.Log("trigger enter");
	}
}
