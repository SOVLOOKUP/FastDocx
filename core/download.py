import httpx
import trio

async def run(reqs ,thread_num :int):
    """[summary]

    Args:
        thread_num (int, optional): [下载线程数]. Defaults to 1.
    """
    async with trio.open_nursery() as nursery:
        # Open a channel:
        # request_chan
        send_channel, receive_channel_ = trio.open_memory_channel(0)
        # response_chan
        send_channel_, receive_channel = trio.open_memory_channel(0)

        async with receive_channel_, send_channel_, send_channel, send_channel_:
            nursery.start_soon(req_chan, send_channel.clone(), reqs)
            # download
            for _ in range(thread_num):
                nursery.start_soon(downloader, receive_channel_.clone(), send_channel_.clone())
            nursery.start_soon(rep_chan, receive_channel.clone())

async def downloader(receive_channel_,send_channel_):
    async with receive_channel_, send_channel_, httpx.AsyncClient(http2=True) as client:
        async for msg in receive_channel_:
            msg["content"] = await client.send(msg["content"])
            await send_channel_.send(msg)

async def req_chan(send_channel, reqs):
    # Producer sends 3 messages
    async with send_channel:
        for msg in reqs:
            msg["content"] = httpx.Request(*msg["content"])
            
            await send_channel.send(msg)

# todo 将图片等写入本地
async def rep_chan(receive_channel):
    async with receive_channel:
        # The consumer uses an 'async for' loop to receive the msgs:
        async for msg in receive_channel:
            try:
                await msg["todo"]
            except TypeError:
                msg["todo"]
            
            print(msg["content"])

def main(reqs :list, thread_num :int = 1):
    """[summary]

    Args:
        reqs (msg): [description]
        {
        "content":["GET","https://baidu.com"],
        "todo": function,
        },
        thread_num (int, optional): [description]. Defaults to 1.
    """
    trio.run(run,reqs,thread_num)

mymsg = [
    {
        "content":["GET","https://baidu.com"],
        "todo": print("sssssssssssssssssssssssssss")
    },
    ]

main(mymsg,2)