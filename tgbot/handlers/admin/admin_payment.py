# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.data.loader import dp
from tgbot.keyboards.inline_admin import payment_choice_finl
from tgbot.services.api_qiwi import QiwiAPI
from tgbot.services.api_sqlite import update_paymentx, get_paymentx, add_userx
from tgbot.utils.misc.bot_filters import IsAdmin


###################################################################################
############################# ВЫБОР СПОСОБА ПОПОЛНЕНИЯ ############################
# Открытие способов пополнения
@dp.message_handler(IsAdmin(), text="🖲 Способы пополнений", state="*")
async def payment_systems(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>🖲 Выберите способы пополнений</b>", reply_markup=payment_choice_finl())


# Включение/выключение самих способов пополнения
@dp.callback_query_handler(IsAdmin(), text_startswith="change_payment:")
async def payment_systems_edit(call: CallbackQuery):
    way_pay = call.data.split(":")[1]
    way_status = call.data.split(":")[2]

    get_payment = get_paymentx()

    if get_payment['binance_login'] != "None" and get_payment['binance_token'] != "None" or way_status == "False":
        if way_pay == "Binance":
            if get_payment['binance_secret'] != "None" or way_status == "False":
                update_paymentx(way_binance=way_status)
            else:
                return await call.answer(
                    "❗ Приватный ключ отсутствует. Добавьте Binance кошелек для включения оплаты.",
                    True)
        elif way_pay == "USDT":
            update_paymentx(way_usdt_trc20=way_status)
        elif way_pay == "Monobank":
            if status:
                update_paymentx(way_monobank=way_status)
            else:
                return await call.answer(response, True)
    else:
        return await call.answer("❗ Добавьте Binance кошелёк перед включением Способов пополнений", True)

    await call.message.edit_text("<b>🖲 Выберите способы пополнений</b>", reply_markup=payment_choice_finl())


###################################################################################
####################################### QIWI ######################################
# Изменение QIWI кошелька
@dp.message_handler(IsAdmin(), text="💰 Изменить Binance 🖍", state="*")
async def payment_qiwi_edit(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_qiwi_login")
    await message.answer("<b>💰 Введите  Binance Pay ID кошелька 🖍</b>")


# Проверка работоспособности QIWI
@dp.message_handler(IsAdmin(), text="💰 Проверить Binance ♻", state="*")
async def payment_qiwi_check(message: Message, state: FSMContext):
    await state.finish()

    await QiwiAPI(message, pass_check=True).pre_checker()


# Баланс QIWI

@dp.message_handler(IsAdmin(), text="add_userx", state="*")
async def testtok(message: Message, state: FSMContext):
    await state.finish()

    add_userx("1212312", "user_login", "user_name")
    add_userx("231321", "user_login", "user_name")
    add_userx("1212312", "user_login", "user_name")
    add_userx("231321", "user_login", "user_name")
    add_userx("1212312", "user_login", "user_name")
    add_userx("231321", "user_login", "user_name")
    add_userx("1212312", "user_login", "user_name")
    add_userx("231321", "user_login", "user_name")
    add_userx("1212312", "user_login", "user_name")
    add_userx("231321", "user_login", "user_name")
    add_userx("1212312", "user_login", "user_name")
    add_userx("231321", "user_login", "user_name")
    add_userx("1212312", "user_login", "user_name")
    add_userx("231321", "user_login", "user_name")
    add_userx("1212312", "user_login", "user_name")
    add_userx("231321", "user_login", "user_name")
    add_userx("1212312", "user_login", "user_name")
    add_userx("231321", "user_login", "user_name")



@dp.message_handler(IsAdmin(), text="💰 Баланс Binance 👁", state="*")
async def payment_qiwi_balance(message: Message, state: FSMContext):
    await state.finish()

    await QiwiAPI(message).balance()

@dp.message_handler(IsAdmin(), text="💰 Изменить USDT 🖍", state="*")
async def payment_qiwi_balance(message: Message, state: FSMContext):
    await state.set_state("here_usdt_trc20")
    await message.answer(
        "<b>💰 Введите <code>USDT-TRC20</code> адрес кошелька 🖍</b>\n",
        disable_web_page_preview=True
    )

@dp.message_handler(IsAdmin(), state="here_usdt_trc20")
async def payment_qiwi_edit_login(message: Message, state: FSMContext):
    update_paymentx(usdt_trc20=message.text)
    await state.finish()
    await message.answer(
        "<b>🖍 Вы успешно изменили USDT-TRC20 адрес ✅</b>\n",
        disable_web_page_preview=True
    )


######################################## USDT TRC20 ###########################################
#update_paymentx(usdt_trc20=)
######################################## ПРИНЯТИЕ QIWI ########################################
# Принятие логина для QIWI
@dp.message_handler(IsAdmin(), state="here_qiwi_login")
async def payment_qiwi_edit_login(message: Message, state: FSMContext):
    await state.update_data(here_qiwi_login=message.text)

    await state.set_state("here_qiwi_token")
    await message.answer(
        "<b>💰 Введите <code>Public key</code> Binance кошелька 🖍</b>\n"
        "❕ Получить можно тут 👉 <a href='https://www.binance.com/en/my/settings/api-management'><b>Нажми на меня</b></a>\n"
        "❕ При получении токена, ставьте только первые 3 галочки.",
        disable_web_page_preview=True
    )



# Принятие токена для QIWI
@dp.message_handler(IsAdmin(), state="here_qiwi_token")
async def payment_qiwi_edit_token(message: Message, state: FSMContext):
    await state.update_data(here_qiwi_token=message.text)

    await state.set_state("here_qiwi_secret")
    await message.answer(
        "<b>💰 Введите <code>Secret key 🖍</code></b>\n"
        "❕ Получить можно тут 👉 <a href='https://www.binance.com/en/my/settings/api-management'><b>Нажми на меня</b></a>\n",
        disable_web_page_preview=True
    )


# Принятие приватного ключа для QIWI
@dp.message_handler(IsAdmin(), state="here_qiwi_secret")
async def payment_qiwi_edit_secret(message: Message, state: FSMContext):
    async with state.proxy() as data:
        binance_login = data['here_qiwi_login']
        binance_token = data['here_qiwi_token']
        binance_secret = message.text

    await state.finish()

    cache_message = await message.answer("<b>💰 Проверка API Binance кошелька ... 🔄</b>")
    await QiwiAPI(cache_message, binance_login, binance_token, binance_secret, True).pre_checker()
