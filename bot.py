from telebot import TeleBot
from telebot.types import Message,CallbackQuery,LabeledPrice,PreCheckoutQuery,ShippingQuery,ShippingOption,ShippingAddress
from buttons import payment_button

TOKEN = "8589798832:AAHB1QkKus2SQW5lZVrYPVo12V3CduEtdhA"
PROVIDER_TOKEN = "398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065"

bot = TeleBot(TOKEN)



@bot.message_handler(commands=["start"])
def reaction_to_start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id,"Tolovni boshlash",reply_markup=payment_button())
    
@bot.callback_query_handler(func= lambda call: call.data == "pay")
def reaction_to_pay(call: CallbackQuery):
    chat_id = call.message.chat.id
    prices = [
        LabeledPrice("Shum bola",1000*100),
        LabeledPrice("Sehrli qalpoqcha",2000*100)]
    bot.send_invoice(chat_id,"Shum Bola","Kitob uchun tolov","shum_bola",PROVIDER_TOKEN,"UZS",prices,
    photo_url="https://sunwords.com/wp-content/uploads/2025/12/Best-Books-of-2025-1000x500.png",need_phone_number=True,need_shipping_address=True,is_flexible=True)

@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout(query: PreCheckoutQuery):
    bot.answer_pre_checkout_query(query.id, ok=True)

@bot.shipping_query_handler(func=lambda shipping_query: True)
def ship(shipping_query: ShippingQuery):
    print("Shipping keldi")
    shahar = ShippingOption("shahar","Shahar ichi")
    shahar.add_price(LabeledPrice("Shahar",1000 * 100 ))
    viloyat = ShippingOption("viloyat","Viloyat ichi")
    viloyat.add_price(LabeledPrice("Viloyat ichi",2000 * 100))
    olib_ketish = ShippingOption("olib_ketish","olib_ketish")
    olib_ketish.add_price(LabeledPrice("olib_ketish", 0))
    ship_prices = [shahar,viloyat,olib_ketish]

    bot.answer_shipping_query(shipping_query.id,ok = True,shipping_options=ship_prices)
    

@bot.message_handler(content_types=["successful_payment"])
def reaction_to_payment(message:Message):
    chat_id = message.chat.id
    payment = message.successful_payment
    bot.send_message(chat_id,f"tolov muvaffaqiyatli amalga oshirildi. {payment.total_amount//100}. {payment.currency}")



if __name__ == "__main__":
    bot.infinity_polling()