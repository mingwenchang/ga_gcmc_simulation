#!/usr/bin/env python3
# coding=UTF-8
"""
NAME
        constructor.py -  A central module for GA/GCMC scripts

                        
DESCRIPTION
        Generate a random structure
        
        Land the structure to a position on a reference deck    

DEVELOPER: 
    
    Dr. Ming-Wen Chang
    E-mail: ming.wen.c@gmail.com

"""

import numpy as np
import modules.assister as ast
import modules.data as data
#import modules.vasp_io2 as vio
from itertools import combinations_with_replacement
from collections import OrderedDict
#import examiner as exm


class DummyCluster:
    def __init__(self, atomtypes=[], natoms=[], sigma=0.05, radiustype='covalent'):
        self.atomtypes = atomtypes
        self.natoms = natoms
        #self.info = {"atomtypes":atomtypes, "natoms":natoms}
        self.sigma = sigma # the standard deviation of the metal bonds
        #self.expd = expd #An expanding constant
        
        if radiustype == 'ionic':
            self.radii = data.atomic_ionic_radii
        else:
            self.radii = data.atomic_covalent_radii
            
        self.generate()
                
    def __repr__(self):
        cf = '' 
        for atom, number in zip(self.atomtypes, self.natoms):
            cf +=atom
            if number > 1:
                cf +=str(number)
        return "DummyClu(%s)"%(cf)   

    def generate(self):
        import re
        pattern =r'[\*\#\$\@\%\^\&]' 
        rmc = lambda term : re.sub(pattern, '', term)
        comb = combinations_with_replacement(self.atomtypes, 2)
        d = [self.radii[rmc(x)] + self.radii[rmc(y)] for x,y in comb]
        d = np.sum(d)/len(d)
        positions = genclu_by_SBLDA(self.ntotal, mean1=d, mean2=None, dev1=self.sigma, dev2=None) 
        np.random.shuffle(positions)
        self._positions = positions
        return self._positions     
    
    def land(self, deck, point, altitude=2.30, nanchors=3, tolerance=0.20):
        #axis = np.random.choice(['x', 'y'])
        
        if nanchors > 0:
            """Adjust the orientation of the cluster to get anchoring points """
            for i in range(100000):
                self.positions  = ast.rotate_structure(self.positions, theta=1.00, 
                                                        axis = np.random.choice(['x', 'y']))
                
                zcoor = self.positions[:, 2:].flatten()
                zmin = np.min(zcoor)
                zcoor -= zmin
                ncp = np.count_nonzero(zcoor <= tolerance)   
                
                if ncp >= nanchors:
                    break
            
        #Move the cluster to the ontop position of the landing point    
        z = np.array([0,0,1])   
        self.positions = ast.move_to_the_point(self.positions, point + 10*z)
        
        #Gradully reduce the distance between the clu and the deck 
        for i in range(100000):
            self.positions -= 0.005 * z 
            dmin = ast.get_distances_betwen_two_clus(self.positions, deck)[0]
            
            if  altitude - 0.5*tolerance <= dmin <= altitude + 0.5*tolerance:
                print ('A successful landing!')
                break

        return self.positions 
    
    @property
    def datomtypes(self):
        return OrderedDict(zip(self.atomtypes, self.natoms))

    @property
    def positions(self):
        return self._positions
    
    @positions.setter
    def positions(self, value):
        self._positions = value
    
    @property
    def ntotal(self):
        return sum(self.natoms)
         
    @property
    def dmatrix(self):
        return ast.get_distance_matrix(self._positions)

    @property
    def minlength(self):#min "bonding" length
        dmatrix = self.dmatrix 
        dmatrix.sort()
        return np.min(dmatrix[:,0])
    
    @property
    def maxlength(self):#max "bonding" length
        dmatrix = self.dmatrix 
        dmatrix.sort()
        return np.max(dmatrix[:,0])
    
    """
    @property 
    def drange(self):
        return self.expd * (self.maxlength - self.minlength)
    """
    
    @property 
    def rcov(self):
        return np.average ([self.radii[x] for x in self.atomtypes])
    
    @property 
    def rins(self):
        return 2 * self.rcov * (0.5 + np.cbrt ((3 * self.ntotal) / ( 4 * np.pi * np.sqrt(2))) )
                                                         
    @property 
    def vclu(self):
        return self.ntotal * (3/4) * np.pi * self.rcov**3 
    
    @property 
    def vins(self):
        return (3/4) * np.pi * self.rins**3 
    
    @property 
    def vacc(self):
        return self.vins - self.vclu
 

