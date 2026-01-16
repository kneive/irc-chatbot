from .baseTag import BaseTag
from dataclasses import dataclass

@dataclass
class SubmysterygiftTag(BaseTag):

    gift_id:str = 'null'
    origin_id:str = 'null'
    sub_plan:str = 'null'
    mass_gift_count:str = '-1'
    sender_count:str = '-1'