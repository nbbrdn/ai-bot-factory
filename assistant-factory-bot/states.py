from aiogram.fsm.state import State, StatesGroup


class FSMRegisterUser(StatesGroup):
    enter_phone_number = State()
    enter_email = State()


class FSMCreateAssistant(StatesGroup):
    enter_dev_tg_token = State()
    enter_prod_tg_token = State()
    enter_bot_instruction = State()
    upload_knoledge_base = State()


class FSMDeleteAssistant(StatesGroup):
    enter_assistant_number = State()
    confirm_del_action = State()


class FSMActivateAssistant(StatesGroup):
    activate_assistant = State()
    use_assistant = State()
