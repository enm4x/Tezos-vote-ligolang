type storage is record [
  owner : address;
  status : bool;
  yes : nat;
  no : nat;
  voters : set(address);
  res : string
]

type parameter is
| Vote of nat
| Resetvote of unit
| Pausevote of string

type return is list (operation) * storage

// Function add_voters :
function add_voters_to_set (const store : storage) : storage is 
block { 
  store.voters := Set.add (Tezos.source, store.voters)
   } with store

// Function counter
function counter(const store : storage; const vote : nat) : storage is
block {
  if vote = 1n
    then store.yes := store.yes + 1n
  else if vote = 2n then
    store.no := store.no + 1n
  else skip;
} with store

function pause_vote (const stat : string; const store : storage) : storage is
 block { 
   if Tezos.source =/= store.owner
   then failwith("Access denied.")
   else if Tezos.source = store.owner and stat = "True"
      then 
        if stat = "True" then
          store.status := True
        else if stat = "False" then 
          store.status := False
        else skip;
    else skip;
    } with store

function vote (const vote : nat; const store : storage) : storage is
block {
    // check if the owner of the contract is trying to vote or
    // if someone who had already voted is trying to vote and
    // if the vote is open
    // if True -> failwith
  
    //Which one is the best between Tezos.source and sender ????
    if Tezos.source = store.owner
      then failwith ("Access denied, you're the owner of the smart-contracts.")
    else if store.voters contains Tezos.source
      then failwith ("Access denied, your vote is already registered.")
    else if store.status = False
      then failwith ("Access denied, the vote is currently disabled.")
    else skip;

    // define a const who takes the numbers of input inside the set of voters then 
    // check if it's equal to 10
    const cardinal : nat = Set.size(store.voters);
    // if the set size of voter is >= to 10 we show the winner
    if cardinal >= 10n 
      then 
        if store.yes > store.no 
          then failwith("Yes won")
        else failwith("No won")
    else if cardinal = 9n 
      then {
        store := add_voters_to_set(store);
        if vote = 1n
          then store.yes := store.yes + 1n
        else if vote = 2n then
          store.no := store.no + 1n
        else skip;
        // we reached 10th vote we can now block the vote
        // and get the result
        if store.yes > store.no 
          then store := store with record [
          status = False;
          res = "Yes won";
        ]
        else store := store with record [
          status = False;
          res = "No won";
        ] 
      } 
    else {
      store := add_voters_to_set(store);
      if vote = 1n
        then store.yes := store.yes + 1n
      else if vote = 2n then
        store.no := store.no + 1n
      else skip;
    }
} with store
   
function reset (const store : storage) : storage is
block {
    const empty_set : set (address) = Set.empty;
    // check if the owner of the contract is trying to reset -> if True then reset the value
    if Tezos.source = store.owner and store.status = False then 
        store := store with record [
          status = True;
          yes = 0n;
          no = 0n;
          voters = empty_set;
          res = "no result";
        ]
    else failwith("Acces denied.")
  
} with store

function main (const action : parameter; const store : storage): return is
block {
  const new_storage : storage = case action of
    | Vote (n) -> vote (n, store)
    | Resetvote -> reset (store)
    | Pausevote (n) -> pause_vote (n, store)
  end
} with ((nil : list (operation)), new_storage)
