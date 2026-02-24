# Formal Model

## Tuple Definition

A Minimal Executable Digital Object (MEDO) is:

\[
O = (M, P, S_0, \tau)
\]

- \(M\): declared metadata
- \(P\): deterministic transition function
- \(S_0\): initial state
- \(\tau\): fixed drift threshold

State evolution:

\[
S_{n+1} = P(S_n)
\]

Deterministic object identity:

\[
I = H(M \| \tau \| S_0)
\]

## Drift and Gate

Deterministic drift metric:

\[
D(S_n, S_{n+1}) = \sum_{k \in K} |S_{n+1}[k] - S_n[k]|
\]

where \(K\) is the union of numeric keys in both states.

Gate condition:

\[
D(S_n, S_{n+1}) > \tau \Rightarrow \text{ConformanceFailure}
\]

## Checkpoint Chain

Let \(H(\cdot)\) be SHA256 and \(h_n = H(S_n)\):

\[
C_0 = H(I \| h_0)
\]

\[
C_n = H(C_{n-1} \| h_n)
\]

## Invariants

- Determinism: for fixed \(S_n\), \(P(S_n)\) is unique.
- Identity binding: \(I\) changes if \(M\), \(\tau\), or \(S_0\) changes.
- Structural drift: \(D\) is deterministic and non-negative.
- Gate safety: accepted transitions satisfy \(D \leq \tau\).
- Checkpoint consistency: \(C_0\) depends on \(I\) and \(S_0\); each \(C_n\) depends on \(C_{n-1}\) and \(S_n\).

## Causal Closure Criteria

A run is causally closed iff:

- Every accepted \(S_{n+1}\) equals \(P(S_n)\).
- Every accepted transition satisfies \(D \leq \tau\).
- Object identity \(I\) matches the declared \(M\), \(\tau\), and \(S_0\).
- The checkpoint chain is contiguous under the recurrence for all accepted states.

## Replay Verifiability Condition

Given an audit bundle, replay verifiability holds iff recomputation of:

1. object identity,
2. transition sequence,
3. drift sequence,
4. checkpoint chain,

yields the same final checkpoint hash as the bundle. Any mismatch implies tamper.
