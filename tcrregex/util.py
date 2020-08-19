# from scipy.cluster import hierarchy # scipy.cluster is not yet in tcrregex folder
# from scipy.spatial import distance
import logging

#from .all_genes import all_genes
from .all_genes import all_genes as all_genes_default
from . import cdr3s_human
from . import basic
from . import html_colors

logger = logging.getLogger('util.py')

def get_rep( gene, organism ):
    assert gene.startswith('TR')
    vj = gene[3]
    if vj == 'V':
        rep = cdr3s_human.all_loopseq_representative[ organism ][ gene ]
    else:
        rep = cdr3s_human.all_jseq_representative[ organism ][ gene ]
    return rep


def get_mm1_rep( gene, organism ):
    assert gene.startswith('TR')
    vj = gene[3]
    if vj == 'V':
        rep = cdr3s_human.all_loopseq_representative_mm1[ organism ][ gene ]
    else:
        rep = cdr3s_human.all_jseq_representative[ organism ][ gene ]
    return rep


def get_rep_ignoring_allele( gene, organism ):
    rep = get_rep( gene, organism )
    rep = rep[:rep.index('*')]
    return rep

def tree_sort( old_l, distances, return_leaves=True ): ## average linkage
    assert len(distances) == len(old_l)

    if len(old_l)==1:
        leaves = [0]
    else:
        y = distance.squareform( distances, checks=True )
        Z = hierarchy.average( y )
        #c,coph_dists = hierarchy.cophenet(Z,y)
        leaves = hierarchy.leaves_list( Z )

    new_l = [ old_l[x] for x in leaves ]

    if not return_leaves:
        return new_l
    else:
        return new_l, leaves

def get_top_genes( blast_hits_string ):
    hits = dict( [ ( x.split(':')[0], int( x.split(':')[1] ) ) for x in blast_hits_string.split(';') ] )
    top_score = max( hits.values() )
    return { x for x, y in hits.items() if y >= top_score }

def get_top_reps( blast_hits_string, organism, all_genes = all_genes_default ):
    hits = dict( [ ( x.split(':')[0], int( x.split(':')[1] ) ) for x in blast_hits_string.split(';') ] )
    top_score = max( hits.values() )
    # vj = hits.keys()[0][3]
    # if vj == 'V':
    #     rep_map = cdr3s_human.all_loopseq_representative[ organism ]
    # else:
    #     assert vj == 'J'
    #     rep_map = cdr3s_human.all_jseq_representative[ organism ]
    return { all_genes[organism][x].rep for x, y in hits.items() if y >= top_score }


def reps_from_genes( genes, organism, mm1=False, trim_allele=False, all_genes = all_genes_default ):
    ## if genes is a set we can't index into it
    # vj = [ x[3] for x in genes ][0]

    # if vj == 'V':
    #     if mm1:
    #         rep_map = cdr3s_human.all_loopseq_representative_mm1[ organism ]
    #     else:
    #         rep_map = cdr3s_human.all_loopseq_representative[ organism ]
    # else:
    #     assert vj == 'J'
    #     rep_map = cdr3s_human.all_jseq_representative[ organism ]

    # reps = set( [ rep_map[x] for x in genes ] )
    reps = set( ( all_genes[organism][x].mm1_rep for x in genes ) ) if mm1 else \
           set( ( all_genes[organism][x].rep     for x in genes ) )
    if trim_allele:
        reps = set( ( x[:x.index('*')] for x in reps ) )
    return reps


def get_mm1_rep_ignoring_allele( gene, organism ): # helper fxn
    rep = get_mm1_rep( gene, organism )
    rep = rep[:rep.index('*')]
    return rep

