package main

import "fmt"

type state struct {
    m, c, boat byte
    parent *state
}

func (s state) String() string {
    return fmt.Sprintf("<%d, %d, %d>", s.m, s.c, s.boat)
}

func (s state) Equals(other state) bool {
    return s.String() == other.String()
}

func (s state) Moves() []state {
    moves := []state{}
    possibles := []state{
        state{1,0,1, nil},
        state{2,0,1, nil},
        state{0,1,1, nil},
        state{0,2,1, nil},
        state{1,1,1, nil}}
    for _, p := range possibles {
        move := s.Transition(p)
        if move.IsValid() {
            moves = append(moves, move)
        }
    }
    return moves

}

func (s state) IsValid() bool {
    return (s.m >= 0 && s.c >= 0 && 3-s.m >= 0 && 3-s.c >=0) &&
           (s.m == 0 || s.m >= s.c) &&
           (3-s.m == 0 || 3-s.m >= 3-s.c) &&
           (s.m <= 3 && s.c <= 3)
}

func (s state) Transition(move state) state {
    if s.boat == 1 {
        return state{s.m - move.m, s.c - move.c, 0, &s}
    } else {
        return state{s.m + move.m, s.c + move.c, 1, &s}
    }
}

func (s state) Difference() state {
    if s.parent == nil { return state{} }
    if s.boat == 1 {
        return state{s.m - s.parent.m, s.c - s.parent.c, 1, nil}
    } else {
        return state{s.parent.m - s.m, s.parent.c - s.c, 1, nil}
    }
}

func (s state) Solve() state {
    goal := state{0, 0, 0, nil}
    examined := make(map[string]bool, 32)
    queue := s.Moves()
    var node state
    for {
        node, queue = queue[0], queue[1:]
        if node.Equals(goal) { return node }
        if _, ok := examined[node.String()]; ok { continue }
        examined[node.String()] = true
        for _, move := range node.Moves() {
            queue = append(queue, move)
        }

    }
}

func main() {
    //tests()
    start := state{3, 3, 1, nil}
    goal := start.Solve()
    moves := []state{}
    for {
        if goal.parent == nil { break }
        moves = append(moves, goal.Difference())
        goal = *goal.parent
    }
    for i := len(moves)-1; i >= 0; i-- {
        fmt.Println(moves[i])
    }
}

func tests() {
    s := state{3,3,1,nil}; if !s.IsValid() { panic("Failure") }
    s = state{2,2,0,nil}; if !s.IsValid() { panic("Failure") }
    s2 := state{2,2,0,nil}; if !s2.Equals(s) { panic("Failure") }
    s3 := state{1,2,0,nil}; if s3.Equals(s) { panic("Failure") }
}

/*

Things I had issues with:

- No built in vector; used slices instead but had to implement own "vector math"
- No built in queue; seen priority queue with containers/heap but unsure of
  order when priorties are the same. Didn't test, but documentation could have explained
- Lots of missing datastructurese (the general of above)
- (wrong, see below) slice = slice[1:] didn't do what I expect, making this pattern difficult:
  queue = []int{0,1,2,3}
  head, queue = queue[0],queue[1:]
  queue[0] == 0 // I expected it to be 1 with reassignment
- slice = slice[1:] DOES do what I expect. My issue was with scoping
  I was doing slice := slice[1:] within the loop, then the next iteration was using
  the parent scope slice, not the "new" one that was local.
- No operator overloading, meaning you have to define your own Equals function and
  identity method
- nil members got me for awhile until I realised I just had to use a pointer
- I dont like that append is a builtin and not a function of the slice type
- Couldn't figure out how to create static members to avoid re-allocating possibilities

Things I liked:

- Concise, with fairly good documentation
- Feels like writing python
- slices are nice (but append(slice, otherslice) is missing)
- really easy to install and run
- great compiler errors and messages
- the idea of interfaces is good, but no need for them here
- same goes for channels and go routines


*/