#First Order Bond Length Distribution Algorithm (F-BLDA)
"""
In the First Order Bond Length Distribution Algorithm (F-BLDA), a cluster
is generated by adding a new atom at a time. A random direction will be
selected and the new atom will be placed on the line. The position of 
the new atom is to make the distances between the new atom and the other 
atoms in the current cluster greater than the lengths randomly picked from 
a normal distribution 
"""
def F_BLDA(mean, dev, clu):
    """
    Step1. 
    Generate a random direction and find atoms with the distances to the line
    are smaller than the lengths randomly picked from a normal distribution 
    """
    n = len(clu)
    u = ast.generate_a_normvect() #A unit vector in a random direction.
    local = {}; ixns = [] 
    for i in range(n):
        #A length picked from a normal distribution 
        rc = np.random.normal(mean, dev) 
        #Using the ith atom as a center and "rc" as a radius to draw a circle,
        #if the circle and the line intersect, then the distance from the ith 
        #atom to the line is smaller than the required length.  
        ixn1 , ixn2 = ast.intxn_of_a_line_and_a_sphere(pt2=u, cent=clu[i], radius=rc) 
        if ixn1 is not None:
            local[i] = rc 
            ixns.append(ixn1)
            ixns.append(ixn2)    
    """
    Step2. 
    Find a point on the line to make the distances between the point and
    the "local" atoms greater than the lengths randomly picked from a normal
    distribution and their total distance has a minimum value.
    """        
    cands = {} 
    for ixn in ixns:
        ttd = 0 #total distance 
        for k in local.keys():
            rc = local[k]
            vk = clu[k]
            d = ast.distance(vk, ixn)
            
            if d > rc or abs(d -rc) < 1E-6:
                ttd += d
            else:
                break
        else:
            cands[ttd] = ixn
                
    ttd = np.min(list(cands.keys()))  
    new = cands[ttd]
        
    clu = np.vstack((clu,new))
    clu = ast.move_to_origin(clu)
    return clu

def genclu_by_FBLDA(natoms=1, mean=2.50, dev=0.05):
    clu = np.array([0.0000, 0.0000, 0.0000])
    if natoms > 1:
        for i in range(1, natoms):
            clu = F_BLDA(mean, dev, clu)
    return clu

#Second Order Bond Length Distribution Algorithm (S-BLDA)
def S_BLDA(clu, mean1=2.50, mean2=None, dev1=0.05, dev2=None):
    if mean2 == None:
        mean2 = mean1 + dev1
    if dev2 == None:
        dev2 = dev1
        
    bad = True
    while bad:
        
        #Part I: selection
        rc1 = np.random.normal(mean1, dev1) 
        rc2 = np.random.normal(mean2, dev2)
        while True:
            i, j = ast.selector(2, len(clu))
            dij = ast.distance(clu[i], clu[j])
            if dij < rc1 + rc2:
                break   
                
        #Part II: circling
        rc0, c, n  = ast.intxn_of_two_spheres(clu[i], clu[j], rc1, rc2) 
        
        #Part III: projecting a point to the interection circle
        x0 = rc0 * ast.generate_a_normvect() + c #A vector in a random direction.
        p0 =  ast.projection_of_a_point_to_a_plane(x0, c, n)
        v = (p0 - c) / ast.vectornorm (p0 - c)  
        p = c + rc0 * v
        
        #Part IV: checking 
        for k in range(len(clu)):
            if k != i and k !=j:
                rc = np.random.normal(mean1, dev1) 
                vk = clu[k]
                dkp = ast.distance(vk, p)
                if dkp < rc:
                    bad = True
                    break
        else:
            new = p 
            bad = False
        
    clu = np.vstack((clu,new))
    clu = ast.move_to_origin(clu)
    return clu

def genclu_by_SBLDA(natoms=1, mean1=2.50, mean2=None, dev1=0.05, dev2=None):
    clu = np.array([[0.0000, 0.0000, -0.5*mean1],
                    [0.0000, 0.0000, +0.5*mean1]])
    if natoms > 2:
        for i in range(2, natoms):
            clu = S_BLDA(clu, mean1, mean2, dev1, dev2) 
    elif natoms == 1:
        clu = np.array([0.0000, 0.0000, 0.0000])
    return clu



