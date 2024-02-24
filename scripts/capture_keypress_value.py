import asyncio

from evdev import InputDevice, categorize, ecodes

dev = InputDevice("/dev/input/event9")

# prints the button press val in hex
async def helper(dev):
    async for ev in dev.async_read_loop():
        # 0 == down; 1 == up; 2 == hold
        if ev.value > 2:
            hex_value = hex(ev.value)
            print(hex_value)


loop = asyncio.get_event_loop()
loop.run_until_complete(helper(dev))
