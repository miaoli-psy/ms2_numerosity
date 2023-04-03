# -*- coding: utf-8 -*- 
"""
Project: CrowdingNumerosityGit
Creator: Miao
Create time: 2021-04-05 23:17
IDE: PyCharm
Introduction:
"""
from math import atan2, pi

from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse
from scipy.spatial import distance


def drawEllipse_full(e_posi, extra_posi, ka, kb, ellipseColor_r = 'orangered', ellipseColor_t = 'royalblue', extra_disc_color = 'orangered', ellipsetransp = 0.5, name_str = 1):
    """
    This function allows to draw more than one ellipse. The parameter is
    a list of coordinate (must contain at least two coordinates)
    The radial and tangential ellipses for the same coordinates are drawn.
    """
    eccentricities = []
    for i in range(len(e_posi)):
        eccentricities0 = distance.euclidean(e_posi[i], (0, 0))
        eccentricities.append(eccentricities0)
    # radial
    angle_deg = []
    for ang in range(len(e_posi)):
        angle_rad0 = atan2(e_posi[ang][1], e_posi[ang][0])
        angle_deg0 = angle_rad0 * 180 / pi
        angle_deg.append(angle_deg0)
    my_e = [Ellipse(xy = e_posi[j], width = eccentricities[j] * ka * 2, height = eccentricities[j] * kb * 2,
                    angle = angle_deg[j])
            for j in range(len(e_posi))]

    # tangential
    angle_deg2 = []
    for ang in range(len(e_posi)):
        angle_rad0_2 = atan2(e_posi[ang][1], e_posi[ang][0])
        angle_deg0_2 = angle_rad0_2 * 180 / pi + 90
        angle_deg2.append(angle_deg0_2)
    my_e2 = [Ellipse(xy = e_posi[j], width = eccentricities[j] * ka * 2, height = eccentricities[j] * kb * 2,
                     angle = angle_deg[j] + 90)
             for j in range(len(e_posi))]

    fig, ax = plt.subplots(subplot_kw = {'aspect': 'equal'}, figsize = (4, 3))
    for e in my_e:
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(ellipsetransp)
        e.set_facecolor(ellipseColor_r)
    for e2 in my_e2:
        ax.add_artist(e2)
        e2.set_clip_box(ax.bbox)
        e2.set_alpha(ellipsetransp)
        e2.set_facecolor(ellipseColor_t)

    # show the discs on the ellipses-flower
    for dot in e_posi:
        plt.plot(dot[0], dot[1], color = 'k', marker = 'o', markersize = 2)
    # plt.show()
    for dot1 in extra_posi:
        plt.plot(dot1[0], dot1[1], color = extra_disc_color, marker = 'o', markersize = 2)
    plt.plot(0, 0, color = 'k', marker = '+', markersize = 4)
    # plt.show()
    # ax.set_xlim([-800, 800])
    # ax.set_ylim([-500, 500])
    ax.set_xlim([-400, 400])
    ax.set_ylim([-260, 260])
    # ax.set_title('wS_%s_eS_%s_%s_E.png' %(newWindowSize,ka,kb))

    # 边框不可见
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # 坐标不可见
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    ax.patch.set_facecolor('lightgray')
    plt.show()

    fig.savefig('efull%s.svg' % (name_str), bbox_inches = 'tight', pad_inches = 0)


