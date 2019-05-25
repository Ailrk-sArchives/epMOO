from idf_handler import EPOutputReader

"""objective functions paras"""
EER = 2.3
COP = 1.9
SUMMER_LAMBDA = 0.415
WINTER_LAMBDA = 0.253

"""economic specs"""
wall_and_roof_specs = [
    [21.3831, 30], [28.5108, 40], [35.6385, 50], [42.7662, 60],
    [49.8939, 70], [57.0216, 80], [64.1493, 90], [71.277, 100]]
C_e_wall = 30
C_e_roof = 40

window_specs = [80, 116.51, 266, 304.5, 220, 500]
C_e_win = 40
total_AC_area = 1584.33
wall_area = 1306.5
roof_area = 409.6
window_area = 304.5


def f1_energy_consumption(*args) -> float:
    # Energy consumption.
    summer_consumption: float = 0
    winter_consumption: float = 0

    with open("./temp/eplustbl.csv", "r") as f:
        data = f.readlines()
        for i, _ in enumerate(data):
            if "Utility Use Per Conditioned Floor Area" in data[i]:
                for line in data[i:]:
                    if "HVAC" in line:
                        s = line.split(",")
                        winter_consumption = float(s[5])
                        summer_consumption = float(s[6])
        energy_consumption = winter_consumption / EER + summer_consumption / EER

    return energy_consumption


def f2_aPMV(*args) -> float:
    # get aPMV
    with EPOutputReader("./temp/eplusout.csv") as ep_table:
        pmv_list = ep_table.read_column("BEDROOM2.2:Zone Thermal Comfort Fanger Model PMV [](Hourly) ")
        pmv_list = list(map(lambda x: float(x), pmv_list))
        pmv_list_summer = list(filter(lambda x: x >= 0, pmv_list))
        pmv_list_winter = list(filter(lambda x: x < 0, pmv_list))

        apmv_list = list(map(lambda x: abs(x / 1 + SUMMER_LAMBDA * x), pmv_list_summer))
        apmv_list.extend(list(map(lambda x: abs(x / 1 - WINTER_LAMBDA * x), pmv_list_winter)))

        apmv_avg = sum(apmv_list) / len(apmv_list)
        return apmv_avg


def f3_economy(*args) -> float:
    wall_id = int(args[0])
    roof_id = int(args[1])
    win_id = int(args[2])

    C_i_wall = wall_and_roof_specs[wall_id][0]
    C_i_roof = wall_and_roof_specs[roof_id][0]
    C_i_win = window_specs[win_id]
    delta_wall = wall_and_roof_specs[wall_id][1]
    delta_roof = wall_and_roof_specs[roof_id][1]

    divident = (C_i_wall * delta_wall + C_e_wall) * wall_area + \
               (C_i_win + C_e_win) * window_area + \
               (C_i_roof * delta_roof + C_e_roof) * roof_area
    price = divident / total_AC_area

    return price
