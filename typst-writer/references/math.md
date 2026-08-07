# Native Typst mathematics

Write Typst math, not LaTeX. Keep semantic source readable and compile examples
before relying on unfamiliar symbols.

## Mode and grouping

```typst
Inline: $f(x) = x^2$.

$
  integral_0^1 x^2 dif x = 1/3
$
```

Use parentheses for multi-token subscripts and superscripts:

```typst
$ a_(n+1), x^(k+1), e^(-x^2), hat(theta)_(t+1) $
```

Use strings for words and named objects inside math:

```typst
$ "PALINDROMES" subset.eq overline("ODD-ODD") $
$ op("rank")(A) = n $
```

## Logic and sets

```typst
$ forall x in A, exists y in B: P(x, y) $
$ P => Q $
$ P <=> Q $
$ not P $
$ P and Q $
$ P or Q $
$ A subset.eq B $
$ x in A $
$ Sigma^* $
$ overline(A) $
```

Prefer tokens such as `forall`, `exists`, `=>`, `<=>`, `not`, `and`, `or`,
`in`, and `subset.eq` over pasted Unicode glyphs.

## Number systems and styled symbols

```typst
$ NN, ZZ, QQ, RR, CC $
$ cal(F), bb(R), bold(x), upright(d) $
```

Use `cal(...)`, `bb(...)`, and `bold(...)` for explicit styling when a built-in
symbol is not available.

## Fractions, roots, sums, and limits

```typst
$ frac(a + b, c) $
$ sqrt(x), root(3, x) $
$ sum_(i=1)^n i = n(n+1)/2 $
$ product_(i=1)^n a_i $
$ lim_(h arrow.r 0) frac(f(x+h)-f(x), h) $
$ integral_a^b f(x) dif x $
```

Use `frac(...)` when grouping would otherwise be ambiguous. Use `dif` for the
differential.

## Linear algebra

```typst
$
  A = mat(
    1, 2;
    3, 4;
  )
$

$ A x = b $
$ norm(x)_2 $
$ lr(chevron.l x, y chevron.r) $
$ A v_i = lambda_i v_i $
$ J_F(x) h $
```

## Cases and aligned derivations

```typst
$
  f(x) = cases(
    x^2 & "if" x >= 0,
    -x & "otherwise",
  )
$
```

```typst
$
  f(x+h) - f(x) &= f'(x)h + o(h) \
  frac(f(x+h)-f(x), h) &= f'(x) + frac(o(h), h)
$
```

Use alignment points (`&`) and math line breaks (`\\`) for derivations and
several related blanks instead of forcing a long expression onto one line.

## Numerical analysis

```typst
$ e_"abs" = abs(q - hat(q)) $
$ e_"rel" = frac(abs(q - hat(q)), abs(q)) $
$ r(h) = O(h^p) $
$ r(h) = o(h) $
$ h arrow.r 0 $
```

Do not treat big-O notation as an algebraic value that can be cancelled.

## Probability and machine learning

```typst
$ bb(E)_(x tilde p(x))[f(x)] $
$ p(theta | x) $
$ hat(R)(theta) = 1/n sum_(i=1)^n "loss"(f_theta(x_i), y_i) $
$ theta_(t+1) = theta_t - eta nabla L(theta_t) $
```

When a specialized operator is unavailable or unclear, use `op("name")` or a
quoted string rather than inventing a LaTeX command.

## Common LaTeX translations

| LaTeX habit | Typst |
|---|---|
| `\mathbb{R}` | `bb(R)` or `RR` |
| `\mathcal{F}` | `cal(F)` |
| `\operatorname{rank}` | `op("rank")` |
| `\text{loss}` | `"loss"` |
| `\frac{a}{b}` | `frac(a, b)` or `a/b` |
| `\subseteq` | `subset.eq` |
| `\infty` | `infinity` |
| `\to` | `arrow.r` |
| `\sum_{i=1}^n` | `sum_(i=1)^n` |

Do not paste a LaTeX expression into Typst and repair it token by token when a
native rewrite is clearer.