'''
#-----------------------generate a random structure ---------------------------
#By giving a number how many atoms in a cluster, a set of atoms will be randomly 
#generated in a box with size of L x L x L. Then they will be gathered together
#forming a cluster according to the theoretically shortest and longest bond 
#distance between the atoms
def produce(natoms, boxsize=10.00, cutoff_low=2.2, cutoff_up=2.80, bridge='default'):
    
    if type(bridge) != int or type(bridge) != float:
        bridge = (cutoff_low + cutoff_up) / 2
    else:
        if bridge < cutoff_low or bridge > cutoff_up:
            bridge = (cutoff_low + cutoff_up) / 2

    structure = np.random.uniform (-boxsize/2, boxsize/2, size = (natoms,3))       
    structure = ast.move_fragments(structure, bridge, cutoff_up)
    structure = ast.move_to_origin(structure)
    return structure
'''


'''
#Land a free cluster onto a hypothetical surface.     
def land(structure, deck, position, altitude=1.8, nanchors=3, tolerance=0.15):
    indexes, anchors, landedstru = ast.search_anchoring_points(structure, nanchors, tolerance)
    anchorscenter = ast.get_center_point(anchors)
    z_basis = np.array([0,0,1])
    vector = (position - anchorscenter) + z_basis * altitude
    landedstru = landedstru + vector
    vector = np.array([1,1,0])* (position - ast.get_center_point(landedstru))
    landedstru = landedstru + vector
    return landedstru

'''



