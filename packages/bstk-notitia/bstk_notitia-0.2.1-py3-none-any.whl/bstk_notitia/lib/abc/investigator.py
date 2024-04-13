from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import typing


if typing.TYPE_CHECKING:
    from lib.abc.driver import DriverABC
    from lib.abc.observer import ObserverABC
    from lib.abc.informant import InformantABC
    from lib.abc.reporter import ReporterABC


"""
Investigators specialise in working with a singular input,
collecting more information if required, deciding what to do
with that information, and then acting on that decision.

A good investigator has a narrow focus and works to quickly
close their case. They are a specialist at one particular task
and should not take more than a few seconds to come to a
conclusion (I/O not withstanding)

Complicated investigations lead to mistakes, so its usually
a good idea to have multiple investigators who specialise in
working with a discrete set of information and either create
new cases for other investigators, or reporting on their
case and closing it.

Abstracts aside, investigators:
  - hold the business logic
  - configure observers, informants and reporters
  - never change information directly
  - ensure each case is isolated from others
"""

NOTITIA_DEPENDENCIES: typing.Dict


@dataclass
class InvestigatorABC(ABC):
    name: typing.AnyStr = field(init=False)
    key: typing.AnyStr = field(init=False)
    type: typing.AnyStr = field(init=False, default="investigator")

    driver: typing.Dict[str, DriverABC] = field(init=True, kw_only=True, default=None)
    observer: typing.Dict[str, ObserverABC] = field(init=False, default=None)
    informant: typing.Dict[str, InformantABC] = field(init=False, default=None)
    reporter: typing.Dict[str, ReporterABC] = field(init=False, default=None)

    def sign_on(
        self,
        driver: typing.Optional[typing.Dict[str, DriverABC]] = None,
        observer: typing.Optional[typing.Dict[str, ObserverABC]] = None,
        informant: typing.Optional[typing.Dict[str, InformantABC]] = None,
        reporter: typing.Optional[typing.Dict[str, ReporterABC]] = None,
    ) -> typing.Dict:
        if driver:
            self.driver = driver
        if observer:
            self.observer = observer
        if informant:
            self.informant = informant
        if reporter:
            self.reporter = reporter

    @abstractmethod
    async def start(self, **kwargs):
        """
        'start' working... that could mean waiting for information from
        an observer, immediately reaching out to an informant, directly
        providing information to a report, or reach for a snack and wait..

        Investigators do whatever they do - we don't ask, they don't tell.
        """
        pass
