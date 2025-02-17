
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, ttest_ind

def extract_domain_and_value(line):
    """Извлекает домен и значение из строки, проверяя допустимость значения."""
    parts = line.split()
    if len(parts) >= 2:
        try:
            value = float(parts[1])  # Попытка преобразования в float
            return normalize_domain(parts[0]), value
        except ValueError:
            print(f"Предупреждение: Не удалось преобразовать '{parts[1]}' в число в строке: {line}")
            return None, None  # Возвращаем None, если преобразование не удалось
    else:
        return None, None

def normalize_domain(domain):
    """Очищает и нормализует доменное имя."""
    domain = re.sub(r'^(https?://)?(www\.)?', '', domain)
    domain = domain.rstrip('/')
    return domain.lower()

# Домены
data = """
ya.ru  0.03276999094097155  iz.ru  0.02835137201556248
yandex.ru  0.03969879804968694  aif.ru  0.059969427283372914
avito.ru  0.0660557739744033  rg.ru  0.03557246131000532
ozon.ru  0.06798139778625473  tass.ru  0.0852088536744255
wildberries.ru  0.014923584541848533  interfax.ru  0.025669253134769424
dzen.ru  0.05075394189808395  ng.ru  0.03234016419725471
sberbank.ru  0.02695873336591993  vedomosti.ru  0.0028024703690337684
gosuslugi.ru  0.014665688495618431  fontanka.ru  0.01315269835773517
ria.ru  0.07934601689012785  avinf.ru  0.029795589874451047
lenta.ru  0.0767326702883295  autostat.ru  0.035744392007492055
gazeta.ru  0.030930332477863497  drom.ru  0.07748916535727113
kp.ru  0.03846089702778246  biblio-globus.ru  0.0004126336739681622
rbc.ru  0.059264511423677294  labirint.ru  0.017193069748673427
pikabu.ru  0.008699693292828754  chitai-gorod.ru  0.0018224653933593834
rambler.ru  0.040180204002649794  bookvoed.ru  0.006395821946506514
kinopoisk.ru  0.009318643803780996  sport-express.ru  0.012361817149296192
sports.ru  0.07429125438401787  sovsport.ru  0.039114233678232045
auto.ru  0.14256493435600004  mail.yandex.ru  0.002819663438782442
cian.ru  0.06746560569379452  auto.drom.ru  0.00557055459857019
irr.ru  0.05505220933525231  74.ru  0.015319025146068022
hh.ru  0.014837619193105167  e1.ru  0.01234462407954752
domclick.ru  0.01586920337802557  top100.ru  0.007135123945699472
youla.ru  0.026872768017176567  a-a.ru  0.06382067490707576
tinkoff.ru  0.028127862108829726  s7.ru  0.01504393603008925
vtb.ru  0.04760761013407672  aeroflot.ru  0.015473762773806084
pochtabank.ru  0.002682118880793054  letsply.ru  0.013960772635922823
gazprombank.ru  0.0055017823195754965  stilzhizni.ru  0.0011003564639150993
tele2.ru  0.033990698893127363  ria.ru  0.07934601689012785
megafon.ru  0.053470446918374354  exler.ru  0.02960646610721564
mts.ru  0.08517446753492815  vedomosti.ru  0.0028024703690337684
beeline.ru  0.08899132901913366  gazeta.ru  0.030930332477863497
rostelecom.ru  0.024328193694372897  izvestia.ru  0.014115510263660883
skbbank.ru  0.04470198134655091  utro.ru  0.06101820453804199
raiffeisen.ru  0.001014391115171732  dni.ru  0.057218536123585156
alfabank.ru  0.023829594671661368  newizv.ru  0.006017574412035699
rosneft.ru  0.04024897628164449  rosbalt.ru  0.04207144167500387
lukoil.ru  0.011553742871108542  mk.ru  0.047641996273574065
magnit.ru  0.034403332567095525  bloknot.ru  0.023227837230457796
x5.ru  0.005381430831334783  life.ru  0.07895057628590837
auchan.ru  0.027388560109636768  pravda.ru  0.031188228524093593
leroymerlin.ru  0.0020459753000921376  nevnov.ru  0.02092396588413556
castorama.ru  0.005278272412842741  pnp.ru  0.05367676375535843
dns-shop.ru  0.06074311542206321  kp.ru  0.03846089702778246
mvideo.ru  0.030191030478670534  
eldorado.ru  0.006636524922987943  
citilink.ru  0.01777763412012832  
regard.ru  0.039165812887478064  
ulmart.ru  0.051579209246020274  
yulsun.ru  0.006258277388517127  
kommersant.ru  0.0021663267883328514
"""

