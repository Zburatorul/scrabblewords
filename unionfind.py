
'''
    This implements a Weighted Quick Union-Find datastructure.
    https://www.youtube.com/watch?v=H0bkmI1Xsxg
    Constructor takes an integer num = which is total number of objects we will be clustering
    It supports adding links (i,j)
    and checking whether there is a path from k to l
    Eugeniu Plamadeala <eugeniu@plamadeala.com>
'''
class UF:

    def __init__(self, num):
        self.num = num

        # This numbers the objects 0...n-1 and assigns to each
        # an id equal to itself
        self.id = list(range(num))

        # this will store the size of the cluster that each
        # object is part of
        self.sz = [1] * num

        # reflects how many clusters there are
        self.components = num

    def root(self, i):
        p = i

        # every object has a root
        # go up the tree until you find the root of the entire cluster
        while self.id[p] != p:
            # compress path along the way
            self.id[p] = self.id[self.id[p]]
            p = self.id[p]
        return p

    '''
        Creates a link between objects i an j.
        Since each may already belong to a cluster whose root is r1
        or r2 respectively, we need to instead link these two clusters
        by either making r1 the root of r2 or vice-versa.
        We do this in a weighted by comparing the sizes of the
        two clusters
    '''
    def union(self, i, j):
        r1 = self.root(i)
        r2 = self.root(j)
        if r1 == r2:
            return
        if self.sz[i] >= self.sz[j]:
            self.id[r2] = r1
            self.sz[r1] = self.sz[r1] + self.sz[r2]
        else:
            self.id[r1] = r2
            self.sz[r2] = self.sz[r2] + self.sz[r1]

        # after every linking the number of clusters decreases by 1
        self.components = self.components - 1

    def connected(self, i, j):
        # if two objects have same root, they are in same cluster
        # and there is a path between them
        return self.root(i) == self.root(j)

    def numClusters(self):
        return self.components

    '''
        print the roots corresponding to disjoint clusters
    '''
    def printClusters(self):
        #lst_cluster_roots = []
        num_seen = 0
        for i in range(self.num):
            # is the object a cluster root
            if i == self.id[i]:
                print(i)
                num_seen += 1
        print('Seen: %d clusters' % num_seen)
        print('numCluster reports: %d' % self.numClusters())