'''
#------------------------------Cross over operators----------------------------
"""
To do the cross over operation, we need find a cutting plane through the center point 
of the cluster (i.e. (0,00, 0,00, 0.00)). This plane can be described by a vector
perpendicular to the plane (i.e. the nomal vector). This vector will be randomly
generated and normalized into unit. If a plane perpendicular to the support
i.e({xy}/{0,0,1} plans) is required, the z-value of the vector will be set to 
zero. By calculating the dot product between the unit normal vector and position
vectors of atoms in the cluster, we can get the angles between the unit normal 
vector and the position vectors, and thereby know the locations of the atoms 
relative to the plane. If the angles are smaller/larger/equal than/to 90 degree,
it means the atoms are on the right/left/on of the plane. 
"""

#The implementation of cut-and-splice is as follow:  
#Cut a cluster along a plane
def cut(cluster,normvect):
    origin = np.array([0.0000, 0.0000, 0.0000])
    center  = ast.get_center_point(cluster) #preserve the original center
    cluster = ast.move_to_the_point(cluster, origin)
    
    #workhorse
    right = []; left = []
    for posvect in cluster:
        if ast.angle(posvect, normvect) < 90:
            right.append(posvect)
            
        else:
            left.append(posvect) 
    
    #move to the original center
    cluster = ast.move_structure(cluster, center)
            
    #sort atoms accordint to their distances to the cut plan  
    right = ast.sort_vectors(right)
    left  = ast.sort_vectors(left)
    #and move their back to their orignal positions
    if len(right) > 0:
        right = ast.move_structure(right, center)
    if len(left) > 0:
        left  = ast.move_structure(left, center)

    return right, left

#for dictionarian coordinates
def cut2(cluster,normvect):
    origin = np.array([0.0000, 0.0000, 0.0000])
    center  = ast.get_center_point(ast.merge(cluster)) #preserve the original center
    cluster = ast.move_to_the_point2(cluster, origin)
    
    #workhorse
    right = OrderedDict(); left = OrderedDict()
    for element in cluster.keys():
        right[element] = []; left[element] = []
        for posvect in cluster[element]:
            if ast.angle(posvect, normvect) < 90:
                right[element].append(posvect)
            else:
                left[element].append(posvect) 
                
        #move to the original center
        cluster[element] = ast.move_structure(cluster[element], center)
    
        #sort atoms accordint to their distances to the cut plan  
        right[element] = ast.sort_vectors(right[element])
        left[element]  = ast.sort_vectors(left[element])
        #and move their back to their orignal positions
        if len(right[element]) > 0:
            right[element] = ast.move_structure(right[element], center)
        else:
            del right[element] 
        
        if len(left[element]) > 0:
            left[element]  = ast.move_structure(left[element], center)
        else:
            del left[element]
            
    return right, left

#Splice_two clusters into a new cluster
def splice(cutclu1, cutclu2, nstoich):
    if np.random.random() > np.random.random():
        spl_right = cutclu1[0]; spl_left = cutclu2[1]
        res_right = cutclu1[1]; res_left = cutclu2[0]
    else:
        spl_right = cutclu1[1]; spl_left = cutclu2[0]
        res_right = cutclu1[0]; res_left = cutclu2[1]
    
    #Spliced part 
    newclu = np.concatenate((spl_right, spl_left))
    newclu = ast.sort_vectors(newclu)
    
    #Residual part
    resclu = np.concatenate((res_right, res_left))
    resclu = ast.sort_vectors(resclu)
    
    #Check number of atoms in each part 
    natoms = len(newclu)# number of atoms in newclu
    nremain = len(resclu) #number of atoms in resclu

    #Remove (natoms- nstoich) atoms which are farthest away from the cutting plane
    if natoms > nstoich: 
        newclu = newclu[0:nstoich]
    #Choose (natoms- nstoich) atoms from tge residual part randomly
    elif natoms < nstoich:
        lack = nstoich - natoms
        for cycle in range(lack):
            candidates = list(range(0, nremain))
            index = np.random.choice(candidates)
            newlyadd = np.reshape(resclu[index], (1,3))
            newclu = np.concatenate((newclu, newlyadd)) 
            candidates.pop(index)
    return newclu   


#for dictionarian coordinates
def splice2(cutclu1, cutclu2, stoich):
    if np.random.random() > np.random.random():
        spl_right = cutclu1[0]; spl_left = cutclu2[1]
        res_right = cutclu1[1]; res_left = cutclu2[0]
    else:
        spl_right = cutclu1[1]; spl_left = cutclu2[0]
        res_right = cutclu1[0]; res_left = cutclu2[1]
         
    #Splice two clusters 
    newclu = OrderedDict(); resclu = OrderedDict()
    for element in stoich.keys():
        #Spliced part 
        if element in spl_right.keys():
            if element in spl_left.keys():
                newclu[element] = np.concatenate((spl_right[element], spl_left[element]))
            else:
                newclu[element] = spl_right[element]
        else:
            if element in spl_left.keys():
                newclu[element] = spl_left[element]
            else:
                newclu[element] = np.concatenate((res_right[element], res_left[element]))
                
        newclu[element] = ast.sort_vectors(newclu[element])
                
        #Residual part                  
        if element in res_right.keys():
            if element in res_left.keys():
                resclu[element] = np.concatenate((res_right[element], res_left[element]))
            else:
                resclu[element] = res_right[element]
        else:
            if element in res_left.keys():
                resclu[element] = res_left[element]
            else:
                resclu[element] = np.concatenate((spl_right[element], spl_left[element]))
                
        resclu[element] = ast.sort_vectors(resclu[element])
                
        #Check number of atoms in each part 
        natoms = len(newclu[element]) #number of atoms in newclu[element] 
        nremain = len(resclu[element]) #number of atoms in resclu[element]
        nstoich = stoich[element] #stoichiometry for the element 

        #Remove (natoms- nstoich) atoms which are farthest away from the cutting plane
        if natoms > nstoich: 
            newclu[element]= newclu[element][0:nstoich]
        #Choose stoichiometry- natoms atoms from the residual parts randomly
        elif natoms < nstoich:
            lack = nstoich - natoms
            for cycle in range(lack):
                candidates = list(range(0, nremain))
                index = np.random.choice(candidates)
                newlyadd = np.reshape(resclu[element][index], (1,3))
                newclu[element]  = np.concatenate((newclu[element], newlyadd))
                candidates.pop(index)
            
    return newclu

#------------------------------Mutation operators----------------------------
#Translate x% atoms in a cluster wtih a random distance in a random direction                           
def rattle(cluster, ratio=0.30, stretch=0.8):
    natoms = len(cluster)
    nmoves = int(natoms * ratio)
    selected = ast.selector(nmoves, natoms)    
    for i in selected:
        factor = np.random.uniform(0.00, stretch)
        vect = factor * ast.generate_a_normvect('random').reshape(1,3)
        cluster[i] = cluster[i] + vect
    return cluster

#for dictionarian coordinates
def rattle2(cluster, ratio=0.30, stretch=0.8):
    stoich = ast.pair_key_and_amount(cluster) #preserve the stoichiometry of the coordinates 
    cluster = ast.merge(cluster) #merge a dictionarian coordinate into a single array   
    natoms = len(cluster)
    nmoves = int(natoms * ratio)
    selected = ast.selector(nmoves, natoms)    
    for i in selected:
        factor = np.random.uniform(0.00, stretch)
        vect = factor * ast.generate_a_normvect('random').reshape(1,3)
        cluster[i] = cluster[i] + vect
    cluster = ast.match(cluster, stoich) #turn a single array to a dictionarian coordinate
    return cluster

#Rotate a cluster adsorbed on a surface with a random angle along the normal
#vector of the surface (i.e. Z axis).
def twist(cluster, axis='z'):
    origin = np.array([0.0000, 0.0000, 0.0000])
    angle   = np.random.uniform(0,360) # the angle of rotation; unit in degree
    center  = ast.get_center_point(cluster) #preserve the original center
    cluster = ast.move_to_the_point(cluster, origin) ##reset the center of the clu to (0,00, 0,00, 0.00)
    cluster = ast.rotate_structure(cluster, angle, axis) #do rotation
    cluster = ast.move_structure(cluster, center) #move to the original center
    return cluster

#for dictionarian coordinates
def twist2(cluster, axis='z'):
    origin = np.array([0.0000, 0.0000, 0.0000])
    angle   = np.random.uniform(0,360) # the angle of rotation; unit in degree
    stoich = ast.pair_key_and_amount(cluster) #preserve the stoichiometry of the coordinates 
    cluster = ast.merge(cluster) #merge a dictionarian coordinate into a single array
    center  = ast.get_center_point(cluster) #preserve the original center
    cluster = ast.move_to_the_point(cluster, origin) ##reset the center of the clu to (0,00, 0,00, 0.00)
    cluster = ast.rotate_structure(cluster, angle, axis) #do rotation
    cluster = ast.move_structure(cluster, center) #move to the original center
    cluster = ast.match(cluster, stoich) #turn a single array to a dictionarian coordinate   
    return cluster

#Swaps the atom types in a selected cluster, without changing the cluster 
#geometry. This is only used for bimetallic clusters. 
def permutate(cluster1, cluster2, ratio=0.30):
    natoms1 = len(cluster1); natoms2 = len(cluster2)
    if natoms1 < natoms2:
        nexchanges = int(natoms1 * ratio)
        if nexchanges < 1:
            nexchanges = 1
    else:
        nexchanges = int(natoms2 * ratio)
        if nexchanges < 1:
            nexchanges = 1
    sel1 = ast.selector(nexchanges, natoms1)
    sel2 = ast.selector(nexchanges, natoms2)
    for i, j in zip(sel1, sel2):
        cluster1[i], cluster2[j] = np.copy(cluster2[j]), np.copy(cluster1[i])
    return cluster1, cluster2

#for dictionarian coordinates
def permutate2(cluster, ratio=0.30):
    
    nelements = len(cluster.keys())
    if nelements >= 2:
        i, j = ast.selector(2, nelements)  
    else:
        i , j = 0, 0
        
    elements = list(cluster.keys())   
    element1 = elements[i]; element2 = elements[j]
    natoms1 = len(cluster[element1]); natoms2 = len(cluster[element2])
    
    if natoms1 < natoms2:
        nexchanges = int(natoms1 * ratio)
        if nexchanges < 1:
            nexchanges = 1       
    else:
        nexchanges = int(natoms2 * ratio)
        if nexchanges < 1:
            nexchanges = 1 
        
    sel1 = ast.selector(nexchanges, natoms1)
    sel2 = ast.selector(nexchanges, natoms2)
        
    for k, l in zip(sel1, sel2):
        cluster[element1][k], cluster[element2][l] = np.copy(cluster[element2][l]), np.copy(cluster[element1][k])
        
    return cluster


def cut3(atomsobj, normvect=None):
    if normvect is None:
        normvect = ast.generate_a_normvect('random') 
    
    #Save the current geometric center 
    center = atomsobj.get_center_of_geometry()
    
    #move the clu to (0, 0 ,0)
    atomsobj.move_to_origin()
    
    #Classify atoms in the clu into two parts according to thier angles 
    dot = np.dot(atomsobj.positions, normvect)
    n1 = np.linalg.norm(atomsobj.positions, axis=1) 
    n2 = np.linalg.norm(normvect, axis=0) #(3,)
    angles = np.arccos(dot/ n1 * n2 ) * (180/np.pi)
    
    #Using Boolean mask 
    leftclu  = atomsobj.positions[angles <= 90 ]
    lindx = np.arange(np.sum(atomsobj.natoms))[angles <= 90]
    
    rightclu  = atomsobj.positions[angles > 90 ] 
    rindx = np.arange(np.sum(atomsobj.natoms))[angles > 90]
    
    
    leftatomtypes = []; rightatomtypes = []
    leftnatoms = []; rightnatoms = []
    start = 0
    for elem, num in zip(atomsobj.atomtypes, atomsobj.natoms):
        #left part 
        leftnum = len(set(range(start, start+num)) & set(lindx)) 
        if leftnum > 0:
            leftatomtypes.append(elem) 
            leftnatoms.append(leftnum)
 
        #right part 
        rightnum  = len(set(range(start, start+num)) & set(rindx)) 
        if rightnum > 0:
            rightatomtypes.append(elem) 
            rightnatoms.append(rightnum)        
    
        start +=num
        
    left = vio.Atoms(atomtypes=leftatomtypes, natoms=leftnatoms, positions=leftclu, cell=atomsobj.cell)
    right = vio.Atoms(atomtypes =rightatomtypes, natoms=rightnatoms, positions=rightclu, cell=atomsobj.cell)
    
    atomsobj.move_to_the_point(center)
    left.move_to_the_point(center)
    right.move_to_the_point(center)
    return left, right
   
 
def splice3(cutatomsobj1, cutatomsobj2, stoich):
    if np.random.random() > np.random.random():
        spl_right = cutatomsobj1[0]; spl_left = cutatomsobj2[1]
        res_right = cutatomsobj1[1]; res_left = cutatomsobj2[0]
    else:
        spl_right = cutatomsobj1[1]; spl_left = cutatomsobj2[0]
        res_right = cutatomsobj1[0]; res_left = cutatomsobj2[1]
    
    #Spliced 
    new = vio.Atoms([spl_right, spl_left])
    red = vio.Atoms([res_right, res_left])  
    
    #sorted 
    start=0 
    for elem, num in zip(new.atomtypes, new.natoms):
        new.positions[start:num+start] = ast.sort_vectors(new.positions[start:num+start])
        start += num
    
    start=0 
    for elem, num in zip(red.atomtypes, red.natoms):
        red.positions[start:num+start] = ast.sort_vectors(red.positions[start:num+start])
        start += num

    #check stoichemistry
    for element in stoich:
        if element in new.atomtypes :
            nextra = new.dict_atomtypes()[element] -  stoich[element] 
            if nextra > 0 : #Remove nextra atoms which are farthest away from the cutting plane
                [new.pop(element) for i in range(nextra)]
            elif nextra  < 0:
                need = red.truncate(atomtypes=element, natoms=abs(nextra), mode='tail')
                new.append(need)
        else:
            need = red.truncate(atomtypes=element, natoms=stoich[element], mode='tail')
            new.append(need)

    return new

'''



