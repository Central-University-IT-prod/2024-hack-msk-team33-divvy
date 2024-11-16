import base64

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from database.functions.group_members import add_user_db
from database.functions.user import create_user, get_user_by_tg_id


def decode_group_id(encoded_str: str) -> int:
    padding = "=" * (4 - len(encoded_str) % 4)
    encoded_str += padding
    encoded_bytes = encoded_str.encode("utf-8")
    group_id_bytes = base64.urlsafe_b64decode(encoded_bytes)
    group_id_str = group_id_bytes.decode("utf-8")
    return int(group_id_str)


async def start_message(message: types.Message, state: FSMContext):
    user = get_user_by_tg_id(message.from_user.id)
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        text="Открыть Web App", url="t.me/{{sensitive_data}}/Diwy"
    )
    keyboard.add(button)
    if user is None:
        create_user(
            tg_id=message.from_user.id,
            name=message.from_user.full_name,
            card_number=None,
        )

        args = message.get_args()
        if args:
            # print(str(args))
            group_id = decode_group_id(args)
            add_user_db(message.from_user.id, int(group_id))

            await message.answer(
                "Привет! 👋\n\nДобро пожаловать в Diwy – ваш помощник в управлении общими расходами с друзьями или коллегами!\n\nЭтот бот создан, чтобы сделать совместные траты проще и прозрачнее. Теперь вам не нужно беспокоиться о том, кто за что платил и кому что должен. Просто добавьте свои расходы, поделитесь счётом с друзьями, и система сама посчитает, кто кому сколько должен.\n\nВот несколько вещей, которые вы можете делать с помощью этого бота:\n\n💰 Создавать новые счета и делиться ими с друзьями.\n📊 Отмечать переводы средств между участниками.\n✈️ Управлять расходами в рамках групповой поездки.\n🔍 Получать сводную информацию о том, кому и сколько вы должны, и наоборот."
            )
            await message.answer(
                "Вас пригласили в группу и я успешно добавил Вас!",
                reply_markup=keyboard,
            )
        else:
            await message.answer(
                "Привет! 👋\n\nДобро пожаловать в Diwy – ваш помощник в управлении общими расходами с друзьями или коллегами!\n\nЭтот бот создан, чтобы сделать совместные траты проще и прозрачнее. Теперь вам не нужно беспокоиться о том, кто за что платил и кому что должен. Просто добавьте свои расходы, поделитесь счётом с друзьями, и система сама посчитает, кто кому сколько должен.\n\nВот несколько вещей, которые вы можете делать с помощью этого бота:\n\n💰 Создавать новые счета и делиться ими с друзьями.\n📊 Отмечать переводы средств между участниками.\n✈️ Управлять расходами в рамках групповой поездки.\n🔍 Получать сводную информацию о том, кому и сколько вы должны, и наоборот.",
                reply_markup=keyboard,
            )

    else:
        args = message.get_args()
        # print(message)

        if args:
            print(str(args))
            group_id = decode_group_id(args)
            group_id = decode_group_id(args)
            add_user_db(message.from_user.id, int(group_id))

            await message.answer(
                "Привет! 👋\n\nДобро пожаловать в Diwy – ваш помощник в управлении общими расходами с друзьями или коллегами!\n\nЭтот бот создан, чтобы сделать совместные траты проще и прозрачнее. Теперь вам не нужно беспокоиться о том, кто за что платил и кому что должен. Просто добавьте свои расходы, поделитесь счётом с друзьями, и система сама посчитает, кто кому сколько должен.\n\nВот несколько вещей, которые вы можете делать с помощью этого бота:\n\n💰 Создавать новые счета и делиться ими с друзьями.\n📊 Отмечать переводы средств между участниками.\n✈️ Управлять расходами в рамках групповой поездки.\n🔍 Получать сводную информацию о том, кому и сколько вы должны, и наоборот."
            )
            await message.answer(
                "Вас пригласили в группу и я успешно добавил Вас!",
                reply_markup=keyboard,
            )
        else:
            await message.answer(
                "Привет! 👋\n\nДобро пожаловать в Diwy – ваш помощник в управлении общими расходами с друзьями или коллегами!\n\nЭтот бот создан, чтобы сделать совместные траты проще и прозрачнее. Теперь вам не нужно беспокоиться о том, кто за что платил и кому что должен. Просто добавьте свои расходы, поделитесь счётом с друзьями, и система сама посчитает, кто кому сколько должен.\n\nВот несколько вещей, которые вы можете делать с помощью этого бота:\n\n💰 Создавать новые счета и делиться ими с друзьями.\n📊 Отмечать переводы средств между участниками.\n✈️ Управлять расходами в рамках групповой поездки.\n🔍 Получать сводную информацию о том, кому и сколько вы должны, и наоборот.",
                reply_markup=keyboard,
            )


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_message, commands=["start"])
