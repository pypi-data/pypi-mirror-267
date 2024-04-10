# For relative imports to work in Python >=3.6
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

class FancySchmancyTestsplit():
    """
    ## like a testsplit, but fancy and also schmancy\n
    a testplit per label category, to ensure that every category is present

    ----
    ### Parameters

    data : DataFrame
        data to be split, containing X and y
    label_column : str
        name of the label(y)
    test_split : float
        percent of test data
    seed : int
        Seed or Random State
    ----
    ### Returns

    test and train data : tuple of X_train, X_test, y_train and y_test
        In this order.

    ----
    ### Notes

    Data has to be DataFrame, other Iterables won't work.

    ----
    ### See Also

    sklearn.model_selection.train_test_split

    ----
    ### Examples

    Assume the following DataFrame:
    >>> df = DataFrame(data= {"Column A":[10, 14, 12, 13, 9, 5, 13, 16, 18, 4, 12],
    >>> "Column B": ["Cat1", "Cat1", "Cat2", "Cat2", "Cat2", "Cat2", "Cat2", "Cat2", "Cat2", "Cat2", "Cat2"]})
    >>> print(df)

        | Column A | Column B
    :- | -: | -:
    0 | 10 | Cat1
    1 | 14 | Cat1
    2 | 12 | Cat2
    3 | 13 | Cat2
    4 | 9 | Cat2
    5 | 5 | Cat2
    6 | 13 | Cat2
    7 | 16 | Cat2
    8 | 18 | Cat2
    9 | 4 | Cat2
    10 | 12 | Cat2

    If we assume further that Column B contains the label categories, we'd
    run the risk of eliminating Cat1 by doing a train test split at 50%.

    So, to preserve every existing category, the split will instead be made
    on every single subset of categories.

    As an example for Cat1:
    >>> subset = df[df["Column B"] == "Cat1"]
    >>> X = subset.drop("Column B", axis= 1)
    >>> y = subset["Column B"]
    >>> if isinstance(y, Series): y = DataFrame(y)
    >>> X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size = 0.5, random_state = 42)
    >>> print(y_tr)

        | Column B
    :- | -:
    0 | Cat1

    If this was done for "Cat1" and "Cat2", it would look like this:

    || Column B
    :- | -:
    0 | Cat1
    4 | Cat2
    6 | Cat2
    5 | Cat2
    8 | Cat2

    To shorten the process, the method fancy_schmancy_testsplit can be used in this way:

    >>> from FancySchmancyTestsplit.fst import fancy_schmancy_testsplit
    >>> from pandas import DataFrame
    >>> df = DataFrame(data= {"Column A":[10, 14, 12, 13, 9, 5, 13, 16, 18, 4, 12],
    >>> "Column B": ["Cat1", "Cat1", "Cat2", "Cat2", "Cat2", "Cat2", "Cat2", "Cat2", "Cat2", "Cat2", "Cat2"]})
    >>> X_train, X_test, y_train, y_test = \\
    >>>     fancy_schmancy_testsplit(data= df,
    >>>                             label_column= "Column B",
    >>>                             test_split= 0.5,
    >>>                             seed= 42
    >>>                             )
    >>> print(y_train)

    || Column B
    :- | -:
    0 | Cat1
    4 | Cat2
    6 | Cat2
    5 | Cat2
    8 | Cat2
    """
    def __init__(self) -> None:
        pass
    pass