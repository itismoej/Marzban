from abc import ABC, abstractproperty
from uuid import UUID

from pydantic import BaseModel

from ..proto.common.serial.typed_message_pb2 import TypedMessage
from ..proto.proxy.shadowsocks.config_pb2 import \
    Account as ShadowsocksAccountPb2
from ..proto.proxy.shadowsocks.config_pb2 import \
    CipherType as ShadowsocksCipherType
from ..proto.proxy.trojan.config_pb2 import Account as TrojanAccountPb2
from ..proto.proxy.vless.account_pb2 import Account as VLESSAccountPb2
from ..proto.proxy.vmess.account_pb2 import Account as VMessAccountPb2
from .message import Message


class Account(BaseModel, ABC):
    email: str
    level: int = 0

    @abstractproperty
    def message(self) -> TypedMessage:
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.email}>"


class VMessAccount(Account):
    id: UUID

    @property
    def message(self):
        return Message(VMessAccountPb2(id=str(self.id), alter_id=0))


class VLESSAccount(Account):
    id: UUID
    flow: str = ""

    @property
    def message(self):
        return Message(VLESSAccountPb2(id=str(self.id), flow=self.flow))


class TrojanAccount(Account):
    password: str

    @property
    def message(self):
        return Message(TrojanAccountPb2(password=self.password))


class ShadowsocksAccount(Account):
    password: str
    cipher_type: str = "CHACHA20_POLY1305"

    @property
    def message(self):
        return Message(ShadowsocksAccountPb2(password=self.password, cipher_type=self.cipher_type))