def drawEllipses(posi, ka, kb, ellipseColor, ellipsetransp = 0.5, extra_posi = [], extra_disc_color = 'orangered', name_str = 1):
    eccentricities2 = []
    for i in range(len(posi)):
        eccentricities0 = distance.euclidean(posi[i], (0, 0))
        eccentricities2.append(eccentricities0)
    # radial
    angle_deg3 = []
    for ang in range(len(posi)):
        angle_rad0s = atan2(posi[ang][1], posi[ang][0])
        angle_deg0s = angle_rad0s * 180 / pi
        angle_deg3.append(angle_deg0s)

    my_e = [Ellipse(xy = posi[j], width = eccentricities2[j] * ka * 2, height = eccentricities2[j] * kb * 2,
                    angle = angle_deg3[j])
            for j in range(len(posi))]

    fig, ax = plt.subplots(subplot_kw = {'aspect': 'equal'}, figsize = (4, 3))

    for e in my_e:
        ax.add_artist(e)
        # random color?
        e.set_clip_box(ax.bbox)
        # e.set_alpha(np.random.rand())
        e.set_alpha(ellipsetransp)
        # e.set_facecolor(np.random.rand(3))
        # change face color here
        if ellipseColor == 'orangered':
            e.set_facecolor('orangered')  # 'royalblue'
        else:
            e.set_facecolor(ellipseColor)
        # e.set_facecolor('royalblue')

    # plot central discs
    for dot in posi:
        plt.plot(dot[0], dot[1], color = 'k', marker = 'o', markersize = 2)

    if len(extra_posi) != 0:
        for dot in extra_posi:
            plt.plot(dot[0], dot[1], color = extra_disc_color, marker = 'o', markersize = 2)

    plt.plot(0, 0, color = 'k', marker = '+', markersize = 4)

    # set x,y lim
    ax.set_xlim([-400, 400])
    ax.set_ylim([-260, 260])
    # 边框不可见
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # 坐标不可见
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    # set background color
    ax.patch.set_facecolor('lightgray')
    plt.show()
    # fig.savefig('%s.svg' % (name_str), bbox_inches = 'tight', pad_inches = 0)
    fig.savefig('%s.png' % (name_str), bbox_inches = 'tight', pad_inches = 0)


def drawEllipses_homo(posi, ka, kb, ellipseColor, ellipsetransp = 0.5, extra_posi = [], extra_disc_color = 'orangered'):
    eccentricities2 = []
    for i in range(len(posi)):
        eccentricities0 = distance.euclidean(posi[i], (0, 0))
        eccentricities2.append(eccentricities0)
    # radial
    angle_deg3 = []
    for ang in range(len(posi)):
        angle_rad0s = atan2(posi[ang][1], posi[ang][0])
        angle_deg0s = angle_rad0s * 180 / pi
        angle_deg3.append(angle_deg0s)

    my_e = [Ellipse(xy = posi[j], width = ka * 2, height = kb * 2,
                    angle = angle_deg3[j])
            for j in range(len(posi))]

    fig, ax = plt.subplots(subplot_kw = {'aspect': 'equal'}, figsize = (4, 3))

    for e in my_e:
        ax.add_artist(e)
        # random color?
        e.set_clip_box(ax.bbox)
        # e.set_alpha(np.random.rand())
        e.set_alpha(ellipsetransp)
        # e.set_facecolor(np.random.rand(3))
        # change face color here
        if ellipseColor == 'orangered':
            e.set_facecolor('orangered')  # 'royalblue'
        else:
            e.set_facecolor(ellipseColor)
        # e.set_facecolor('royalblue')

    # plot central discs
    for dot in posi:
        plt.plot(dot[0], dot[1], color = 'k', marker = 'o', markersize = 2)

    if len(extra_posi) != 0:
        for dot in extra_posi:
            plt.plot(dot[0], dot[1], color = extra_disc_color, marker = 'o', markersize = 2)

    plt.plot(0, 0, color = 'k', marker = '+', markersize = 4)

    # set x,y lim
    ax.set_xlim([-400, 400])
    ax.set_ylim([-260, 260])
    # 边框不可见
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # 坐标不可见
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    # set background color
    ax.patch.set_facecolor('lightgray')
    plt.show()
    fig.savefig('e%s.svg' % (str(posi)[0:15]), bbox_inches = 'tight', pad_inches = 0)

