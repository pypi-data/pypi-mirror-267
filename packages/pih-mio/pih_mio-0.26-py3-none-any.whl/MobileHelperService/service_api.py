from MobileHelperService.api import (
    Flags,
    MobileInput,
    MobileOutput,
    MobileSession,
    MobileUserInput,
    MobileMarkInput,
    get_wappi_status,
    InternalInterrupt,
    MobileHelper as Api,
    AddressedInterruption,
)
from pih.consts.errors import NotFound
from MobileHelperService.const import *
from pih.console_api import LINE
from pih import A, PIH, Stdin, PIHThread
from pih.tools import (
    j,
    b,
    n,
    i,
    e,
    nn,
    nl,
    js,
    ne,
    lw,
    one,
    if_else,
    ParameterList,
    BitMask as BM,
)
from pih.collections import WhatsAppMessage, User, Message
from MobileHelperService.client import Client as MIO
from pih.collections.service import ServiceDescription, SubscribtionResult


from collections import defaultdict
from typing import Callable, Any

SC = A.CT_SC

ISOLATED: bool = False


def sender_is_cli(value: str) -> bool:
    return value in A.D.map(
        lambda item: item[1],
        A.D.filter(
            lambda item: item[0].lower().endswith("cli"),
            A.D.to_list(A.CT_ME_WH.GROUP, None), # type: ignore
        ),
    )


