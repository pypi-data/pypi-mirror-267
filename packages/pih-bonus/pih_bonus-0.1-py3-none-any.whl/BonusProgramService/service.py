import ipih

from pih import A, serve, subscribe_on
from BonusProgramService.const import SD

SC = A.CT_SC

ISOLATED: bool = False


def start(as_standalone: bool = False) -> None:

    from pih.collections import (
        BonusInformation,
    )
    from pih.tools import (
        ParameterList,
        js,
        nn,
        one,
    )

    SENDER: str = A.D.get(A.CT_ME_WH_W.Profiles.CALL_CENTRE)

    def server_call_handler(sc: SC, pl: ParameterList) -> bool | None:
        if sc == SC.send_event:
            event: A.CT_E = A.D_Ex_E.get(pl)
            if event == A.CT_E.POLIBASE_PERSON_BONUSES_WAS_UPDATED:
                polibase_person_pin: int = A.D_Ex_E.parameters(pl)[0]
                bonus_information: BonusInformation | None = one(
                    A.R_P.bonus_information(polibase_person_pin)
                )
                if nn(bonus_information):
                    A.L.polibase(
                        js(
                            (
                                "Для клиента:",
                                polibase_person_pin,
                                "обновлены бонусы:",
                                bonus_information.bonus_last,
                                "из",
                                bonus_information.bonus_active,
                            )
                        )
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
