import hashlib
from decimal import Decimal


class Transaction(object):
    """A single instance of the changing hands of money."""

    def __init__(self,
                 name,
                 amount,
                 occurred_at,
                 source):
        """
        Args:
            name (str): the name of the transaction
            amount (str or Number): the amount the transaction was for
            occurred_at (datetime): the time at which the transaction
                occurred
            source (str): the name of the source
        """
        self.name = name
        self.amount = Decimal(amount).quantize(Decimal("0.01"))
        self.occurred_at = occurred_at
        self.source = source

    @property
    def as_dict(self):
        """Return the identifying values of this Transaction in a
        dictionary."""
        props = dict(self.__dict__)
        props['id'] = self.id
        props['amount'] = str(props.pop('amount'))

        return props

    @property
    def id(self):
        """Return a unique identifier based on this transaction's values."""
        dict_str = repr(sorted(self.__dict__.items()))

        return hashlib.sha224(dict_str).hexdigest()

    def __repr__(self):
        return ("<Transaction name='%s' amount='%s' occurred_at='%s'>"
                % (self.name, "$%s" % str(self.amount), str(self.occurred_at)))

    __str__ = __repr__

