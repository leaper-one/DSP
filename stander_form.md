# Befor all  
Every json need to be packed for UDP.  
# order  
>json  

`
{  
    "type": "order",
    "user_id": uuid,
    "order_id": uuid,
    "data": {
        "file_type": mine,
        "file_hash: str(md5),
        "file_slices_hash": list
    },
    "date":str,
    "order_hash":str
}
`  
# order_slice
>json  

`{
    "type": "order_slice",
    "user_id": uuid,
    "order_id": uuid,
    "order_hash":str,
    "data": str
}
`  
