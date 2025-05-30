# -*- coding: utf-8 -*-
from sys import exit
from libfptr10 import IFptr
from datetime import datetime

print('Сканирую ККТ Атол...')

fptr = IFptr("fptr10.dll")

print('Версия драйвера:', fptr.version())

# пробуем USB подключение
fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_MODEL, str(IFptr.LIBFPTR_MODEL_ATOL_22F))
fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_PORT, str(IFptr.LIBFPTR_PORT_USB))
fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_OFD_CHANNEL, str(IFptr.LIBFPTR_OFD_CHANNEL_PROTO))
fptr.applySingleSettings()
fptr.open()
channelKKT = 'USB'

if fptr.isOpened() == 1:
    print('ФР Атол найден на USB')
else:
    print('ФР Атол не найден на USB. Ищу по COM портам...')
    found = False
    for port_number in range(1, 7):
        # если USB не доступен переберем COM порты
        fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_PORT, str(IFptr.LIBFPTR_PORT_COM))
        fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_COM_FILE, f'COM{port_number}')
        fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_BAUDRATE, str(IFptr.LIBFPTR_PORT_BR_115200))
        fptr.applySingleSettings()
        fptr.open()
        if fptr.isOpened() == 1:
            channelKKT = 'COM'
            print(f'ФР Атол найден на COM{port_number}')
            found = True
            break
    if not found:
        print('ФР Атол не доступен')
        exit()

fptr.setParam(IFptr.LIBFPTR_PARAM_DATA_TYPE, IFptr.LIBFPTR_DT_STATUS)
fptr.queryData()
serialNumber = fptr.getParamString(IFptr.LIBFPTR_PARAM_SERIAL_NUMBER)
modelName = fptr.getParamString(IFptr.LIBFPTR_PARAM_MODEL_NAME)
firmwareVersion = fptr.getParamString(IFptr.LIBFPTR_PARAM_UNIT_VERSION)
smena = fptr.getParamString(IFptr.LIBFPTR_PARAM_SHIFT_STATE)
lastDocument = fptr.getParamString(IFptr.LIBFPTR_PARAM_DOCUMENT_NUMBER)
dateTimeFR = fptr.getParamDateTime(IFptr.LIBFPTR_PARAM_DATE_TIME)

fptr.setParam(IFptr.LIBFPTR_PARAM_FN_DATA_TYPE, IFptr.LIBFPTR_FNDT_REG_INFO)
fptr.fnQueryData()
taxationTypes = fptr.getParamInt(1062)
organizationName = fptr.getParamString(1048)
innOrganization = fptr.getParamString(1018)
addressNalog = fptr.getParamString(1060)
ffdVersion = fptr.getParamInt(1209)
ofdVATIN = fptr.getParamString(1017)
shopAddress = fptr.getParamString(1009)
ofdName = fptr.getParamString(1046)
regNumberFN = fptr.getParamString(1037)
regMarkirovka = fptr.getParamBool(IFptr.LIBFPTR_PARAM_TRADE_MARKED_PRODUCTS)
agentSign = fptr.getParamInt(1057)  # признак агента
exciseSign = fptr.getParamBool(1207)  # признак подакцизного товара
autoModeSign = fptr.getParamBool(1001)  # Признак автоматического режима
lotterySign = fptr.getParamBool(1126)  # Признак проведения лотерей
gamblingSign = fptr.getParamBool(1193)  # Признак проведения азартных игр

fptr.setParam(IFptr.LIBFPTR_PARAM_FN_DATA_TYPE, IFptr.LIBFPTR_FNDT_FN_INFO)
fptr.fnQueryData()
fnSerial = fptr.getParamString(IFptr.LIBFPTR_PARAM_SERIAL_NUMBER)
fnExhausted = fptr.getParamBool(IFptr.LIBFPTR_PARAM_FN_RESOURCE_EXHAUSTED)
fnMemoryOverflow = fptr.getParamBool(IFptr.LIBFPTR_PARAM_FN_MEMORY_OVERFLOW)
fnCriticalError = fptr.getParamBool(IFptr.LIBFPTR_PARAM_FN_CRITICAL_ERROR)

fptr.setParam(IFptr.LIBFPTR_PARAM_FN_DATA_TYPE, IFptr.LIBFPTR_FNDT_OFD_EXCHANGE_STATUS)
fptr.fnQueryData()
exchangeStatus = fptr.getParamInt(IFptr.LIBFPTR_PARAM_OFD_EXCHANGE_STATUS)
unsentCountOFD = fptr.getParamInt(IFptr.LIBFPTR_PARAM_DOCUMENTS_COUNT)
firstUnsentNumberOFD = fptr.getParamInt(IFptr.LIBFPTR_PARAM_DOCUMENT_NUMBER)
ofdMessageRead = fptr.getParamBool(IFptr.LIBFPTR_PARAM_OFD_MESSAGE_READ)
dateTimeExchangeOFD = fptr.getParamDateTime(IFptr.LIBFPTR_PARAM_DATE_TIME)

