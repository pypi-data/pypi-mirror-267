from .client import Client, AsyncNetwork
import csv
from itertools import count


PASS_VARIANT = 'pass', 'secret'
IP_VARIANT = 'ip', 'addr'
NAME_VARIANT = 'пу', 'имя'
PORT_VARIANT = 'port',
MECHANISM_ID = 'm_id', 'mechanism_id'
SAP = "sap",
DA = "da",


class IpAddress:
    __value: list[int]

    def __init__(self, value: str = '127.0.0.1'):
        self.__value = list()
        for el1 in value.split('.'):
            if el1.isdigit():
                el = int(el1)
                if 0 <= el <= 255:
                    self.__value.append(el)
                else:
                    raise ValueError(F'Wrong digit in value: {el}, must be 0..255')
            else:
                raise ValueError(F'Value is not digit: {el1}')
        if len(self.__value) != 4:
            raise ValueError(F'Length of Ip address {value} must be 4, got {len(self.__value)}')

    @classmethod
    def is_valid(cls, value: str) -> bool:
        try:
            cls(value)
            return True
        except ValueError:
            return False

    def __str__(self):
        return '.'.join(map(str, self.__value))


def get_client_from_csv(file_name: str) -> list[Client]:
    with open(file_name, 'r') as csv_file:
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(csv_file.read(1024))
        csv_file.seek(0)
        reader = csv.reader(csv_file, dialect=dialect)
        first_row: list[str] = next(reader)
        if any(map(IpAddress.is_valid, first_row)):  # search ip_address in first row
            # header is absence
            raise ValueError('Не найден заголовок таблицы')
        else:  # header is exist
            # search column by name
            column_name_count = count()
            field_names: list[str] = list()
            for index, cell in enumerate(first_row):
                if any(map(cell.lower().startswith, PASS_VARIANT)):
                    field_names.append('secret')
                elif any(map(cell.lower().startswith, IP_VARIANT)):
                    field_names.append('ip')
                elif any(map(cell.lower().startswith, NAME_VARIANT)):
                    field_names.append('name')
                elif any(map(cell.lower().startswith, MECHANISM_ID)):
                    field_names.append('m_id')
                elif any(map(cell.lower().startswith, SAP)):
                    field_names.append('sap')
                elif any(map(cell.lower().startswith, DA)):
                    field_names.append('da')
                elif any(map(cell.lower().startswith, PORT_VARIANT)):
                    field_names.append('port')
                else:
                    field_names.append(F'unknown{next(column_name_count)}')
            if all(map(lambda name: name in field_names, ('ip',))):
                csv_file.seek(0)
                reader = csv.DictReader(csv_file, fieldnames=field_names, dialect=dialect)
                next(reader)
                res: list[Client] = list()
                for i in reader:
                    if IpAddress.is_valid(i['ip']):
                        res.append(c := Client(
                            media=AsyncNetwork(
                                host=i.get("ip", "127.0.0.1"),
                                port=8888),
                        ))
                        c.secret = bytes(i.get('secret', '0000000000000000'), 'utf-8')
                        if m_id := i.get('m_id'):
                            c.m_id.set(m_id)
                        if port := i.get('port'):
                            c.media.port = port
                        if sap := i.get('sap'):
                            c.SAP.set(sap)
                        if da := i.get('da'):
                            c.device_address.set(da)
                return res
