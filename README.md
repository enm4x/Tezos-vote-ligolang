# How to Smart contracts in ligo

you will find : 

- A vote.ligo file in written with ligolang
- a list of all the commands you need in order to compile/test/deploy the given contracts

---

## Compile contract

input : 
```shell
$ ligo compile-contract vote.ligo main
```

output : 
```
michelson code
```



---

## compile storage 

```shell
$ ligo compile-storage vote.ligo main 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address)); res = "no result"]'
```



---

## Dry-run examples for every functions : 

### Vote function :



- Non-owner account : vote yes -> [ Success, +1 yes ]

```shell
$ ligo dry-run --source="tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN" vote.ligo main 'Vote(1n)' 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address)); res = "no result"]'
```



- Non-owner account : vote no -> [ Success, +1 no ]

```shell
$ ligo dry-run --source="tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN" vote.ligo main 'Vote(2n)' 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address)); res = "no result"]'
```



- Non-owner account tries to re-vote -> [ Fail ]

```shell
$ ligo dry-run --source="tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN" -- source="tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN" vote.ligo main 'Vote(1n)' 'record[status = True; yes = 0n; no = 0n; voters = set[("tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN" : address)]; res = "no result"]'
```



- Non-owner account : vote status disabled -> [ Fail ]

```shell
$ ligo dry-run --source="tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN" vote.ligo main 'Vote(1n)' 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address)); res = "no result"]'
```



- Owner account, vote with active vote -> [ Fail ] 

```shell
$ ligo dry-run --source="tz1Yzb54tZxbDDEePxKPPCCV4H2TiN667row" vote.ligo main 'Vote(1n)' 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address)); res = "no result"]'
```



- Owner account, vote with active vote -> [ Fail ]

```shell
$ ligo dry-run --source="tz1Yzb54tZxbDDEePxKPPCCV4H2TiN667row" vote.ligo main 'Vote(1n)' 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address)); res = "no result"]'
```





### Pause function : 



- Non-owner account -> [Fail]

```shell
$ ligo dry-run --source="tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN" vote.ligo main 'Break("True")' 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address)); res = "no result"]'
```



- Owner account, False to True-> [Succes]

```shell
$ ligo dry-run --source="tz1Yzb54tZxbDDEePxKPPCCV4H2TiN667row" vote.ligo main 'Break("True")' 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address)); res = "no result"]'
```



- Owner account, True to False -> [Succes]

```shell
$ ligo dry-run --source="tz1Yzb54tZxbDDEePxKPPCCV4H2TiN667row" vote.ligo main 'Break("False")' 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address)); res = "no result"]'
```





### Reset function : 



- Non-owner account-> [Fail]

```shell
$ ligo dry-run --source="tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN" vote.ligo main 'Reset' 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address)); res = "no result"]'
```



- Owner account, vote stopped -> [Succes]

```shell
$ ligo dry-run --source="tz1Yzb54tZxbDDEePxKPPCCV4H2TiN667row" vote.ligo main 'Reset' 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address)); res = "no result"]'
```



- Owner account, vote running -> [Fail]

```shell
$ ligo dry-run --source="tz1Yzb54tZxbDDEePxKPPCCV4H2TiN667row" vote.ligo main 'Reset' 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address)); res = "no result"]'
```