def draw_disc_only(e_posi):
    fig, ax = plt.subplots(subplot_kw = {'aspect': 'equal'}, figsize = (4, 3))
    for dot in e_posi:
        plt.plot(dot[0], dot[1], color = 'k', marker = 'o', markersize = 2)
    plt.plot(0, 0, color = 'k', marker = '+', markersize = 4)

    # set x,y lim
    ax.set_xlim([-400, 400])
    ax.set_ylim([-260, 260])
    # 边框不可见
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # 坐标不可见
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    # set background color
    ax.patch.set_facecolor('lightgray')
    plt.show()

    fig.savefig('disc%s.svg' % (str(e_posi)[0:15]), bbox_inches = 'tight', pad_inches = 0)


def draw_mix_color_discs(base_posi, extra_posi):
    fig, ax = plt.subplots(subplot_kw = {'aspect': 'equal'}, figsize = (4, 3))
    for dot in base_posi:
        plt.plot(dot[0], dot[1], color = 'k', marker = 'o', markersize = 2)
    for dot in extra_posi:
        plt.plot(dot[0], dot[1], color = 'white', marker = 'o', markersize = 2)
    plt.plot(0, 0, color = 'k', marker = '+', markersize = 4)

    # set x,y lim
    ax.set_xlim([-400, 400])
    ax.set_ylim([-260, 260])
    # 边框不可见
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # 坐标不可见
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    # set background color
    ax.patch.set_facecolor('lightgray')
    plt.show()

    fig.savefig('disc%s.svg' % (str(extra_posi)[0:15]), bbox_inches = 'tight', pad_inches = 0)

def drawEllipse_crowding(e_posi, black_disc_posi, red_disc_posi, crowding_posi, ka, kb, ellipseColor_r = 'royalblue',
                         savefig = False):
    """
    crowding display: show discs that falls into others crowding zones.
    """
    eccentricities = []
    for i in range(len(e_posi)):
        eccentricities0 = distance.euclidean(e_posi[i], (0, 0))
        eccentricities.append(eccentricities0)
    # radial
    angle_deg = []
    for ang in range(len(e_posi)):
        angle_rad0 = atan2(e_posi[ang][1], e_posi[ang][0])
        angle_deg0 = angle_rad0 * 180 / pi
        angle_deg.append(angle_deg0)

    # crowding disc
    eccentricities_c = []
    for i in range(len(crowding_posi)):
        eccentricities0 = distance.euclidean(crowding_posi[i], (0, 0))
        eccentricities_c.append(eccentricities0)
    angle_deg_c = []
    for ang in range(len(crowding_posi)):
        angle_rad0 = atan2(crowding_posi[ang][1], crowding_posi[ang][0])
        angle_deg0 = angle_rad0 * 180 / pi
        angle_deg_c.append(angle_deg0)
    my_e = [Ellipse(xy = crowding_posi[j], width = eccentricities_c[j] * ka * 2, height = eccentricities_c[j] * kb * 2,
                    angle = angle_deg_c[j], linestyle = "--")
            for j in range(len(crowding_posi))]

    fig, ax = plt.subplots(subplot_kw = {'aspect': 'equal'}, figsize = (8, 6))
    for e in my_e:
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_edgecolor(ellipseColor_r)
        e.set_fill(False)

    # show the discs on the ellipses-flower
    for dot in e_posi:
        plt.plot(dot[0], dot[1], color = 'k', marker = 'o', markersize = 4, alpha = 0.3)
    for dot in black_disc_posi:
        plt.plot(dot[0], dot[1], color = 'k', marker = 'o', markersize = 4)
    for dot in red_disc_posi:
        plt.plot(dot[0], dot[1], color = 'orangered', marker = 'o', markersize = 4)

    # add concentric circles
    for posi in black_disc_posi:
        ax.add_patch(
                plt.Circle((0, 0), distance.euclidean(posi, (0, 0)), alpha = 0.5, linestyle = "--", fill = False))
    # fixation
    plt.plot(0, 0, color = 'k', marker = '+', markersize = 10)

    # x, y limit
    ax.set_xlim([-400, 400])
    ax.set_ylim([-260, 260])

    # 边框不可见
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # 坐标不可见
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    ax.patch.set_facecolor('lightgray')
    plt.show()
    if savefig:
        fig.savefig('try.svg', bbox_inches = 'tight', pad_inches = 0)