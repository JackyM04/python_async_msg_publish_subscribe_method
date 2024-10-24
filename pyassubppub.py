import asyncio
class KabiInterface_dm:
    def __init__(self):
        self.is_comming_gift = asyncio.Condition()
        self.gift_id = None
        self.is_on_gift_msg = asyncio.Condition()
        self.gift_msg = None
        self.is_kabi_recive = asyncio.Condition()
        self.condition_dict = {}
        self.gift_msg_dict = {}
    
    def new_trsiter(self, name):
        self.condition_dict[name] = asyncio.Condition()
        self.gift_msg_dict[name] = None
    
    #for async with
    def get_transiter(self, name):
        return self.condition_dict[name]
    
    #for set get msg befor get should with async with
    async def set_get_msg(self, name, value=None):
        ov = self.gift_msg_dict[name]
        if value is not None:
            self.gift_msg_dict[name] = value
            async with self.condition_dict[name]:
                self.condition_dict[name].notify_all()
        return self.gift_msg_dict[name]
    
main_instance = KabiInterface_dm()