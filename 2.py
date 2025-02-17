import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def extract_domain_and_value(line):
    """Извлекает домен и значение из строки."""
    parts = line.split()
    if len(parts) >= 2:
        return normalize_domain(parts[0]), float(parts[1]) # Нормализуем домен
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

ChatGPT4 | Midjourney, [16.02.2025 4:13]
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

# Список известных доменов
known_domains = ['ya.ru', 'yandex.ru', 'avito.ru', 'ozon.ru', 'wildberries.ru', 'dzen.ru',
                 'sberbank.ru', 'gosuslugi.ru', 'ria.ru', 'lenta.ru', 'gazeta.ru', 'kp.ru',
                 'rbc.ru', 'pikabu.ru', 'rambler.ru', 'kinopoisk.ru', 'sports.ru', 'auto.ru',
                 'cian.ru', 'irr.ru', 'hh.ru', 'domclick.ru', 'youla.ru', 'tinkoff.ru', 'vtb.ru',
                 'pochtabank.ru', 'gazprombank.ru', 'tele2.ru', 'megafon.ru', 'mts.ru',
                 'beeline.ru', 'rostelecom.ru', 'skbbank.ru', 'raiffeisen.ru', 'alfabank.ru',
                 'rosneft.ru', 'lukoil.ru', 'magnit.ru', 'x5.ru', 'auchan.ru', 'leroymerlin.ru',
                 'castorama.ru', 'dns-shop.ru', 'mvideo.ru', 'eldorado.ru', 'citilink.ru',
                 'regard.ru', 'ulmart.ru', 'yulsun.ru', 'kommersant.ru']

# Извлекаем данные и фильтруем только известные домены
domain_values = []
for line in data.strip().split('\n'):
    domain, value = extract_domain_and_value(line)
    if domain and domain in known_domains:  # Фильтруем
        domain_values.append((domain, value))

# Отделяем домены и значения
domains = [item[0] for item in domain_values]
values = [item[1] for item in domain_values]
domain_lengths = [len(domain) for domain in domains]

# Вычисляем коэффициент корреляции Пирсона
correlation, p_value = pearsonr(domain_lengths, values)

print(f"Коэффициент корреляции Пирсона между длиной домена и степенью подделываемости: {correlation}")
print(f"P-значение: {p_value}")

# Диаграмма рассеяния
plt.scatter(domain_lengths, values)
plt.xlabel("Длина домена")
plt.ylabel("Степень подделываемости")
plt.title("Корреляция между длиной домена и степенью подделываемости")
plt.show()