# Классификация доменов по типу организации (ОБНОВЛЕНО)
domain_type = {
    'yandex.ru': 'поисковик/сервисы',
    'ya.ru': 'поисковик/сервисы',
    'sberbank.ru': 'банк',
    'ozon.ru': 'e-commerce',
    'gosuslugi.ru': 'государственный орган',
    'avito.ru': 'доска объявлений',
    'wildberries.ru': 'e-commerce',
    'dzen.ru': 'контент-платформа',
    'lenta.ru': 'новостной сайт',
    'ria.ru': 'новостной сайт',
    'gazeta.ru': 'новостной сайт',
    'kp.ru': 'новостной сайт',
    'rbc.ru': 'деловые новости',
    'rambler.ru': 'портал',
    'kinopoisk.ru': 'фильмы/развлечения',
    'sports.ru': 'спорт',
    'auto.ru': 'авто',
    'cian.ru': 'недвижимость',
    'tinkoff.ru': 'банк',
    'mts.ru': 'оператор связи',
    'megafon.ru': 'оператор связи',
    'beeline.ru': 'оператор связи',
    'vtb.ru': 'банк',
    'youla.ru': 'доска объявлений',
    'rostelecom.ru': 'оператор связи',
    'hh.ru': 'поиск работы',
    'magnit.ru': 'розничная торговля',
    'tele2.ru': 'оператор связи',
    'domclick.ru': 'недвижимость/финансы', # Сервис от Сбербанка
    'rosneft.ru': 'нефтегазовая промышленность',
    'lukoil.ru': 'нефтегазовая промышленность',
    'alfabank.ru': 'банк',
    'irr.ru': 'доска объявлений',
    'auchan.ru': 'розничная торговля',
    'x5.ru': 'розничная торговля', # "Пятерочка", "Перекресток"
    'pochtabank.ru': 'банк',
    'skbbank.ru': 'банк',
    'raiffeisen.ru': 'банк',
    'leroymerlin.ru': 'товары для дома/строительство',
    'dns-shop.ru': 'розничная торговля электроникой',
    'mvideo.ru': 'розничная торговля электроникой',
    'eldorado.ru': 'розничная торговля электроникой',
    'citilink.ru': 'розничная торговля электроникой',
    'pikabu.ru': 'развлечения',
    'kommersant.ru': 'деловые новости',
    'regard.ru': 'розничная торговля электроникой',
    'ulmart.ru': 'розничная торговля электроникой', 
    'yulsun.ru': 'другое'
}

# Извлекаем данные и фильтруем только известные домены
domain_values = []
for line in data.strip().split('\n'):
    domain, value = extract_domain_and_value(line)
    if domain and domain in domain_type and value is not None:  # Фильтруем
        domain_values.append((domain, value, domain_type[domain])) # Добавляем тип

# Группируем по типу организации и вычисляем среднюю степень подделываемости
type_values = {}
for domain, value, domain_type in domain_values:
    if domain_type not in type_values:
        type_values[domain_type] = []
    type_values[domain_type].append(value)

# Вычисляем средние значения для каждого типа
type_means = {}
for domain_type, values in type_values.items():
    type_means[domain_type] = np.mean(values)

# Выводим результаты
print("Средняя степень подделываемости по типу организации:")
for domain_type, mean_value in sorted(type_means.items(), key=lambda item: item[1], reverse=True): # Сортируем
    print(f"{domain_type}: {mean_value}")

# Визуализация (столбчатая диаграмма)
types = list(type_means.keys())
means = list(type_means.values())

plt.bar(types, means)
plt.xlabel("Тип организации")
plt.ylabel("Средняя степень подделываемости")
plt.title("Средняя степень подделываемости по типу организации")
plt.xticks(rotation=45, ha="right")  # Поворачиваем подписи для читаемости
plt.tight_layout() #  Предотвращает обрезание подписей
plt.show()
