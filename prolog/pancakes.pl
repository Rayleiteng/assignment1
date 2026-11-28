% The pancake problem in Prolog. A stack is a list of pancake sizes, the top first:
% [3, 1, 2] has pancake 3 on top. It is sorted when the sizes increase downwards.

% TODO: flip(K, Stack, Flipped): Flipped is Stack with its top K pancakes in reverse
%       order. Use length/2, append/3 and reverse/2.
flip(K, Xs, Ys) :-
    length(Head, K),
    append(Head, Tail, Xs),
    reverse(Head, RHead),
    append(RHead, Tail, Ys).

% TODO: move(Stack, flip(K), Next): Next is Stack after flipping its top K pancakes, for
%       every K from 2 to the number of pancakes. Hint: between/3.
move(Stack,flip(K),Next):-
    length(Stack, N),
    between(2, N, K),
    flip(K, Stack, Next).

% sorted_stack(Stack): the sizes increase from the top down.
sorted_stack(Stack) :-
    msort(Stack, Stack).

% TODO: solve(Stack, Moves): Moves is a list of moves that sorts Stack (depth-first).
solve(Stack, []) :-
    sorted_stack(Stack).

solve(Stack, [Move|Moves]) :-
    move(Stack, Move, Next),
    solve(Next, Moves).
% TODO: solve_id(Stack, Moves): like solve, but trying shorter lists of moves first
%       (iterative deepening).
solve_id(Stack, Moves):-
    length(Moves, _),
    solve(Stack, Moves).

% TODO: gaps(Stack, G): G is the number of gaps in Stack, with the plate counting as a
%       pancake of size N + 1 under the stack: the gap heuristic of part B.
adj(X,Y) :-
    X is Y + 1.
adj(X,Y) :-
    Y is X + 1.
pair_gap(X, Y, 0) :-
    adj(X, Y).
pair_gap(X, Y, 1) :-
    \+ adj(X, Y).

nadjCount([_], 0).
nadjCount([X, Y|Xs], C):-
    pair_gap(X, Y, A),
    nadjCount([Y|Xs], B),
    C is A + B.

gaps(Stack, G) :-
    length(Stack, K),
    P is K + 1,
    append(Stack, [P], Xs),
    nadjCount(Xs, G).
