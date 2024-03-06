import math

# Definition of variables needed for calculation that may vary
jahr = 365.25  # Average number of days in a year (365) or leap year (366)
tarifwoche = 40  # Tariff contractual working hours per week in hours
feiertage = 13  # Number of legal holidays in Mecklenburg-Vorpommern
urlaubsanspruch_werktage = 26  # Tariff holiday entitlement in working days
rundungs_intervall = (
    5  # rounding of target shift length to nearest time unit in minutes
)

# Calculate actual length of vacation in whole days in regular work schedule 5/2
urlaubstage_normal = urlaubsanspruch_werktage + (urlaubsanspruch_werktage // 5 * 2)


# Function to calculate actual length of vacation in whole days in the Rufbus work schedule 3/1 plus 6/3
def berechne_urlaubstage_rufbusfahrer(urlaubsanspruch):
    global zyklus_laenge
    global werktage_pro_zyklus
    werktage_pro_zyklus = [3, 6]  # Workdays within a cycle
    frei_pro_zyklus = [1, 3]  # Days off within a cycle
    zyklus_laenge = sum(werktage_pro_zyklus) + sum(
        frei_pro_zyklus
    )  # Total cycle length

    anzahl_zyklen = urlaubsanspruch // sum(werktage_pro_zyklus)
    uebrige_werktage = urlaubsanspruch % sum(werktage_pro_zyklus)
    zusaetzliche_freie_tage = min(uebrige_werktage, frei_pro_zyklus[0])

    return anzahl_zyklen * zyklus_laenge + uebrige_werktage + zusaetzliche_freie_tage


urlaubstage_rufbusfahrer = berechne_urlaubstage_rufbusfahrer(urlaubsanspruch_werktage)


# Function to calculate normal working hours per year minus holidays and vacation in traditional work schedule
def berechne_sollarbeitszeit_normal():
    return (jahr - feiertage - urlaubstage_normal) / 7 * tarifwoche


sollarbeitszeit_normal = berechne_sollarbeitszeit_normal()


# Function to calculate the target shift length of Rufbus drivers in the Rufbus work schedule 3/1 plus 6/3
def berechne_sollschichtlaenge_rufbusfahrer():
    global werktage_im_restjahr
    restjahr = jahr - feiertage - urlaubstage_rufbusfahrer
    zyklen = restjahr / zyklus_laenge
    werktage = sum(werktage_pro_zyklus)
    werktage_im_restjahr = werktage * zyklen
    return sollarbeitszeit_normal / (zyklen * werktage)


sollschichtlaenge_rufbusfahrer = berechne_sollschichtlaenge_rufbusfahrer()


# Function to convert decimal time to hours, minutes, and seconds
def decimal_time_to_hms(decimal_time):
    total_seconds = int(decimal_time * 3600)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return hours, minutes, seconds


hours, minutes, seconds = decimal_time_to_hms(sollschichtlaenge_rufbusfahrer)

print(
    f"""
    Die Sollschichtlänge von Rufbusfahrern beträgt {hours} Stunden, {minutes} Minuten und {seconds} Sekunden pro Werktag. Die Berechnung erfolgte aufgrund einer tariflichen {tarifwoche}-Stunden-Woche in einem Jahr mit {jahr} Tagen, {feiertage} gesetzlichen Feiertagen in Mecklenburg-Vorpommern und einem Urlaubsanspruch von {urlaubsanspruch_werktage} Werktagen."""
)


# Function to round decimal time to nearest interval
def round_to_nearest_interval(decimal_time):
    # Convert decimal time to minutes
    total_minutes = decimal_time * 60

    # Round minutes to the nearest multiple (defined variable name is rundungs_intervall)
    rounded_minutes = round(total_minutes / rundungs_intervall) * rundungs_intervall

    # Convert rounded minutes back to hours and minutes
    rounded_hours = math.floor(rounded_minutes / 60)
    rounded_minutes = rounded_minutes % 60

    return rounded_hours + rounded_minutes / 60


rounded_shift = decimal_time_to_hms(
    round_to_nearest_interval(sollschichtlaenge_rufbusfahrer)
)

print(
    f"""
    Die empfohlene Schichtlänge beträgt {rounded_shift[0]} Stunden und {rounded_shift[1]} Minuten, zuzüglich unbezahlter Pausen, wobei ein Rundungsintervall zu den am nächsten gelegenen {rundungs_intervall} Minuten angewendet wurde."""
)


# Function to calculate length of single adjustment for precision timing
def berechne_ausgleichszeit():
    rounded_time = round_to_nearest_interval(sollschichtlaenge_rufbusfahrer)
    difference = (rounded_time - sollschichtlaenge_rufbusfahrer) * werktage_im_restjahr
    return difference


ausgleichszeit_decimal = berechne_ausgleichszeit()
ausgleich_stunden, ausgleich_minuten, ausgleich_sekunden = decimal_time_to_hms(
    ausgleichszeit_decimal
)


print(
    f"""
    Um die tägliche Abweichung der Sollschichtlänge um wenige Minuten und Sekunden nach der Auf- oder Abrundung zum nahegelegensten Rundungsintervall auszugleichen, wird eine einmalige Ausgleichszeit von {ausgleich_stunden} Stunden und {ausgleich_minuten} Minuten pro Kalenderjahr benötigt. Sofern dies eine positive Zahl ist, wird Freizeit gewährt, sofern die Zahl negativ ist und keine Überstunden zum Ausgleich vorliegen, wird nachgearbeitet."""
)
