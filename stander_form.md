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
    }
}
`  
# order_slice
>json  

`{
    "type": "order_slice",
    "id": uuid,
    "data": str
}
`  