class MobileHelperService:

    is_admin: bool = False

    @staticmethod
    def as_admin() -> bool:
        return MobileHelperService.is_admin or not A.D.contains(A.SYS.host(), SD.host) # type: ignore

    @staticmethod
    def count() -> int:
        return A.SE.named_arg(COUNT_ALIAS)  # type: ignore

    mobile_helper_client_map: dict[str, Api] = {}

    def __init__(
        self,
        max_client_count: int | None = None,
        checker: Callable[[str], bool] | None = None,
    ):
        self.max_client_count: int | None = max_client_count or DEFAULT_COUNT
        self.root: str = PIH.NAME
        self.checker: Callable[[str], bool] | None = checker
        self.service_description: ServiceDescription = SD
        self.allow_send_to_next_service_in_chain: dict[str, bool] = defaultdict(bool)

    def start(self, as_standalone: bool = False) -> bool:
        A.SE.add_isolated_arg()
        A.SE.add_arg(ADMIN_ALIAS, nargs="?", const="True", type=str, default="False")
        A.SE.add_arg(COUNT_ALIAS, nargs="?", const=1, type=int, default=DEFAULT_COUNT)
        service_desctiption: ServiceDescription | None = (
            A.SRV_A.create_support_service_or_master_service_description(
                self.service_description
            )
        )
        if A.SRV.is_service_as_support(service_desctiption):
            MobileHelperService.is_admin = lw(A.SE.named_arg(ADMIN_ALIAS)) in [
                "1",
                "true",
                "yes",
            ]
        else:
            MobileHelperService.is_admin = False
        if ne(service_desctiption):
            A.SRV_A.serve(
                service_desctiption,
                self.service_call_handler,
                MobileHelperService.service_starts_handler,
                as_standalone=as_standalone,
                isolate=ISOLATED,
            )
            return True
        return False

    def create_mobile_helper(
        self,
        sender: str,
        external_flags: int | None = None,
        recipient: str | None = None,
    ) -> Api:
        is_cli: bool = sender_is_cli(sender)
        if is_cli:
            external_flags = BM.add(external_flags, Flags.CLI)
        stdin: Stdin = Stdin()
        session: MobileSession = MobileSession(sender, external_flags)
        output: MobileOutput = MobileOutput(session)
        try:
            session.say_hello(recipient)
            output.write_line(
                j(
                    (
                        (
                            j(
                                (
                                    "Добро пожаловать, ",
                                    nl(
                                        j(
                                            (
                                                output.user.get_formatted_given_name(
                                                    session.user_given_name
                                                ),
                                                "!",
                                            )
                                        )
                                    ),
                                )
                            )
                            if not BM.has(session.flags, Flags.ONLY_RESULT)
                            else None
                        ),
                        " ",
                        A.CT_V.WAIT,
                        " ",
                        i("Ожидайте..."),
                    )
                )
            )
        except NotFound as error:
            output.error(
                "К сожалению, не могу идентифицировать Вас. ИТ отдел добавит Вас после окончания процедуры идентификации."
            )
            raise error
        as_admin: bool = is_cli
        if not as_admin:
            try:
                as_admin = A.C_U.by_group(
                    A.R_U.by_telephone_number(sender).data, A.CT_AD.Groups.Admin # type: ignore
                )
            except NotFound as _:
                pass
        input: MobileInput = MobileInput(
            stdin,
            MobileUserInput(),
            MobileMarkInput(),
            output,
            session,
            [None, -1][as_admin],
        )
        api: Api = Api(PIH(input, output, session), stdin)
        if is_cli:
            api.external_flags = external_flags
        return api

    @staticmethod
    def say_good_bye(mobile_helper: Api, with_error: bool = False) -> None:
        mobile_helper.say_good_bye(with_error=with_error)
        mobile_helper.show_good_bye = False

    def pih_handler(
        self,
        sender: str,
        line: str | None = None,
        sender_user: User | None = None,
        external_flags: int | None = None,
        chat_id: str | None = None,
        return_result_key: str | None = None,
        args: tuple[Any] | None = None,
    ) -> None:
        mobile_helper: Api | None = None
        is_cli: bool = sender_is_cli(sender)
        while True:
            try:
                if MobileHelperService.is_client_new(sender):
                    A.IW.remove(A.CT_P.NAMES.PERSON_PIN, sender)
                    if is_cli or Api.check_for_starts_with_pih_keyword(line):
                        self.allow_send_to_next_service_in_chain[sender] = (
                            self.is_client_stack_full()
                        )
                        if not self.allow_send_to_next_service_in_chain[sender]:
                            MobileHelperService.mobile_helper_client_map[sender] = (
                                self.create_mobile_helper(
                                    sender, external_flags, chat_id
                                )
                            )
                    else:
                        self.allow_send_to_next_service_in_chain[sender] = False
                else:
                    self.allow_send_to_next_service_in_chain[sender] = False
                if sender in MobileHelperService.mobile_helper_client_map:
                    mobile_helper = MobileHelperService.mobile_helper_client_map[sender]
                    if is_cli and not mobile_helper.wait_for_input():
                        if not Api.check_for_starts_with_pih_keyword(line):
                            line = js((self.root, line))
                    try:
                        if mobile_helper.do_pih(
                            line, sender_user, external_flags, return_result_key, args # type: ignore
                        ):
                            if mobile_helper.show_good_bye:
                                if not mobile_helper.is_only_result:
                                    MobileHelperService.say_good_bye(mobile_helper)
                    except BaseException as error:
                        is_error: bool = not isinstance(error, InternalInterrupt)
                        if not mobile_helper.is_only_result and is_error:
                            MobileHelperService.say_good_bye(mobile_helper, with_error = is_error)
                        raise error
                break
            except NotFound:
                break
            except InternalInterrupt as interruption:
                if interruption.type == InterruptionTypes.NEW_COMMAND:
                    line = mobile_helper.line
                    if not Api.check_for_starts_with_pih_keyword(line):
                        MobileHelperService.say_good_bye(mobile_helper)
                        break
                elif interruption.type in (
                    InterruptionTypes.TIMEOUT,
                    InterruptionTypes.EXIT,
                ):
                    MobileHelperService.say_good_bye(mobile_helper)
                    break

    def is_client_stack_full(self) -> bool:
        max_client_count: int | None = self.max_client_count
        if n(max_client_count):
            max_client_count = MobileHelperService.count()
        return len(MobileHelperService.mobile_helper_client_map) == max_client_count

    @staticmethod
    def is_client_new(value: str) -> bool:
        return value not in MobileHelperService.mobile_helper_client_map

    def receive_message_handler(
        self,
        message_text: str,
        sender: str,
        external_flags: int | None = None,
        chat_id: str | None = None,
        return_result_key: str | None = None,
        args: tuple[Any] | None = None,
    ) -> None:
        interruption: AddressedInterruption | None = None
        while True:
            try:
                if e(interruption):
                    self.pih_handler(
                        sender,
                        message_text,
                        None,
                        external_flags,
                        chat_id,
                        return_result_key,
                        args,
                    )
                else:
                    for recipient_user in interruption.recipient_user_list():
                        recipient_user: User = recipient_user
                        self.pih_handler(
                            recipient_user.telephoneNumber,
                            js((self.root, interruption.command_name)),
                            interruption.sender_user,
                            interruption.flags,
                        )
                    interruption = None
                break
            except AddressedInterruption as local_interruption:
                interruption = local_interruption

    def receive_message_handler_thread_handler(self, message: WhatsAppMessage) -> None:
        self.receive_message_handler(
            message.message,
            message.sender,
            message.flags,
            message.chatId,
            message.return_result_key,
            message.args,
        )

    def service_call_handler(
        self,
        sc: SC,
        parameter_list: ParameterList,
        subscribtion_result: SubscribtionResult | None,
    ) -> Any:
        if sc == A.CT_SC.send_event:
            if nn(subscribtion_result) and subscribtion_result.result:
                if subscribtion_result.type == A.CT_SubT.ON_RESULT_SEQUENTIALLY:
                    message: WhatsAppMessage | None = A.D_Ex_E.whatsapp_message(
                        parameter_list
                    )

                    if nn(message):
                        if (
                            A.D.get_by_value(A.CT_ME_WH_W.Profiles, message.profile_id)
                            == A.CT_ME_WH_W.Profiles.IT
                        ):
                            allow_for_group: bool = ne(
                                message.chatId
                            ) and sender_is_cli(message.chatId)
                            if n(message.chatId) or allow_for_group:
                                telephone_number: str = if_else(
                                    allow_for_group, message.chatId, message.sender
                                )
                                if allow_for_group:
                                    message.chatId = message.sender
                                    message.sender = telephone_number
                                if n(self.checker) or self.checker(telephone_number):
                                    if self.is_client_stack_full():
                                        return True
                                    else:
                                        if (
                                            telephone_number
                                            in self.allow_send_to_next_service_in_chain
                                        ):
                                            del self.allow_send_to_next_service_in_chain[
                                                telephone_number
                                            ]
                                        PIHThread(
                                            self.receive_message_handler_thread_handler,
                                            args=[message], name="receive_message_handler_thread_handler"
                                        )
                                        while (
                                            telephone_number
                                            not in self.allow_send_to_next_service_in_chain
                                        ):
                                            pass
                                        return self.allow_send_to_next_service_in_chain[
                                            telephone_number
                                        ]
                                else:
                                    if (
                                        telephone_number
                                        in MobileHelperService.mobile_helper_client_map
                                    ):
                                        del MobileHelperService.mobile_helper_client_map[
                                            telephone_number
                                        ]
                                    return True
            return False
        return None

    @staticmethod
    def service_starts_handler() -> None:
        A.O.write_line(nl())
        A.O.blue("Configuration:")
        as_admin: bool = MobileHelperService.as_admin()
        with A.O.make_indent(1):
            A.O.value("As admin", str(as_admin))
            if not as_admin:
                A.O.value("Count", str(MobileHelperService.count()))
        A.SRV_A.subscribe_on(
            A.CT_SC.send_event,
            A.CT_SubT.ON_RESULT_SEQUENTIALLY,
            SD.name,
        )
        profile = A.CT_ME_WH_W.Profiles
        if as_admin:
            space: str = "     "

            A.ME_WH_W_Q.add_message(
                Message(
                    j(
                        (
                            " ",
                            A.CT_V.ROBOT,
                            " ",
                            nl(b("Pih cli запущен...")),
                            nl(js((space, b("Сервер:"), A.SYS.host()))),
                            js((space, b("Версия:"), VERSION_STRING)),
                            nl(),
                            space,
                            LINE,
                            nl(),
                            get_wappi_status(space, profile.IT),
                            nl() * 2,
                            get_wappi_status(space, profile.CALL_CENTRE),
                            nl() * 2,
                            get_wappi_status(space, profile.MARKETER),
                        )
                    ),
                    A.D.get(A.CT_ME_WH.GROUP.PIH_CLI),
                    A.D.get(profile.IT)
                )
            )

        for item in one(A.R_F.find("@mobile_helper_import_module_list")).text.splitlines():  # type: ignore
            A.R_F.execute(item)
