# Section 3: Algebraic simplification

# This code implements a simple computer algebra system, which takes in an
# expression made of nested sums and products, and simplifies it into a
# single sum of products. The goal is described in more detail in the
# problem set writeup.

# Much of this code is already implemented. We provide you with a
# representation for sums and products, and a top-level simplify() function
# which applies the associative law in obvious cases. For example, it
# turns both (a + (b + c)) and ((a + b) + c) into the simpler expression
# (a + b + c).

# However, the code has a gap in it: it cannot simplify expressions that are
# multiplied together. In interesting cases of this, you will need to apply
# the distributive law.

# Your goal is to fill in the do_multiply() function so that multiplication
# can be simplified as intended. 

# Testing will be mathematical:  If you return a flat list that
# evaluates to the same value as the original expression, you will
# get full credit.


# We've already defined the data structures that you'll use to symbolically
# represent these expressions, as two classes called Sum and Product,
# defined below. These classes both descend from the abstract Expression class.
#
# The top level function that will be called is the .simplify() method of an
# Expression.
#
# >>> expr = Sum([1, Sum([2, 3])])
# >>> expr.simplify()
# Sum([1, 2, 3])


### Expression classes _____________________________________________________

# Expressions will be represented as "Sum()" and "Product()" objects.
# These objects can be treated just like lists (they inherit from the
# "list" class), but you can test for their type using the "isinstance()"
# function.  For example:
#
# >>> isinstance(Sum([1,2,3]), Sum)
# True
# >>> isinstance(Product([1,2,3]), Product)
# True
# >>> isinstance(Sum([1,2,3]), Expression) # Sums and Products are both Expressions
# True

class Expression:
    "This abstract class does nothing on its own."
    pass

class Sum(list, Expression):
    """
    A Sum acts just like a list in almost all regards, except that this code
    can tell it is a Sum using isinstance(), and we add useful methods
    such as simplify().

    Because of this:
      * You can index into a sum like a list, as in term = sum[0].
      * You can iterate over a sum with "for term in sum:".
      * You can convert a sum to an ordinary list with the list() constructor:
         the_list = list(the_sum)
      * You can convert an ordinary list to a sum with the Sum() constructor:
         the_sum = Sum(the_list)
    """
    def __repr__(self):
        return "Sum(%s)" % list.__repr__(self)
    
    def simplify(self):
        """
        This is the starting point for the task you need to perform. It
        removes unnecessary nesting and applies the associative law.
        """
        terms = self.flatten()
        if len(terms) == 1:
            return simplify_if_possible(terms[0])
        else:
            return Sum([simplify_if_possible(term) for term in terms]).flatten()

    def flatten(self):
        """Simplifies nested sums."""
        terms = []
        for term in self:
            if isinstance(term, Sum):
                terms += list(term)
            else:
                terms.append(term)
        return Sum(terms)


class Product(list, Expression):
    """
    See the documentation above for Sum. A Product acts almost exactly
    like a list, and can be converted to and from a list when necessary.
    """
    def __repr__(self):
        return "Product(%s)" % list.__repr__(self)
    
    def simplify(self):
        """
        To simplify a product, we need to multiply all its factors together
        while taking things like the distributive law into account. This
        method calls multiply() repeatedly, leading to the code you will
        need to write.
        """
        factors = []
        for factor in self:
            if isinstance(factor, Product):
                factors += list(factor)
            else:
                factors.append(factor)
        result = Product([1])
        for factor in factors:
            result = multiply(result, simplify_if_possible(factor))
        return result.flatten()

    def flatten(self):
        """Simplifies nested products."""
        factors = []
        for factor in self:
            if isinstance(factor, Product):
                factors += list(factor)
            else:
                factors.append(factor)
        return Product(factors)

def simplify_if_possible(expr):
    """
    A helper function that guards against trying to simplify a non-Expression.
    """
    if isinstance(expr, Expression):
        return expr.simplify()
    else:
        return expr

    # You may find the following helper functions to be useful.
    # "multiply" is provided for you; but you will need to write "do_multiply"
    # if you would like to use it.

def multiply(expr1, expr2):
    """
    This function makes sure that its arguments are represented as either a
    Sum or a Product, and then passes the hard work onto do_multiply.
    """
    # Simple expressions that are not sums or products can be handled
    # in exactly the same way as products -- they just have one thing in them.
    if not isinstance(expr1, Expression): expr1 = Product([expr1])
    if not isinstance(expr2, Expression): expr2 = Product([expr2])
    return do_multiply(expr1, expr2)
    
