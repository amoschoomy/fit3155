import sys
from unionbyrank import find, union, init_set


def read_file(graph_file):
    with open(graph_file, "r", encoding="UTF-8") as f:
        lst = [x.rstrip() for x in f]
    return lst


def write_tofile(stats, count, n, p):
    with open("output_graphstats.txt", "w", encoding="UTF-8") as f:
        f.write(str(n)+" "+str(p)+"\n")
        f.write(str(count)+"\n")
        f.write(" ".join(str(s) for s in stats[0] if stats[0][0] != -1))
        for i in range(1, count):
            f.write("\n")
            f.write(("%s %s" % stats[i]))


def all_hamming_distance(lst):
    """
    Get all hamming distance between words

    """
    lst_of_edges = []
    for i in range(len(lst)):
        for j in range(len(lst)):
            if i>=j :
                continue
            h_d = hamming_distance(lst[i], lst[j])
            if h_d <= 2:
                lst_of_edges.append((i, j, h_d))
                lst_of_edges.append((j,i,h_d))
    return lst_of_edges


def kruskal(lst, n):
    lst.sort(key=lambda x: x[2])
    stats = [(1, 0)]*n  # stats array L=size R=weight
    count = n  # Initial N connected components
    parent = init_set(n)
    for edge in lst:
        if find(edge[0], parent) != find(edge[1], parent):
            new_root, old_root = union(edge[0], edge[1], parent)
            # Update stats
            stats[new_root] = (stats[old_root][0]+stats[new_root]
                               [0], stats[old_root][1]+stats[new_root][1]+edge[2])
            stats[old_root] = (-1, -1)
            count -= 1

    stats.sort(reverse=True)
    return stats, count


def hamming_distance(string1, string2):
    """
    Brute force hamming distance

    """

    distance = 0
    for i in range(len(string1)):
        if string1[i] != string2[i]:
            distance += 1
    return distance


if __name__ == "__main__":
    graph = sys.argv[1]
    lst_vertice = read_file(graph)
    lst_edges = all_hamming_distance(lst_vertice)
    stats, count = kruskal(lst_edges, len(lst_vertice))
    write_tofile(stats, count, len(lst_vertice), len(lst_edges)//2)
