#
# Debugging code:
#
import algebra
import tools
tools.cls()
expr = algebra.Sum([1, algebra.Sum([2, 3])])
simplified = expr.simplify()
assert (list(simplified) == [1,2,3]), "Sum([1, Sum([2, 3])]) :: Unexpected simplified result."

expr2 = algebra.Product([algebra.Product(['a', 'b']),'c'])
simplified = expr2.simplify()
assert (list(simplified) == ['c','a','b']), "Product([algebra.Product(['a', 'b']),'c']) :: Unexpected simplified result."

# a . (c + d)
#Representation:
#Product([a, Sum([c,d])])
expr3 = algebra.Product(['a', algebra.Sum(['c','d'])])
result = expr3.simplify()
print( result )

# a . (c + d) + b . ( c + d)
# a.c + a.d + b.c + b.d
expr3 = algebra.Sum([algebra.Product(['a', algebra.Sum(['c','d'])]), algebra.Product(['b', algebra.Sum(['c','d'])])])
result = expr3.simplify()
print( result )

#(a + b) . (c + d)
#Representation:
# Product([Sum([a,b]), Sum([c,d])])
# a . (c + d) + b . (c + d)
#Representation:
# Sum([Product([a, Sum([c,d])]), Product([b, Sum([c,d])])])
# Sum([Product(['a', 'c']), Product(['a', 'd']), Product(['b', 'c']), Product(['b', 'd'])])
expr3 = algebra.Product([algebra.Sum(['a','b']), algebra.Sum(['c','d'])])
result = expr3.simplify()
print( result )

#1) (2 * (x + 1) * (y + 3))
#    (2 * x + 2 * 1) * (y + 3)
#2) ((2 * x * y) + (2 * x * 3) + (2 * 1 * y) + (2 * 1 * 3))
#Representation:
#1) Product([2, Sum(['x', 1]), Sum(['y', 3])])
#2) Sum([Product([2, 'x', 'y'], Product([2, 'x', 3]), Product([2, 1, 'y']), Product([2, 1, 3]))])
#Simplified:
#2) Sum([Product([2, 'x', 'y'], Product([2, 'x', 3]), Product([2, 'y']), Product([2, 3]))])
expr3 = algebra.Product([2, algebra.Sum(['x', 1]), algebra.Sum(['y', 3])])
result = expr3.simplify()
print( result )