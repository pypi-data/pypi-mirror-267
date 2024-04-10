import ipih

from pih import A, serve, subscribe_on
from PolibasePersonNotificationAnswerService.const import SD

SC = A.CT_SC

ISOLATED: bool = False


def start(as_standalone: bool = False) -> None:

    from pih.collections import (
        Message,
        PolibasePerson,
        WhatsAppMessage,
        PolibasePersonVisitDS as PPVDS,
        PolibasePersonNotificationConfirmation as PPNC,
    )
    from pih.tools import (
        ParameterList,
        ne,
        nn,
        one,
        nns,
        nni,
    )

    SENDER: str = A.D.get(A.CT_ME_WH_W.Profiles.CALL_CENTRE)

    def server_call_handler(sc: SC, pl: ParameterList) -> bool | None:
        if sc == SC.send_event:
            event: A.CT_E = A.D_Ex_E.get(pl)
            if event == A.CT_E.WHATSAPP_MESSAGE_RECEIVED:
                message: WhatsAppMessage | None = A.D_Ex_E.whatsapp_message(pl)
                if ne(message):
                    sender: str = message.profile_id
                    if sender == SENDER:
                        telephone_number: str = A.D_F.telephone_number_international(
                            message.sender
                        )
                        notification_confirmation: PPNC | None = A.R_P_N_C.by(
                            telephone_number, sender
                        ).data
                        if (
                            ne(notification_confirmation)
                            and notification_confirmation.status == 2
                        ):
                            visit: PPVDS | None = one(
                                A.R_P_V_DS.search(
                                    PPVDS(
                                        telephoneNumber=A.D_F.telephone_number(
                                            telephone_number
                                        )
                                    )
                                )
                            )
                            if nn(visit):
                                person: PolibasePerson = A.D_P.person_by_pin(
                                    nni(visit.pin)
                                )
                                full_name: str | None = person.FullName
                                if A.A_P_N_C.update(telephone_number, sender, 1):
                                    A.ME_WH_W_Q.add_message(
                                        Message(
                                            A.S_P_V.offer_telegram_bot_url_text(
                                                full_name
                                            ),
                                            telephone_number,
                                            sender,
                                        )
                                    )
                                    A.ME_WH_W_Q.add_message(
                                        Message(
                                            A.CT_P.TELEGRAM_BOT_URL,
                                            telephone_number,
                                            sender,
                                        )
                                    )
                                    A.E.polibase_person_answered(
                                        person, nns(message.message)
                                    )
        return None

    def service_starts_handler() -> None:
        subscribe_on(SC.send_event)

    serve(
        SD,
        server_call_handler,
        service_starts_handler,
        isolate=ISOLATED,
        as_standalone=as_standalone,
    )


if __name__ == "__main__":
    start()