fptr.setParam(IFptr.LIBFPTR_PARAM_DATA_TYPE, IFptr.LIBFPTR_DT_LAST_SENT_OFD_DOCUMENT_DATE_TIME)
fptr.queryData()
dateTimeLastSendOFD = fptr.getParamDateTime(IFptr.LIBFPTR_PARAM_DATE_TIME)

fptr.setParam(IFptr.LIBFPTR_PARAM_FN_DATA_TYPE, IFptr.LIBFPTR_FNDT_VALIDITY)
fptr.fnQueryData()
dateTimeFNValidaty = fptr.getParamDateTime(IFptr.LIBFPTR_PARAM_DATE_TIME)

# критические ошибки
fptr.setParam(IFptr.LIBFPTR_PARAM_FN_DATA_TYPE, IFptr.LIBFPTR_FNDT_ERRORS)
fptr.fnQueryData()
networkErrorText = fptr.getParamString(IFptr.LIBFPTR_PARAM_NETWORK_ERROR_TEXT)
ofdErrorText = fptr.getParamString(IFptr.LIBFPTR_PARAM_OFD_ERROR_TEXT)
fnErrorText = fptr.getParamString(IFptr.LIBFPTR_PARAM_FN_ERROR_TEXT)

# Статус информационного обмена с ИСМ
fptr.setParam(IFptr.LIBFPTR_PARAM_FN_DATA_TYPE, IFptr.LIBFPTR_FNDT_ISM_EXCHANGE_STATUS)
fptr.fnQueryData()
unsentCountISM = fptr.getParamInt(IFptr.LIBFPTR_PARAM_DOCUMENTS_COUNT)
firstUnsentNumberISM = fptr.getParamInt(IFptr.LIBFPTR_PARAM_DOCUMENT_NUMBER)
dateTimeExchangeISM = fptr.getParamDateTime(IFptr.LIBFPTR_PARAM_DATE_TIME)

# Ошибки обмена с ИСМ
fptr.setParam(IFptr.LIBFPTR_PARAM_FN_DATA_TYPE, IFptr.LIBFPTR_FNDT_ISM_ERRORS)
fptr.fnQueryData()
networkErrorTextISM = fptr.getParamString(IFptr.LIBFPTR_PARAM_NETWORK_ERROR_TEXT)
ismErrorText = fptr.getParamString(IFptr.LIBFPTR_PARAM_ISM_ERROR_TEXT)
fnErrorTextISM = fptr.getParamString(IFptr.LIBFPTR_PARAM_FN_ERROR_TEXT)
documentNumberErrorISM = fptr.getParamInt(IFptr.LIBFPTR_PARAM_DOCUMENT_NUMBER)
dateTimeLastSendISM = fptr.getParamDateTime(IFptr.LIBFPTR_PARAM_DATE_TIME)

# считать даные ОФД
fptr.setParam(IFptr.LIBFPTR_PARAM_SETTING_ID, 273)
fptr.readDeviceSetting()
addressOFD = fptr.getParamString(IFptr.LIBFPTR_PARAM_SETTING_VALUE)

fptr.setParam(IFptr.LIBFPTR_PARAM_SETTING_ID, 274)
fptr.readDeviceSetting()
portOFD = fptr.getParamString(IFptr.LIBFPTR_PARAM_SETTING_VALUE)

# Адрес ИСМ
fptr.setParam(IFptr.LIBFPTR_PARAM_SETTING_ID, 1000)
fptr.readDeviceSetting()
addressISM = fptr.getParamString(IFptr.LIBFPTR_PARAM_SETTING_VALUE)

# порт ИСМ
fptr.setParam(IFptr.LIBFPTR_PARAM_SETTING_ID, 1001)
fptr.readDeviceSetting()
portISM = fptr.getParamInt(IFptr.LIBFPTR_PARAM_SETTING_VALUE)

# канал обмена с ОФД
fptr.setParam(IFptr.LIBFPTR_PARAM_SETTING_ID, 276)
fptr.readDeviceSetting()
channelOFD = fptr.getParamString(IFptr.LIBFPTR_PARAM_SETTING_VALUE)

# версия загрузчика
fptr.setParam(IFptr.LIBFPTR_PARAM_DATA_TYPE, IFptr.LIBFPTR_DT_UNIT_VERSION)
fptr.setParam(IFptr.LIBFPTR_PARAM_UNIT_TYPE, IFptr.LIBFPTR_UT_BOOT)
fptr.queryData()
bootVersion = fptr.getParamString(IFptr.LIBFPTR_PARAM_UNIT_VERSION)

# преобразование статусов
if smena == '0':
    smena_str = 'Закрыта'
elif smena == '1':
    smena_str = 'Открыта'
elif smena == '2':
    smena_str = 'Истекла'
else:
    smena_str = smena

if exchangeStatus == 0:
    exchangeStatus_str = 'соединение установлено'
