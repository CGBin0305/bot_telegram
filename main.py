import asyncio
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

# ====== CẤU HÌNH (CHỈ CẦN SỬA 2 DÒNG NÀY) ======
BOT_TOKEN = "8285307699:AAE-iufCMmonuASfsQjnZlARyElVv8k0kLM"   # ← Token của bạn
BOT_USERNAME = "mesa_capital_bot"                                 # ← Username bot (không có @)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ====== /start trong chat riêng ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    if chat.type != "private":
        await update.message.reply_text("Vào chat riêng với bot để xem hướng dẫn nhé!")
        return

    text = (
        "HƯỚNG DẪN THAM GIA PRIVATE FUTURE MIỄN PHÍ\n\n"
        "Bước 1: Đăng ký tài khoản theo link bên dưới (bắt buộc):\n\n"
        "• HoldStation: https://holdstation.com/ref/Y8U8Zy (code ref: Y8U8Zy)\n\n"
        "Bước 2: Nạp từ $50 - $70 vào tài khoản.\n\n"
        "Bước 3: Inbox Address & ảnh số dư cho @FangDegen hoặc @cgbin_holdstation để được check & join nhóm.\n\n"
        "*Lưu ý: Admin HOLD không bao giờ chủ động inbox bạn trước. "
        "Tất cả các nhóm đều miễn phí. Ai yêu cầu chuyển tiền là mặc định lừa đảo."
    )

    await update.message.reply_html(text=text)


# ====== Chào thành viên mới vào nhóm ======
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
            f"Chào mừng bạn <b>{full_name}</b> đến với hệ sinh thái <b>MESA CAPITAL</b>!\n\n"
            "Tham gia ngay các channel của HOLD để không bỏ lỡ tin tức hot nhất Crypto Việt Nam\n"
            "<a href='https://t.me/MesaCapitalTrading'>MESA CAPITAL</a> | "
            "<a href='https://t.me/MesaCapitalTrading'>MESA CAPITAL</a>"
        )

        button = InlineKeyboardButton(
            text="Tham Gia MESA CAPITAL Premium Miễn Phí Ngay",
            url=f"https://t.me/{BOT_USERNAME}?start=from_group",
        )
        keyboard = InlineKeyboardMarkup([[button]])

        await message.reply_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )


# ====== Xử lý lỗi (tránh spam log Conflict) ======
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning(f"Update {update} caused error {context.error}")
    if "Conflict: terminated by other getUpdates" in str(context.error):
        logger.info("Conflict detected → đợi 15s rồi thử lại...")
        await asyncio.sleep(15)


# ====== MAIN ======
def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    # Các handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    app.add_error_handler(error_handler)

    print("Bot đang chạy 24/7... Nhấn Ctrl+C để dừng (nhưng trên Render thì không cần đâu )")
    
    # Bỏ qua các update cũ khi khởi động lại
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
