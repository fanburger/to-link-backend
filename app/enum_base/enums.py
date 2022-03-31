from enum import Enum, unique


@unique
class UserLanguage(Enum):
    zh_CN = 'zh_CN'
    en = 'en'


@unique
class UserSex(Enum):
    man = 1
    woman = 0


@unique
class UserPurview(Enum):
    publish = 0
    receive = 1
    manage = 2
