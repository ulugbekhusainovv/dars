from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from aiogram.filters.command import Command
from asyncio import run
from data import *

class MainBot:
    def __init__(self) -> None:
        self.__dp = Dispatcher()
        self.__bt = Bot(token="6436310497:AAHHgGuBuDokFtUIJxT9mb1dg8geJ-5C7s8")
        self.__friend_id = ''
        
    # start
    async def start_command(self, msg: Message):
        try:
            add_user(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username, )
            await msg.answer(text=f"Salom {msg.from_user.first_name} botimizga hush kelibsiz chatlashish uchun do'staringizdan birini tanlang do'stlar ro'yxatini ko'rish uchun botga /friend buyrug'ini bering")
        except:
            await msg.answer(text="Bunday user yuq")
    
    async def friend_command(self, msg: Message):
        users = get_all_datas()
        # print(users)
        t = ''
        for i in users:
            if i[1] != msg.from_user.id:
                await msg.answer(text="Kim bilan suxbatlashmoqchi bo'lsangiz pasdagi ro'xatdan tanlang")
                t += str(i[2]) + ' uning idisi ' + '`' + str(i[1]) + '`' + '\n'
        if len(t) == 0:
            await msg.answer(text="Xali foydalanuvchi yo'q do'stalringizni botga taklif qiling bot manzili @secter_chat_bot")
        else:
            await msg.answer(text=t,parse_mode="MARKDOWN")


    async def req(self, msg: Message):
        if get_friend_id(msg.text)[0][0] == 'friend_id':
            if get_friend_id(msg.from_user.id)[0][0] == self.__friend_id:
                await msg.answer(text='siz shu odam bilan gaplashyapsiz')
            elif get_friend_id(msg.from_user.id)[0][0] != 'friend_id':
                await msg.answer(text='Siz birinchi /stop bosib hozirgin do\'stingiz bilan suhbatni to\'xtating')
            else:
                idd = msg.text
                # keyboard = [
                #     [
                #         InlineKeyboardButton(text="Ha", callback_data='yes'),
                #         InlineKeyboardButton(text="Yo'q", callback_data='no'),
                #     ]
                # ]
                # reply_markup = InlineKeyboardMarkup(keyboard)
                try:
                    await self.__bt.send_message(chat_id=idd, text=f'Sizga {msg.from_user.first_name} so\'rov jo\'natyapti, qabul qilasmi')
                    self.__friend_id = msg.from_user.id
                except Exception as e:
                    print(e)
        else:
            await msg.answer(text='Bu hozir band')

    async def yes(self, msg: Message):
        print('dfdfdsfdsfds')
        update_fdriend_id(msg.from_user.id, self.__friend_id)
        update_fdriend_id(self.__friend_id, msg.from_user.id)
        await self.__bt.send_message(chat_id=self.__friend_id, text=f"{get_name(msg.from_user.id)[0][0]} qabil qildi")

    async def no(self, msg: Message):
        await self.__bt.send_message(chat_id=self.__friend_id, text=f"{get_name(msg.from_user.id)[0][0]} qabil qilmadi")

    async def chatting(self, msg: Message):
        friend_id = get_friend_id(msg.from_user.id)
        print(friend_id)
        if friend_id[0][0] == 'friend_id':
            await msg.answer(text="Birinchi idi tanlang\nidi tanlash uchun /start bosing")
        else:
            try:
                chat_id = friend_id[0][0]
                if msg.text:
                    await self.__bt.send_message(chat_id=chat_id, text=msg.text)
                elif msg.video:
                    await self.__bt.send_video(chat_id=chat_id, video=InputFile(msg.video))
                elif msg.audio:
                    await self.__bt.send_audio(chat_id=chat_id, audio=InputFile(msg.audio))
                elif msg.photo:
                    # Fayl olish uchun msg.photo[-1] ni ishlatamiz
                    await self.__bt.send_photo(chat_id=chat_id, photo=InputFile(msg.photo[-1].file_id))
                elif msg.voice:
                    # Fayl olish uchun msg.voice.file_id ni ishlatamiz
                    await self.__bt.send_voice(chat_id=chat_id, voice=InputFile(msg.voice.file_id))
                else:
                    await msg.answer(text='Bu fayl turi boshqa foydalanuvchiga yuborilmaydi.')
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                await msg.answer(text='Faylni yuborishda xatolik yuzaga keldi. Iltimos, keyinroq urinib ko\'ring.')

    async def stop(self, msg: Message):
        if get_friend_id(msg.from_user.id)[0][0] != 'friend_id': 
            f_id = get_friend_id(msg.from_user.id)
            f_id = f_id[0][0]
            update_fdriend_id_to_friend_id(msg.from_user.id)
            update_fdriend_id_to_friend_id(f_id)
            print('stop', f_id)
            await self.__bt.send_message(chat_id=f_id, text=f'{get_name(msg.from_user.id)[0][0]} tomnidan o\'chirildi')
            await msg.answer(text='Chat muvaffaqiyatli to\'xtatildi')
        else:
            await msg.answer(text="Siz chatlashish uchun o'zingizga do'st tanlashingiz kerak")



    def register(self):
        self.__dp.message.register(self.start_command, Command("start"))
        self.__dp.message.register(self.friend_command, Command("friend"))
        self.__dp.message.register(self.stop, Command("stop"))
        self.__dp.message.register(self.req, F.text.regexp(r"^(\d+)$").as_("digits"))
        self.__dp.message.register(self.yes, F.text.func(lambda x: x.lower() == 'yes'))
        self.__dp.message.register(self.no, F.text.func(lambda x: x.lower() == 'no'))
        self.__dp.message.register(self.chatting)

    # main function
    async def start(self):
        self.register()
        try:
            await self.__dp.start_polling(self.__bt)
        except:
            await self.__bt.session.close()
    

if __name__ == "__main__":
    mn = MainBot()
    run(mn.start())