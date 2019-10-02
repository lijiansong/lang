#!/usr/bin/python

# provide the path to the csv file to generate the ?.tex file
# then run pdflatex ?.tex to generate pdf
# for format of csv file look at csv_reader.py

from math import log
from csv_reader import read_csv
from csv_reader import get_bw_f
from csv_reader import get_oi
from csv_reader import calc_flops
import sys

peak_percent = 0.8

def write_roofline(filename, maxgflops, bwstream, oi, gflops, space, time, title, env):
    ordinal = lambda n: "%d$^{%s}$" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

    texfile = open(filename, 'w')

    graphTitle = ''.join(title) + ' : ' + ''.join(env)

    xmin = 0.5 * min(oi)
    xmax = 0.5 + max(oi)

    ymin = 0.5 * min(gflops)

    texfile.write(r"""\documentclass[tikz]{standalone}

\usepackage{pgfplots}
\usepackage{calc}

\pgfplotsset{compat=1.8}

\tikzset{every picture/.style={font issue=\footnotesize},
         font issue/.style={execute at begin picture={#1\selectfont}}
         }

\usepackage[printwatermark]{xwatermark}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{lipsum}


\begin{document}

  \begin{tikzpicture}[domain=0:32]
  \begin{axis}[
    title={%s},
    height=250pt,
    width=400pt,
    scale=1.0,
    xmode=log,
    ymode=log,
    xmin=%f,
    xmax=%f,
    ymin=%f,
    xlabel = Operational intensity (Flops/Byte),
    ylabel = Performance (GFlops/sec),
    log basis y={2},
    log basis x={2},
    log ticks with fixed point,
    x tick label style={rotate=45, anchor=east},
    grid=major,
    grid style={dotted, cyan},
    x tick label style={/pgf/number format/.cd},
    xticklabel shift=.0cm,
    xtick={""" % (graphTitle, xmin, xmax, ymin))

    for i in range(len(gflops)-1):
        texfile.write("%f, "%oi[i])
    texfile.write("""%f},
    xticklabels={"""%oi[len(gflops)-1])

    for i in range(len(gflops)-1):
        texfile.write("{OI=%.1f,p=%s}, "%(oi[i], space[i]))
    texfile.write("""{OI=%.1f,p=%s}} ]
                     """%(oi[len(gflops)-1], space[len(gflops)-1]))

    dx = oi[1]-oi[0]
    for i in range(2, len(oi)):
        dx = min(dx, oi[i]-oi[i-1])
    dx *= 0.8

    for oi_i, gflops_i in zip(oi, gflops):
        # Performance achieved.
        peak = min(oi_i*bwstream, maxgflops)
        peak80 = peak_percent*peak
        percent = (100.*gflops_i/peak)

        texfile.write(r"""\addplot[mark=*] coordinates {(%g, %g)}
                          node[left, sloped] {\tiny %.0f\%%};
                          """ % (oi_i, gflops_i, percent))

        # Codes OI
        texfile.write(r"""\addplot+[sharp plot, mark=none,
                          color=green, style=solid, line width=1.5pt] coordinates
                          {(%f, %f) (%f, %f)};
                          """ % (oi_i, ymin, oi_i, gflops_i))

        texfile.write(r"""\addplot+[sharp plot, mark=none,
                          color=blue, style=dashed, line width=1.5pt] coordinates
                          {(%f, %f) (%f, %f)};
                          """ % (oi_i, gflops_i, oi_i, peak80))

        texfile.write(r"""\addplot+[sharp plot, mark=none,
                          color=red, style=dashed, line width=1.5pt] coordinates
                          {(%f, %f) (%f, %f)};
                          """ % (oi_i, peak80, oi_i, peak))


    # Measured memory bandwidth
    texfile.write(r"""\addplot+[sharp plot, mark=none, style=solid,
                      color=blue, line width=1.5pt] coordinates
                      {(%f, %f) (%f, %f)};
                   """ % (maxgflops/bwstream, maxgflops, xmax, maxgflops))

    texfile.write(r"""\addplot+[sharp plot, mark=none, style=solid,
                      color=blue, line width=1.5pt] coordinates
                      {(%f, %f) (%f, %f)}
                      node[above, sloped, pos = .3] {Memory bandwidth (STREAM)};
                      """ % (xmin, xmin*bwstream,
                             maxgflops/bwstream, maxgflops))

    texfile.write(r"""\end{axis}
    \end{tikzpicture}
    \end{document}
    """)
    texfile.close()


def draw_roofline(filepath):
    result = read_csv(filepath)
    meta = result[0]
    testname = meta[0]
    timestep = meta[1]
    space = meta[2]
    nbpml = meta[3]
    dimension = meta[4]
    title = result[1]
    chipname = title[0]
    outputname = chipname + '.tex'
    env = title[1]
    rest = result[2:]
    time_order = map(lambda l : l[0], rest)
    space_order = map(lambda l : l[1], rest)
    time = map(lambda l : l[2], rest)
    gflops = []
    oi = []
    for to, s, t in zip(time_order, space_order, time):
        gflops.append(calc_flops(testname, space, timestep, to, s, t, nbpml * 2, dimension))
        oi.append(get_oi(testname, to, s))
    (bw, maxflops) = get_bw_f(chipname)
    print gflops
    print oi
    print bw
    print maxflops
    write_roofline(outputname, maxflops, bw, oi, gflops, space_order, time_order, chipname, env)

draw_roofline(sys.argv[1]) 
