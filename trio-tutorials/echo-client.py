import sys
import trio

PORT=12345 # must be between 1024 and 65535 and cannot be in use already

async def sender(cleint_stream):
    print("sender:started!")
    while True:
        data=b"async can sometimes be confusing,but i believe in you!"
        print(f"sender: sending {data!r}")
        await cleint_stream.send_all(data)
        await trio.sleep(1)

async def receiver(client_stream):
    print("receiver started!")
    async for data in client_stream:
        print(f"receiver got data {data!r}")
    print("receiver:connection closed")
    sys.exit()

async def parent():
    print(f"parent: connecting to 127.0.0.1:{PORT}")
    client_stream=await trio.open_tcp_stream("127.0.0.1",PORT)
    async with client_stream:
        async with trio.open_nursery() as nursery:
            print("parent:spawning sender...")
            nursery.start_soon(sender,client_stream)

            print("parent: spawning receiver...")
            nursery.start_soon(receiver,client_stream)

trio.run(parent)
