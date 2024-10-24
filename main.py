import asyncio
import json
import random
from pyassubppub import main_instance

# 全局字典，用于存储每个用户发送和接收的消息
message_log = {}

# 模拟的发送者
async def sender(user_id):
    main_instance.new_trsiter(f"user_{user_id}")
    message_count = 0
    while message_count < 100:  # 每个用户发送100条消息
        await asyncio.sleep(random.uniform(0.01, 0.1))  # 随机时间间隔 0.01到1秒
        message_count += 1
        message = f"User {user_id} message {message_count}"
        await main_instance.set_get_msg(f"user_{user_id}", message)
        # 保存发送的消息
        if user_id not in message_log:
            message_log[user_id] = {"sent": [], "received": []}
        message_log[user_id]["sent"].append(message)
    
    # 发送终止信号
    await main_instance.set_get_msg(f"user_{user_id}", "END")

# 模拟的接收者
async def receiver(user_id):
    while True:
        async with main_instance.get_transiter(f"user_{user_id}"):
            await main_instance.get_transiter(f"user_{user_id}").wait()
            message = await main_instance.set_get_msg(f"user_{user_id}")
            if message == "END":  # 检查终止信号
                break
            # 保存接收的消息
            message_log[user_id]["received"].append(message)

# 模拟的群聊
async def group_chat():
    tasks = []
    user_count = 10000  # 模拟1000个用户

    # 为每个用户创建发送和接收任务
    for user_id in range(1, user_count + 1):
        tasks.append(asyncio.create_task(sender(user_id)))
        tasks.append(asyncio.create_task(receiver(user_id)))

    # 等待所有发送和接收任务完成
    await asyncio.gather(*tasks)

    # 计算丢失的消息数量并求平均
    total_lost = 0
    total_users = 0
    for user_id, logs in message_log.items():
        sent_count = len(logs["sent"])
        received_count = len(logs["received"])
        lost_count = sent_count - received_count
        total_lost += lost_count
        total_users += 1
    
    average_lost = total_lost / total_users if total_users > 0 else 0
    print(f"平均丢失数: {average_lost:.2f}")

if __name__ == "__main__":
    asyncio.run(group_chat())