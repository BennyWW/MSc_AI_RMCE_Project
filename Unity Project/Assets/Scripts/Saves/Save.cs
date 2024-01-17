using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class Save
{
    public string _name;
    public saveType _type;


    public enum saveType
    {
        _string,
        _int,
        _float
    }
}
