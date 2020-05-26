""" Example pylib functions"""


def row_generator(resource, doc, env, *args, **kwargs):
    """ An example row generator function.

    Reference this function in a Metatab file as the value of a Datafile:

            Datafile: python:pylib#row_generator

    The function must yield rows, with the first being headers, and subsequenct rows being data.

    :param resource: The Datafile term being processed
    :param doc: The Metatab document that contains the term being processed
    :param args: Positional arguments passed to the generator
    :param kwargs: Keyword arguments passed to the generator
    :return:


    The env argument is a dict with these environmental keys:

    * CACHE_DIR
    * RESOURCE_NAME
    * RESOLVED_URL
    * WORKING_DIR
    * METATAB_DOC
    * METATAB_WORKING_DIR
    * METATAB_PACKAGE

    It also contains key/value pairs for all of the properties of the resource.

    """
    
    from operator import itemgetter
    from geoid.acs import Tract
    
    st = resource.schema_term
    
    header = []
    columns = []
    
    for c in st.children:
        
        header.append(c.name)
        if c.get('col_pos'):
            columns.append(int(c.col_pos)-1)
        
        
    yield header
    
    ig = itemgetter(*columns)
    


    for ref in doc.references():
        for row in ref:
            yield (Tract(row[2], row[3], row[4]),)+ig(row)
            
        


def example_transform(v, row, row_n, i_s, i_d, header_s, header_d, scratch, errors, accumulator):
    """ An example column transform.

    This is an example of a column transform with all of the arguments listed. An real transform
    can omit any ( or all ) of these, and can supply them in any order; the calling code will inspect the
    signature.

    When the function is listed as a transform for a column, it is called for every row of data.

    :param v: The current value of the column
    :param row: A RowProxy object for the whiole row.
    :param row_n: The current row number.
    :param i_s: The numeric index of the source column
    :param i_d: The numeric index for the destination column
    :param header_s: The name of the source column
    :param header_d: The name of the destination column
    :param scratch: A dict that can be used for storing any values. Persists between rows.
    :param errors: A dict used to store error messages. Persists for all columns in a row, but not between rows.
    :param accumulator: A dict for use in accumulating values, such as computing aggregates.
    :return: The final value to be supplied for the column.
    """

    return str(v) + '-foo'


def custom_update(doc, args):
    """Custom update function, run with `mp update -U`

    The args argument will recieve any remainder arguments from the call, for instance

        mp update -U -- --foo bar

    """

    doc.reference('source')

    doc.write()
