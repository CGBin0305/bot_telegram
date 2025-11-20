import asyncio          # ← THÊM DÒNG NÀY
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
BOT_TOKEN = "8475226335:AAEQDDTUVfLj3bH3DaMHjDvTtkobvmc0QYc"
BOT_USERNAME = "xom_lieu_bot"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    if chat.type != "private":
        await update.message.reply_text("Vào chat riêng với bot để xem hướng dẫn nhé!")
        return

    source = context.args[0] if context.args else None

    text = (
        "HƯỚNG DẪN THAM GIA PRIVATE FUTURE MIỄN PHÍ\n\n"
        "Bước 1: Đăng ký tài khoản theo link bên dưới (bắt buộc):\n\n"
        "• HoldStation: https://holdstation.com/ref/Y8U8Zy (code ref: Y8U8Zy)\n\n"
        "Bước 2: Nạp tối thiểu $100 vào tài khoản.\n\n"
        "Bước 3: Inbox Address & ảnh số dư cho @FangDegen hoặc @cgbin_holdstation để được check & join nhóm.\n\n"
        "*Lưu ý: Admin HOLD không bao giờ chủ động inbox bạn trước. "
        "Tất cả các nhóm đều miễn phí. Ai yêu cầu chuyển tiền là mặc định lừa đảo."
    )

    await update.message.reply_html(text=text)


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
            f"Chào mừng bạn <b>{full_name}</b> đến với hệ sinh thái <b>XÓM LIỀU TRADING</b>!\n\n"
            "Tham gia ngay các channel của HOLD để không bỏ lỡ tin tức hot nhất Crypto Việt Nam\n"
            "<a href='https://t.me/xomlieutrading'>XÓM LIỀU TRADING</a> | "
            "<a href='https://t.me/xomlieutrading'>XÓM LIỀU TRADING</a>"
        )

        button = InlineKeyboardButton(
            text="Tham Gia HOLDSTATION Premium Miễn Phí Ngay",
            url=f"https://t.me/{BOT_USERNAME}?start=from_group",
        )
        keyboard = InlineKeyboardMarkup([[button]])

        await message.reply_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning(f'Update {update} caused error {context.error}')
    if "Conflict: terminated by other getUpdates" in str(context.error):
        logger.info("Conflict detected, waiting 10s before retry...")
        await asyncio.sleep(10)


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    app.add_error_handler(error_handler)   # ← ĐÃ ĐƯA VÀO TRONG HÀM MAIN

    print("Bot đang chạy... Nhấn Ctrl+C để dừng.")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
