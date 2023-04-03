

from src.commons.process_number import cal_eccentricity
from src.display_properties.properties import Properties

def get_sub_posi_list_at_given_e(eccentricty, display_posis):
    """
    :param eccentricty: in pixel
    :param posilist:  display position
    :return: the sub-display positions (within the given eccentricity)
    """
    sub_displays = list()
    sub_numerosity = 0
    for posi in display_posis:
        if cal_eccentricity((eccentricty, 0)) >= cal_eccentricity(posi):
            sub_numerosity += 1
            sub_displays.append(posi)
    if len(sub_displays) <= 3:
        return sub_numerosity, []
    else:
        return sub_numerosity, sub_displays


def get_local_density_at_given_e(eccentricity, display_posis):
    sub_numerosity, sub_display = get_sub_posi_list_at_given_e(eccentricity, display_posis)
    if len(sub_display) == 0:
        return sub_numerosity, 0
    else:
        return sub_numerosity, Properties(sub_display).density_reduced


def get_local_density_for_single_display(display_posis):
    # get max eccentricty
    eccentricities = [cal_eccentricity(posi) for posi in display_posis]
    max_e = int(max(eccentricities))
    local_density_list, sub_numerosity = [], 0
    for e in range(int(max_e) + 2):
        # 对每个e都计算当前的numerosity和local density
        new_sub_numerosity, local_density = get_local_density_at_given_e(e, display_posis)
        # 判断得到的numerosity是不是和以前一样，不一样的话更新
        if sub_numerosity != new_sub_numerosity:
            sub_numerosity = new_sub_numerosity
            local_density_list.append((e, local_density))
    # print(local_density_list)
    return local_density_list

