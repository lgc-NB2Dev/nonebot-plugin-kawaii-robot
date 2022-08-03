from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    leaf_reply_type: int = 1
    leaf_poke_rand:int = 5