"""
#Cluster Class is used to generate structures of clusters. 
#The structure of the cluster will be verified automatically. 
#Only the physically and chemically reasonable structure will be proposed.    
class Cluster:
    def __init__(self, natoms=8, coordnum=1, shortestbond=2.2, longestbond=2.80,\
                 bridge='default', boxsize=10.00, maxattempts= 1000000):
        
        self.natoms = natoms
        self.boxsize = boxsize
        
        self.cutoff_low = shortestbond
        self.cutoff_up = longestbond
        self.bridge = bridge
        
        self.minbondindex = coordnum - 1
        self.maxattempts = maxattempts
    
    #This part will generate a free cluster randomely, and check its reasonableness
    #automatically. If a reasonable structure was not found within 'maxattempts' times,
    #a Runtime Error message will give and the GA code will stop automatically.   
        print ('Generating a random structure....') 
        for i in range(self.maxattempts):
            structure = produce(self.natoms, self.boxsize, self.cutoff_low,\
                                 self.cutoff_up, self.bridge)
            
            bad = exm.is_a_bad_structure(structure, self.cutoff_low,\
                                              self.cutoff_up, self.minbondindex)
            if bad:
                continue
            else:
                print ('A reasonable structure was generated in cycle %s.' %(i))
                break
        else:
            RuntimeError("Sorry, no reasonable structure was found.")
        self.structure = structure 



    #Throw a cluster to a specific position on a plane     
    def land(self, deck, position, altitude, nanchors=3, shortestfoot=1.8,\
             longestfoot=2.8, tolerance=0.15):
        
        print ('Landing the free cluster onto the deck') 
        for i in range(self.maxattempts):
            landedstru = land(self.structure, deck, position, altitude, nanchors, tolerance)
            bad = exm.is_a_bad_combination(landedstru, deck, shortestfoot,\
                                                   longestfoot, nanchors-1)
            if bad:
                continue
            else:
                print ('A successful landing') 
                break
            
        self.landedstru = landedstru 
        return landedstru        

"""