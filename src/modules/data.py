#!/usr/bin/env python3
# coding=UTF-8
"""
NAME
        data.py -  A central module for GA/GCMC scripts. 

                        
DESCRIPTION
        Store atom's various chemical properties.
        
            
DEVELOPER: 
    
    Dr. Ming-Wen Chang
    E-mail: ming.wen.c@gmail.com

"""
from collections import OrderedDict
    
atomic_numbers = OrderedDict([
     ('X', 0),
     ('H', 1),
     ('He', 2),
     ('Li', 3),
     ('Be', 4),
     ('B', 5),
     ('C', 6),
     ('N', 7),
     ('O', 8),
     ('F', 9),
     ('Ne', 10),
     ('Na', 11),
     ('Mg', 12),
     ('Al', 13),
     ('Si', 14),
     ('P', 15),
     ('S', 16),
     ('Cl', 17),
     ('Ar', 18),
     ('K', 19),
     ('Ca', 20),
     ('Sc', 21),
     ('Ti', 22),
     ('V', 23),
     ('Cr', 24),
     ('Mn', 25),
     ('Fe', 26),
     ('Co', 27),
     ('Ni', 28),
     ('Cu', 29),
     ('Zn', 30),
     ('Ga', 31),
     ('Ge', 32),
     ('As', 33),
     ('Se', 34),
     ('Br', 35),
     ('Kr', 36),
     ('Rb', 37),
     ('Sr', 38),
     ('Y', 39),
     ('Zr', 40),
     ('Nb', 41),
     ('Mo', 42),
     ('Tc', 43),
     ('Ru', 44),
     ('Rh', 45),
     ('Pd', 46),
     ('Ag', 47),
     ('Cd', 48),
     ('In', 49),
     ('Sn', 50),
     ('Sb', 51),
     ('Te', 52),
     ('I', 53),
     ('Xe', 54),
     ('Cs', 55),
     ('Ba', 56),
     ('La', 57),
     ('Ce', 58),
     ('Pr', 59),
     ('Nd', 60),
     ('Pm', 61),
     ('Sm', 62),
     ('Eu', 63),
     ('Gd', 64),
     ('Tb', 65),
     ('Dy', 66),
     ('Ho', 67),
     ('Er', 68),
     ('Tm', 69),
     ('Yb', 70),
     ('Lu', 71),
     ('Hf', 72),
     ('Ta', 73),
     ('W', 74),
     ('Re', 75),
     ('Os', 76),
     ('Ir', 77),
     ('Pt', 78),
     ('Au', 79),
     ('Hg', 80),
     ('Tl', 81),
     ('Pb', 82),
     ('Bi', 83),
     ('Po', 84),
     ('At', 85),
     ('Rn', 86),
     ('Fr', 87),
     ('Ra', 88),
     ('Ac', 89),
     ('Th', 90),
     ('Pa', 91),
     ('U', 92),
     ('Np', 93),
     ('Pu', 94),
     ('Am', 95),
     ('Cm', 96),
     ('Bk', 97),
     ('Cf', 98),
     ('Es', 99),
     ('Fm', 100),
     ('Md', 101),
     ('No', 102),
     ('Lr', 103),
     ('Rf', 104),
     ('Db', 105),
     ('Sg', 106),
     ('Bh', 107),
     ('Hs', 108),
     ('Mt', 109),
     ('Ds', 110),
     ('Rg', 111),
     ('Cn', 112),
     ('Nh', 113),
     ('Fl', 114),
     ('Mc', 115),
     ('Lv', 116),
     ('Ts', 117),
     ('Og', 118)])

atomic_masses = OrderedDict([
     ('X', 0.000),
     ('H', 1.008),
     ('He', 4.002602),
     ('Li', 6.94),
     ('Be', 9.0121831),
     ('B', 10.81),
     ('C', 12.011),
     ('N', 14.007),
     ('O', 15.999),
     ('F', 18.998403163),
     ('Ne', 20.1797),
     ('Na', 22.98976928),
     ('Mg', 24.305),
     ('Al', 26.9815385),
     ('Si', 28.085),
     ('P', 30.973761998),
     ('S', 32.06),
     ('Cl', 35.45),
     ('Ar', 39.948),
     ('K', 39.0983),
     ('Ca', 40.078),
     ('Sc', 44.955908),
     ('Ti', 47.867),
     ('V', 50.9415),
     ('Cr', 51.9961),
     ('Mn', 54.938044),
     ('Fe', 55.845),
     ('Co', 58.933194),
     ('Ni', 58.6934),
     ('Cu', 63.546),
     ('Zn', 65.38),
     ('Ga', 69.723),
     ('Ge', 72.63),
     ('As', 74.921595),
     ('Se', 78.971),
     ('Br', 79.904),
     ('Kr', 83.798),
     ('Rb', 85.4678),
     ('Sr', 87.62),
     ('Y', 88.90584),
     ('Zr', 91.224),
     ('Nb', 92.90637),
     ('Mo', 95.95),
     ('Tc', 97.90721),
     ('Ru', 101.07),
     ('Rh', 102.9055),
     ('Pd', 106.42),
     ('Ag', 107.8682),
     ('Cd', 112.414),
     ('In', 114.818),
     ('Sn', 118.71),
     ('Sb', 121.76),
     ('Te', 127.6),
     ('I', 126.90447),
     ('Xe', 131.293),
     ('Cs', 132.90545196),
     ('Ba', 137.327),
     ('La', 138.90547),
     ('Ce', 140.116),
     ('Pr', 140.90766),
     ('Nd', 144.242),
     ('Pm', 144.91276),
     ('Sm', 150.36),
     ('Eu', 151.964),
     ('Gd', 157.25),
     ('Tb', 158.92535),
     ('Dy', 162.5),
     ('Ho', 164.93033),
     ('Er', 167.259),
     ('Tm', 168.93422),
     ('Yb', 173.054),
     ('Lu', 174.9668),
     ('Hf', 178.49),
     ('Ta', 180.94788),
     ('W', 183.84),
     ('Re', 186.207),
     ('Os', 190.23),
     ('Ir', 192.217),
     ('Pt', 195.084),
     ('Au', 196.966569),
     ('Hg', 200.592),
     ('Tl', 204.38),
     ('Pb', 207.2),
     ('Bi', 208.9804),
     ('Po', 208.98243),
     ('At', 209.98715),
     ('Rn', 222.01758),
     ('Fr', 223.01974),
     ('Ra', 226.02541),
     ('Ac', 227.02775),
     ('Th', 232.0377),
     ('Pa', 231.03588),
     ('U', 238.02891),
     ('Np', 237.04817),
     ('Pu', 244.06421),
     ('Am', 243.06138),
     ('Cm', 247.07035),
     ('Bk', 247.07031),
     ('Cf', 251.07959),
     ('Es', 252.083),
     ('Fm', 257.09511),
     ('Md', 258.09843),
     ('No', 259.101),
     ('Lr', 262.11),
     ('Rf', 267.122),
     ('Db', 268.126),
     ('Sg', 271.134),
     ('Bh', 270.133),
     ('Hs', 269.1338),
     ('Mt', 278.156),
     ('Ds', 281.165),
     ('Rg', 281.166),
     ('Cn', 285.177),
     ('Nh', 286.182),
     ('Fl', 289.19),
     ('Mc', 289.194),
     ('Lv', 293.204),
     ('Ts', 293.208),
     ('Og', 294.214)])