elif exchangeStatus == 1:
    exchangeStatus_str = 'есть сообщение для передачи в ОФД'
elif exchangeStatus == 2:
    exchangeStatus_str = 'ожидание ответного сообщения от ОФД'
elif exchangeStatus == 3:
    exchangeStatus_str = 'есть команда от ОФД'
elif exchangeStatus == 4:
    exchangeStatus_str = 'изменились настройки соединения с ОФД'
elif exchangeStatus == 5:
    exchangeStatus_str = 'ожидание ответа на команду от ОФД'
else:
    exchangeStatus_str = exchangeStatus

if channelOFD == '1':
    channelOFD_str = 'EoU'
elif channelOFD == '2':
    channelOFD_str = 'Ethernet'
elif channelOFD == '3':
    channelOFD_str = 'Wi-Fi'
elif channelOFD == '4':
    channelOFD_str = 'GSM-модем'
elif channelOFD == '5':
    channelOFD_str = 'EoT'
else:
    channelOFD_str = channelOFD


def fn_end_of_days(dateEnd: str):
    '''Расчет оставшихся дней до окончания ФН'''
    try:
        delta = dateEnd - datetime.now()
        return delta.days
    except:
        return 'Не удалось рассчитать'


# статичные данные
result_info = f'''01) Время ФР: {dateTimeFR}
02) Организация: {organizationName} ({innOrganization})
03) Модель ФР: {modelName}
04) Номер ФР: {serialNumber}
05) Номер ФН: {fnSerial}
06) Регномер ФН: {regNumberFN}
07) Дата окончания ФН: {dateTimeFNValidaty.date()}
08) Дней до окончания ФН: {fn_end_of_days(dateTimeFNValidaty)}
09) Последний документ: {lastDocument}
10) Смена: {smena_str}
11) Версия ФФД: {ffdVersion}
12) Канал обмена: {channelOFD_str}
13) Подключение: {channelKKT}
14) Налоговая: {addressNalog}
15) Прошивка: {firmwareVersion}
16) Загрузчик: {bootVersion}
17) ОФД: {addressOFD}:{portOFD}
18) ИСМ: {addressISM}:{portISM}'''

# динамичные данные
if unsentCountOFD > 0:
    details_ofd = f'''
19) Количество неотправленных в ОФД: {unsentCountOFD}
  - Статус обмена с ОФД: {exchangeStatus_str}
  - Номер первого неотправленного документа в ОФД: {firstUnsentNumberOFD}
  - Дата первого неотправленного документа в ОФД: {dateTimeExchangeOFD}
  - Последний успешный обмен с ОФД: {dateTimeLastSendOFD}
  - Ошибка сети: {networkErrorText}
  - Ошибка ОФД: {ofdErrorText}
  - Ошибка ФН: {fnErrorText}'''
else:
    details_ofd = f'''
19) Количество неотправленных в ОФД: {unsentCountOFD}'''

if unsentCountISM > 0:
    details_ism = f'''
20) Количество неотправленных в ИСМ: {unsentCountISM}
  - Номер первого неотправленного документа в ИСМ: {firstUnsentNumberISM}
  - Дата первого неотправленного документа в ИСМ: {dateTimeExchangeISM}
  - Последний успешный обмен с ИСМ: {dateTimeLastSendISM}
  - Ошибка сети: {networkErrorTextISM}
  - Ошибка ИСМ: {ismErrorText}
  - Ошибка ФН: {fnErrorTextISM}
  - Номер ФД, на котором произошла ошибка: {documentNumberErrorISM}'''
else:
    details_ism = f'''
20) Количество неотправленных в ИСМ: {unsentCountISM}'''

if regMarkirovka:
    regMarkirovka_str = 'Да'
else:
    regMarkirovka_str = 'Нет'

if exciseSign:
    exciseSign_str = 'Да'
else:
    exciseSign_str = 'Нет'

details_registration = f'''
21) Регистрационные данные:
  - Признак агента: {agentSign}
  - Признак маркировки: {regMarkirovka_str}
  - Признак подакцизного товара: {exciseSign_str}
  - Налогообложение: {taxationTypes}'''

if autoModeSign:
    details_registration += '''
  - Признак автоматического режима: Да'''
if lotterySign:
    details_registration += '''
  - Признак проведения лотерей: Да'''
if gamblingSign:
    details_registration += '''
  - Признак проведения азартных игр: Да'''

errors_fn = f'''
22) Критическая ошибка:
  - Память ФН переполнена: {fnMemoryOverflow}
  - Исчерпан ресурс ФН: {fnExhausted}
  - Критическая ошибка ФН: {fnCriticalError}'''

# вывод информации в консоль
print(result_info)
print(details_ofd)
print(details_ism)
print(details_registration)
if fnMemoryOverflow or fnExhausted or fnCriticalError:
    print(errors_fn)

# закрываем соединение
fptr.close()
input("\nНажмите Enter для выхода...")