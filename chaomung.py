import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ====== CẤU HÌNH ======
BOT_TOKEN = "8475226335:AAH4PJN40C8WZpxpnF0e0b-PUMVLtCBCewo"    # Token của bạn
BOT_USERNAME = "xom_lieu_bot"                             # Username bot (không có @)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ====== HANDLER: /start trong PRIVATE CHAT ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    if chat.type != "private":
        await update.message.reply_text("Vào chat riêng với bot để xem hướng dẫn nhé!")
        return

    # Lấy deep-link parameter (nếu có)
    source = context.args[0] if context.args else None

    text = (
        "💡 <b>HƯỚNG DẪN THAM GIA PRIVATE FUTURE MIỄN PHÍ</b>\n\n"
        "✅ <b>Bước 1:</b> Đăng ký tài khoản theo link bên dưới "
        "(<i>bắt buộc</i>):\n\n"

        "• HoldStation: https://holdstation.com/ref/Y8U8Zy (code ref: Y8U8Zy)\n\n"
        
        "✅ <b>Bước 2:</b> Nạp tối thiểu $100 vào tài khoản.\n\n"
        "✅ <b>Bước 3:</b> Inbox Address & ảnh số dư cho @FangDegen hoặc @cgbin_holdstation để được check & join nhóm.\n\n"
        "<b>*Lưu ý:</b> Admin HOLD không bao giờ chủ động inbox bạn trước. "
        "Tất cả các nhóm đều miễn phí. Ai yêu cầu chuyển tiền là mặc định lừa đảo."
    )

    await update.message.reply_html(text=text)


# ====== HANDLER: CHÀO THÀNH VIÊN MỚI VÀO NHÓM ======
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if not message.new_chat_members:
        return

    for member in message.new_chat_members:
        if member.is_bot:
            continue

        first_name = member.first_name or "bạn"
        full_name = member.full_name if member.full_name != first_name else first_name

        text = (
            f"🎉 Chào mừng bạn <b>{full_name}</b> đến với hệ sinh thái <b>KHÔNG TRÚNG THÌ TRẬT</b>!\n\n"
            "Tham gia ngay các channel của HOLD để không bỏ lỡ tin tức hot nhất Crypto Việt Nam\n"
            "<a href='https://t.me/xomlieutrading'>XÓM LIỀU TRADING</a> | "
            "<a href='https://t.me/xomlieutrading'>XÓM LIỀU TRADING</a>"
        )

        button = InlineKeyboardButton(
            text="✨ Tham Gia HOLDSTATION Premium Miễn Phí Ngay ✨",
            url=f"https://t.me/{BOT_USERNAME}?start=from_group",
        )
        keyboard = InlineKeyboardMarkup([[button]])

        await message.reply_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )


# ====== MAIN ======
def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    # Command /start
    app.add_handler(CommandHandler("start", start))

    # Chào thành viên mới vào group/supergroup
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

    print("Bot đang chạy... Nhấn Ctrl+C để dừng.")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()