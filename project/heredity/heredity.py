import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    p = 1
    for person in people.keys():
        mother = people[person]["mother"]
        father = people[person]["father"]
        mother_gene_num = gn(mother, one_gene, two_genes)
        father_gene_num = gn(father, one_gene, two_genes)

        gene_num = 0

        # helper function
        
        
        if person in one_gene:
            p *= one(mother, father, mother_gene_num, father_gene_num)
            gene_num = 1
        elif person in two_genes:
            p *= two(mother, father, mother_gene_num, father_gene_num)
            gene_num = 2
        else:   
            p *= no_genes(mother, father, mother_gene_num, father_gene_num)
            gene_num = 0

        if person in have_trait:
            p *= PROBS["trait"][gene_num][True]
        else:       
            p *= PROBS["trait"][gene_num][False]

    return p

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for i in probabilities.keys():
        if i in one_gene:
            probabilities[i]["gene"][1] += p

        elif i in two_genes:
            probabilities[i]["gene"][2] += p

        else:
             probabilities[i]["gene"][0] += p

    for x in probabilities.keys():
        if x in have_trait:
            probabilities[x]["trait"][True] += p
        else:
            probabilities[x]["trait"][False] += p    

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for i in probabilities.keys():
        true = probabilities[i]["trait"][True]
        false = probabilities[i]["trait"][False]
        if true + false != 1:
            probabilities[i]["trait"][False] = false / (true + false)
            probabilities[i]["trait"][True] = 1 - false
        zero = probabilities[i]["gene"][0]
        one = probabilities[i]["gene"][1]
        two = probabilities[i]["gene"][2] 
        if zero + one + two != 1:
            probabilities[i]["gene"][0] = zero / (zero + one + two)
            probabilities[i]["gene"][1]= one / (zero + one + two)
            probabilities[i]["gene"][2]= 1 - one - zero    
        
# Helper function
def not_deliver(num):
    if num == 0:
        return 1 - PROBS["mutation"]
    elif num == 1:
        return 0.5
    else:
        return PROBS["mutation"] 

def deliver(num):
    if num == 0:
        return PROBS["mutation"] 
    elif num == 1:
        return 0.5
    else:
        return 1 - PROBS["mutation"]        

def no_genes(mother, father, mg, fg):
    if mother == None and father == None:
        return PROBS["gene"][0]
    else:
        return not_deliver(mg) * not_deliver(fg)   
    

def one(mother,father, mg, fg):
    if mother == None and father == None:
        return PROBS["gene"][1]
    else:
        return deliver(mg) * not_deliver(fg) + not_deliver(mg) * deliver(fg)
        

def two(mother,father, mg, fg):
    if mother == None and father == None:
        return PROBS["gene"][2]
    else:
        
        return deliver(mg) * deliver(fg)   

def gn(person, one_gene, two_genes):
    if person == None:
        return None
    elif person in one_gene:
        return 1
    elif person in two_genes:
        return 2
    else:
        return 0        

if __name__ == "__main__":
    main()