nan = 0.20 
atomic_covalent_radii = OrderedDict([
     ('X', nan),
     ('H', 0.31),
     ('He', 0.28),
     ('Li', 1.28),
     ('Be', 0.96),
     ('B', 0.84),
     ('C', 0.76),
     ('N', 0.71),
     ('O', 0.66),
     ('F', 0.57),
     ('Ne', 0.58),
     ('Na', 1.66),
     ('Mg', 1.41),
     ('Al', 1.21),
     ('Si', 1.11),
     ('P', 1.07),
     ('S', 1.05),
     ('Cl', 1.02),
     ('Ar', 1.06),
     ('K', 2.03),
     ('Ca', 1.76),
     ('Sc', 1.7),
     ('Ti', 1.6),
     ('V', 1.53),
     ('Cr', 1.39),
     ('Mn', 1.39),
     ('Fe', 1.32),
     ('Co', 1.26),
     ('Ni', 1.24),
     ('Cu', 1.32),
     ('Zn', 1.22),
     ('Ga', 1.22),
     ('Ge', 1.2),
     ('As', 1.19),
     ('Se', 1.2),
     ('Br', 1.2),
     ('Kr', 1.16),
     ('Rb', 2.2),
     ('Sr', 1.95),
     ('Y', 1.9),
     ('Zr', 1.75),
     ('Nb', 1.64),
     ('Mo', 1.54),
     ('Tc', 1.47),
     ('Ru', 1.46),
     ('Rh', 1.42),
     ('Pd', 1.39),
     ('Ag', 1.45),
     ('Cd', 1.44),
     ('In', 1.42),
     ('Sn', 1.39),
     ('Sb', 1.39),
     ('Te', 1.38),
     ('I', 1.39),
     ('Xe', 1.4),
     ('Cs', 2.44),
     ('Ba', 2.15),
     ('La', 2.07),
     ('Ce', 2.04),
     ('Pr', 2.03),
     ('Nd', 2.01),
     ('Pm', 1.99),
     ('Sm', 1.98),
     ('Eu', 1.98),
     ('Gd', 1.96),
     ('Tb', 1.94),
     ('Dy', 1.92),
     ('Ho', 1.92),
     ('Er', 1.89),
     ('Tm', 1.9),
     ('Yb', 1.87),
     ('Lu', 1.87),
     ('Hf', 1.75),
     ('Ta', 1.7),
     ('W', 1.62),
     ('Re', 1.51),
     ('Os', 1.44),
     ('Ir', 1.41),
     ('Pt', 1.36),
     ('Au', 1.36),
     ('Hg', 1.32),
     ('Tl', 1.45),
     ('Pb', 1.46),
     ('Bi', 1.48),
     ('Po', 1.4),
     ('At', 1.5),
     ('Rn', 1.5),
     ('Fr', 2.6),
     ('Ra', 2.21),
     ('Ac', 2.15),
     ('Th', 2.06),
     ('Pa', 2.0),
     ('U', 1.96),
     ('Np', 1.9),
     ('Pu', 1.87),
     ('Am', 1.8),
     ('Cm', 1.69),
     ('Bk', nan),
     ('Cf', nan),
     ('Es', nan),
     ('Fm', nan),
     ('Md', nan),
     ('No', nan),
     ('Lr', nan),
     ('Rf', nan),
     ('Db', nan),
     ('Sg', nan),
     ('Bh', nan),
     ('Hs', nan),
     ('Mt', nan),
     ('Ds', nan),
     ('Rg', nan),
     ('Cn', nan),
     ('Nh', nan),
     ('Fl', nan),
     ('Mc', nan),
     ('Lv', nan),
     ('Ts', nan),
     ('Og', nan)])
