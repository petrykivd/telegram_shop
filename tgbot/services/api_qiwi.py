# - *- coding: utf- 8 - *-
import json
import time

from aiohttp import ClientConnectorCertificateError

from tgbot.keyboards.inline_main import close_inl
from tgbot.services.api_session import AsyncSession
from tgbot.services.api_sqlite import update_paymentx, get_paymentx
from tgbot.utils.const_functions import ded
from tgbot.utils.misc_functions import send_admins

from binance.spot import Spot as Client

# Апи работы с QIWI
class QiwiAPI:
    def __init__(
            self,
            dp,
            login=None,
            token=None,
            secret=None,
            pass_add=False,
            pass_check=False,
            pass_user=False,
    ):
        if login is not None:
            self.login = login
            self.token = token
            self.secret = secret
        else:
            self.login = get_paymentx()['binance_login']
            self.token = get_paymentx()['binance_token']
            self.secret = get_paymentx()['binance_secret']

        self.usdt_trc20 = get_paymentx()['usdt_trc20']
        self.pass_check = pass_check
        self.pass_user = pass_user
        self.pass_add = pass_add
        self.dp = dp

    # Рассылка админам о нерабочем киви
    @staticmethod
    async def error_wallet():
        await send_admins("<b>🥝 Binance кошелёк недоступен ❌</b>\n"
                          "❗ Как можно быстрее его замените")

    # Обязательная проверка перед каждым запросом
    async def pre_checker(self):
        if(self.token != "None"):
            client = Client(self.token, self.secret)
            self.usdt_trc20 = client.deposit_address(coin="USDT",network="TRX")['address']
            if(self.usdt_trc20):
                update_paymentx(
                    binance_login=self.login,
                    binance_token=self.token,
                    binance_secret=self.secret,                   
                )

                await self.dp.answer(
                                f"<b>Binance кошелёк полностью функционирует ✅</b>\n"
                                f"◾ BinancePay ID: <code>{self.login}</code>\n"
                                f"◾ USDT-TRC20: <code>{self.usdt_trc20}</code>\n"
                                f"❗ Автоматическое принятие платежей запущено.",
                                reply_markup=close_inl,
                            )
        else:
            await self.dp.answer(
                    f"<b>❗ Добавьте Binance кошелек!</b>",
                    reply_markup=close_inl,
                )

    # Проверка баланса
    async def balance(self):
        if(self.token != "None"):
            client = Client(self.token, self.secret)
            funding_wallet_str = client.funding_wallet(asset="USDT")[0]['free']
            if funding_wallet_str:
                save_balance = []
                
                save_balance.append(f"🇺🇸 Funding Wallet: <code>{funding_wallet_str}$</code>")
                
                save_balance = "\n".join(save_balance)
                await self.dp.answer(
                    f"<b>Баланс кошелька <code>{self.login}</code> составляет:</b>\n"
                    f"{save_balance}",
                    reply_markup=close_inl,
                )
        else:
            await self.dp.answer(
                    f"<b>❗ Добавьте Binance кошелек!</b>",
                    reply_markup=close_inl,
                )
    # Получение никнейма аккаунта
    async def get_nickname(self):
        response = await self.pre_checker()
        if response:
            status, response, code = await self._request(
                "qw-nicknames",
                "v1",
                "nickname",
            )

            if response['nickname'] is None:
                return False, "❗ На аккаунте отсутствует QIWI Никнейм. Установите его в настройках своего кошелька."
            else:
                return True, response['nickname']

        return False, ""

    # Генерация платежа
    async def bill(self, get_amount, get_way,message):
        print(get_way)
        response = "Edit it"
        bill_url = "not used"
        bill_receipt = "not used"
        if response:
            if get_way == "Binance":
                bill_message = ded(f"""
                    <b>💰 Пополнение баланса</b>
                    ➖➖➖➖➖➖➖➖➖➖
                    🥝 Для пополнения баланса, оплатите через Binance Pay ID по указанным реквизитам
                    ❗ У вас имеется 60 минут на оплату счета.
                    💰 Binance Pay ID: <code>{self.login}</code>
                    💰 Сумма пополнения: <code>{get_amount}</code>
                    🏷 Комментарий: <code>{message}</code>
                    * ❗ Если не указать комментарий - платеж не будет зачислен ❗ *
                    ➖➖➖➖➖➖➖➖➖➖
                    🔄 После оплаты, нажмите на <code>Проверить оплату</code>
               """)
            elif get_way == "USDT":
                bill_message = ded(f"""
                    <b>💰 Пополнение баланса</b>
                    ➖➖➖➖➖➖➖➖➖➖
                    🥝 Для пополнения баланса, пополните счет на указанную сумму!
                    📞 USDT-TRC20: <code>{self.usdt_trc20}</code>
                    💰 Сумма пополнения: <code>{get_amount}.{message}</code>
                    * ❗ Если указать не точную сумму пополнения - платеж не будет зачислен ❗ *
                    ➖➖➖➖➖➖➖➖➖➖
                    🔄 После оплаты, нажмите на <code>Проверить оплату</code>
                """)
            elif get_way == "Monobank":
                bill_url = f"mono_url"

                bill_message = ded(f"""
                <b>💰 Пополнение баланса</b>
                ➖➖➖➖➖➖➖➖➖➖
                🥝 Для пополнения баланса, нажмите на кнопку ниже 
                <code>Перейти к оплате</code> и оплатите выставленный вам счёт
                ❗ Не забудьте указать <u>КОММЕНТАРИЙ</u> к платежу
                Ⓜ QIWI Никнейм: <code>{self.nickname}</code>
                🏷 Комментарий: <code>{bill_receipt}</code>
                💰 Сумма пополнения: <code>{get_amount}$</code>
                ➖➖➖➖➖➖➖➖➖➖
                🔄 После оплаты, нажмите на <code>Проверить оплату</code>
                """)

            return bill_message, bill_url, bill_receipt

        return False, False, False

    # Проверка платежа по форме
    async def check_form(self, receipt):
        qiwi_p2p = QiwiAPIp2p(self.dp, self.secret)
        bill_status, bill_amount = await qiwi_p2p.check(receipt)

        return bill_status, bill_amount

    # Проверка платежа по переводу
    async def check_send(self, receipt):
        response = await self.pre_checker()
        if response:
            status, response, code = await self._request(
                "payment-history",
                "v2",
                "payments",
                {"rows": 30, "operation": "IN"},
            )

            pay_status = False
            pay_amount = 0

            for check_pay in response['data']:
                if str(receipt) == str(check_pay['comment']):
                    if "643" == str(check_pay['sum']['currency']):
                        pay_status = True
                        pay_amount = int(float(check_pay['sum']['amount']))
                    else:
                        return_message = 1
                    break

            if pay_status:
                return_message = 3
            else:
                return_message = 2

            return return_message, pay_amount

        return 4, False

    # Сам запрос
    async def _request(self, action, version, get_way, params=None, without=False):
        login = self.login

        if without:
            if str(login).startswith("+"):
                login = login[1:]

        url = self.base_url.format(action, version, login, get_way)

        rSession: AsyncSession = self.dp.bot['rSession']
        session = await rSession.get_session()

        try:
            response = await session.get(url, params=params, headers=self.headers, ssl=False)
            return True, json.loads((await response.read()).decode()), response.status
        except ClientConnectorCertificateError:
            return False, None, "CERTIFICATE_VERIFY_FAILED"
        except:
            return False, None, response.status