def do_multiply(expr1, expr2):
    """
    You have two Expressions, and you need to make a simplified expression
    representing their product. They are guaranteed to be of type Expression
    -- that is, either Sums or Products -- by the multiply() function that
    calls this one.
    So, you have four cases to deal with:
    * expr1 is a Sum, and expr2 is a Sum
    * expr1 is a Sum, and expr2 is a Product
    * expr1 is a Product, and expr2 is a Sum
    * expr1 is a Product, and expr2 is a Product
    You need to create Sums or Products that represent what you get by
    applying the algebraic rules of multiplication to these expressions,
    and simplifying.
    Look above for details on the Sum and Product classes. The Python operator
    '*' will not help you.
    
    Author: MELO CAVALCANTE, Roberto.
    Copyright: Copyright 2020, Roberto Melo Cavalcante.
    Date: April 18th, 2020.
    """
    if( isinstance(expr1, Sum) and isinstance(expr2, Sum)):
        e1_list = list(expr1)
        e2_list = list(expr2)
        e1_len = len(e1_list)
        e2_len = len(e2_list)
        if(e1_len == 1 or e2_len == 1):
            if(e1_len == 1 and e2_len == 1):
                p = Product([e1_list[0], e2_list[0]])
                return p;
            if(e1_len == 1):
                # a . (c + d)
                # Product([a, Sum([c,d])])
                # a.c + a.d
                # Sum( [ Product([a,c]), Product([a,d]) ] )
                sum_list = []
                for e2_elem in e2_list:
                    sum_list.extend(Product([e1_list[0], e2_elem]))
                s = Sum(sum_list)
                return s
            if(e2_len == 1):
                p = Product(expr2, expr1)
                return p.multiply()
        else:
            #(a + b) . (c + d)
            #Representation:
            # Product([Sum([a,b]), Sum([c,d])])
            # a . (c + d) + b . (c + d)
            #Representation:
            # Sum([Product([a, Sum([c,d])]), Product([b, Sum([c,d])])])
            sum_list=Sum()
            for e1_elem in e1_list:
                pp = Product([e1_elem, expr2])
                pp = pp.simplify()
                sum_list.append(pp)
            return sum_list

    # Replace this with your solution.
    if( isinstance(expr1, Product) and isinstance(expr2, Product)):
        if((0 in expr1) or (0 in expr2)):
            return Product([0])
        if(expr1[0]==0 or expr2[0]==0):
            return Product([0])
        p1_len = len(expr1)
        p2_len = len(expr2)
        if(p1_len == 1 and p2_len == 1):
            if(expr1[0] == 1):
                return expr2
            if(expr2[0] == 1):
                return expr1
            p3list = list([v for v in expr1 if v != 1])
            p3list.extend([v for v in expr2 if v != 1])
            if(len(p3list) == 0): # all elements on both expressions were 1.
                return Product([1])
            return Product(p3list)

        if(p1_len==1):
            p3list = []
            p3list = list(expr1)
            p3list.extend(list(expr2))
            while(1 in p3list):
                p3list.remove(1)
            
            if(len(p3list) == 0): # all elements on both expressions were 1.
                return Product([1])
            p3 = Product(p3list)
            return p3
        if(p2_len==1):
            return do_multiply(expr2, expr1)
        #
        # (a.b).(c.d)
        # Product([Product([a,b]), Product([c,d])])
        # a.b.c.d
        # Product([a,b,c,d])
        #
        p1 = list(expr1)
        p2 = list(expr2)
        p1.extend(p2)
        if(0 in p1):
            return Product([0])
        return Product(p1)
    
    if(isinstance(expr1, Product) and isinstance(expr2, Sum)):
        # a . (c + d):
        # Product([a, Sum([c,d])])
        # a.c + a.d
        # Sum( [ Product([a,c]), Product([a,d]) ] )
        #
        sum = Sum()
        for ex2 in expr2:
            exprM = Product()
            exprM.extend(expr1)
            if(ex2!=1):
                exprM.append(ex2)
            sum.append(exprM)
        return sum 
    
    if( isinstance(expr1, Sum) and isinstance(expr2, Product)):
        return do_multiply(expr2, expr1)
    