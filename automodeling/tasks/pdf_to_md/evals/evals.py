from automodeling.tasks.pdf_to_md.utils import remove_page_nums
from automodeling.tasks.utils import print_differences


def eval_footnotes(dataset):
    """
    Check that headers and footers are correctly removed
    """
    pass


def eval_bold(dataset):
    """
    Ensure bold text is correctly handled
    """
    pass


def eval_titles(dataset):
    """
    Ensure titles are correctly converted with correct level
    """
    pass


def eval_page_merging(dataset):
    """
    Ensure pages are correctly merged together
    """
    pass


def eval_table_of_contents(dataset):
    """
    Check if ToC is in correct format
    """
    pass


def eval_page_nr_removed(dataset):
    """
    Check that page numbers are removed from the text
    """
    num_correct = 0
    for i, (md, ref_md) in enumerate(dataset):
        new_md = remove_page_nums(md)
        if new_md == ref_md:
            num_correct += 1
        else:
            print(f"Incorrect MD {i}")
            print_differences(new_md, ref_md)

    accuracy = float(num_correct) / len(dataset)
    print(f"Evaluation of page number removed accuracy: {accuracy}")
    return accuracy
