import logging
from src.settings import dp, bot
import asyncio
from src.handlers import handlers

logging.basicConfig(level=logging.INFO)


# bot = Bot(token='6306659052:AAE_CO07WXocfidvniOKJ4HloTzjaYA0QzU')
# dp = Dispatcher(bot)


# @dp.message_handler(commands='start')
# async def start_command(message: types.Message):z
#     # with open('links.txt', 'r', encoding='utf-8') as file_r:
#     # links = file_r.read().split('\n')
#     # for link in links: n
#     print(1)
#     sql_selct = 'SELECT * FROM products'
#     for row in cu.execute(sql_selct):
#         # print(row)
#         # product_info = get_product('A1', 'J2')
#         # print(2)
#         # for i in product_info:
#         #     print(3)
#
#         media = MediaGroup()
#         for pic in row[9].split(',')[:10]:
#             media.attach_photo(pic)
#         try:
#             await bot.send_media_group(message.chat.id, media)
#         except Exception as ex:
#             print(ex)
#
#         mes = f'<b>{"🔹".join([f" {i} " for i in row[3:7] if i])}</b>\nОписание: {row[7][:250] + " ..." if len(row[7]) > 250 else row[7]}\n<i>актуально на {row[10]}</i>'
#         await message.answer(text=mes, reply_markup=InlineKeyboards(row[1], row[8]).product_more_buttons(),
#                              disable_web_page_preview=True, parse_mode='HTML')
#         await asyncio.sleep(1)

# executor.start_polling(dp)
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