def get_allele2mm1_rep_gene_for_counting(all_genes = all_genes_default):
    allele2mm1_rep_gene_for_counting = {}
    for organism in ['human', 'mouse']:
        allele2mm1_rep_gene_for_counting[ organism ] = {}

        for chain in 'AB':

            ## look at gene/allele maps
            vj_alleles = { 'V': [ id for (id, g) in all_genes[organism].items() if g.chain==chain and g.region=='V'],
                           'J': [ id for (id, g) in all_genes[organism].items() if g.chain==chain and g.region=='J'] }

            for vj, alleles in vj_alleles.items():
                gene2rep = {}
                gene2alleles = {}
                rep_gene2alleles = {}

                for allele in alleles:
                    #assert allele[2] == chain
                    gene = allele[:allele.index('*')]
                    rep_gene = get_mm1_rep_ignoring_allele( allele, organism )
                    if rep_gene not in rep_gene2alleles:
                        rep_gene2alleles[ rep_gene ] = []
                    rep_gene2alleles[ rep_gene ].append( allele )

                    if gene not in gene2rep:
                        gene2rep[gene] = set()
                        gene2alleles[gene] = []
                    gene2rep[ gene ].add( rep_gene )
                    gene2alleles[gene].append( allele )

                merge_rep_genes = {}
                for gene, reps in gene2rep.items():
                    if len(reps)>1:
                        assert vj=='V'
                        logger.debug('multireps: %s, %s, %s', organism, gene, reps)
                        '''
                        for allele in gene2alleles[gene]:
                            logger.debug('%s %s %s %s' % (' '.join(all_genes[organism][allele].cdrs), allele, get_rep(allele,organism), get_mm1_rep(allele,organism)))
                        '''

                        ## we are going to merge these reps
                        ## which one should we choose?
                        l = sorted([ (len(rep_gene2alleles[rep]), rep ) for rep in reps ])
                        l = l[::-1]
                        assert l[0][0] > l[1][0]
                        toprep = l[0][1]
                        for (count, rep) in l:
                            if rep in merge_rep_genes:
                                assert rep == toprep and merge_rep_genes[rep] == rep
                            merge_rep_genes[ rep ] = toprep


                for allele in alleles:
                    count_rep = get_mm1_rep_ignoring_allele( allele, organism )
                    if count_rep in merge_rep_genes:
                        count_rep = merge_rep_genes[ count_rep ]
                    allele2mm1_rep_gene_for_counting[ organism ][ allele] = count_rep
                    logger.debug('allele2mm1_rep_gene_for_counting: %s, %s, %s', organism, allele, count_rep)
    return allele2mm1_rep_gene_for_counting

allele2mm1_rep_gene_for_counting = get_allele2mm1_rep_gene_for_counting(all_genes = all_genes_default)

def get_mm1_rep_gene_for_counting( allele, organism ):
    return allele2mm1_rep_gene_for_counting[ organism ][ allele ]

def countreps_from_genes( genes, organism ):
    reps = set( ( allele2mm1_rep_gene_for_counting[ organism ][ x ] for x in genes ) )
    return reps


def assign_label_reps_and_colors_based_on_most_common_genes_in_repertoire( tcr_infos, organism ):
    ## assumes that each element of tcr_infos is a dictionary with fields that would have come from parse_tsv_line
    ## uses the *_countreps info that was filled in by read_pair_seqs.py
    ## the _label_rep* fields get over-written if they were present
    for segtype in basic.segtypes_lowercase:
        countreps_tag = segtype+'_countreps'
        rep_tag       = segtype+'_label_rep'
        color_tag     = segtype+'_label_rep_color' ## where we will store the rep info

        counts = {}
        for tcr_info in tcr_infos:
            try:
                reps = tcr_info[countreps_tag].split(';')
                for rep in reps:
                    counts[rep] = counts.get(rep, 0)+1
            except KeyError:
                pass # KMB added 5/13/2020 - this to try to permit beta only analysis

        newcounts = {}
        for tcr_info in tcr_infos:
            try:
                reps = tcr_info[countreps_tag].split(';')
                toprep = max( [ ( counts[x], x) for x in reps ] )[1]
                tcr_info[rep_tag] = toprep ## doesnt have allele info anymore
                newcounts[toprep] = newcounts.get(toprep, 0)+1
            except KeyError:
                pass # KMB added 5/13/2020 - this to try to permit beta only analysis

        l = sorted([(y, x) for x, y in newcounts.items()])
        l.reverse()
        rep_colors = dict( list(zip( [x[1] for x in l], html_colors.get_rank_colors_no_lights(len(l)) )) )
        for tcr_info in tcr_infos:
            try:
                tcr_info[ color_tag ] = rep_colors[ tcr_info[ rep_tag ] ]
            except KeyError:
                pass # KMB added 5/13/2020 - this to try to permit beta only analysis

    return ## we modified the elements of the tcr_infos list in place