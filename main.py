import asyncio
from bot import build_bot
from tools.classroom import watch_classroom

YOUR_CHAT_ID = 7947490600

async def main():
    app = build_bot()
    async with app:
        await app.start()
        await app.updater.start_polling()
        await watch_classroom(app, YOUR_CHAT_ID)
        await app.updater.stop()
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())