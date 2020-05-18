from os.path import dirname, join
from unittest import TestCase
from pytezos import ContractInterface, MichelsonRuntimeError

# run this test with :
# pytest test.py

class TestContractTest(TestCase):

    @classmethod
    def setUpClass(cls):
        project_dir = dirname(dirname(__file__))
        print("projectdir", project_dir)
        cls.test = ContractInterface.create_from(
            join(project_dir, 'src/vote.tz'))

##########################################################
#############   Vote entrypoint tests  #############

    def test_vote_as_user_yes(self):
        alice = "tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN"
        res = 1
        result = self.test.vote(
            1
        ).result(
            storage={
                "status": True,
                "yes": 0,
                "no": 0,
                "voters": set(),
                "res" : "no result"
            },
            source=alice
        )
        self.assertEqual(res, result.storage["yes"])

    def test_vote_as_user_no(self):
        alice = "tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN"
        res = 1
        result = self.test.vote(
            2
        ).result(
            storage={
                "status": True,
                "yes": 0,
                "no": 0,
                "voters": set(),
                "res" : "no result"
            },
            source=alice
        )
        self.assertEqual(res, result.storage["no"])

    def test_vote_fail_because_owner(self):
        owner = "tz1Yzb54tZxbDDEePxKPPCCV4H2TiN667row"
        with self.assertRaises(MichelsonRuntimeError):
            self.test.vote(
                1
            ).result(
                storage={
                    "status": True,
                    "yes": 0,
                    "no": 0,
                    "voters": set(),
                    "res" : "no result"
                },
                source=owner
            )

    def test_vote_fail_because_voting_disabled(self):
        alice = "tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN"
        with self.assertRaises(MichelsonRuntimeError):
            self.test.vote(1).result(
                storage={
                    "status": False,
                    "yes": 0,
                    "no": 0,
                    "voters": set(),
                    "res" : "no result"
                },
                source=alice
            )
#--------------------------------------------------------#
##########################################################



##########################################################
#############   Reset-vote entrypoint tests  #############

    def test_reset_as_owner_voting_disabled(self):
        owner = "tz1Yzb54tZxbDDEePxKPPCCV4H2TiN667row"
        result = self.test.resetvote(0).result(
            storage={
                "status": False,
                "yes": 4,
                "no": 6,
                "voters": set(),
                "res" : "no result"
            },
            source=owner
        )
        self.assertEqual(0, result.storage["yes"])

    def test_reset_as_owner_voting_enabled(self):
        owner = "tz1Yzb54tZxbDDEePxKPPCCV4H2TiN667row"
        with self.assertRaises(MichelsonRuntimeError):
            self.test.resetvote(0).result(
                storage={
                    "status": True,
                    "yes": 0,
                    "no": 0,
                    "voters": set(),
                    "res" : "no result"
                },
                source=owner
            )

    def test_reset_as_alice(self):
        alice = "tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN"
        with self.assertRaises(MichelsonRuntimeError):
            self.test.resetvote(0).result(
                storage={
                    "status": True,
                    "yes": 0,
                    "no": 0,
                    "voters": set(),
                    "res" : "no result"
                },
                source=alice
            )
#--------------------------------------------------------#
##########################################################


##########################################################
#############   Pause-vote entrypoint tests  #############

    def test_pause_as_owner_T2F(self):
        owner = "tz1Yzb54tZxbDDEePxKPPCCV4H2TiN667row"
        res = False
        result = self.test.pausevote("False").result(
                storage={
                    "status":True,
                    "yes":0,
                    "no":0,
                    "voters":set(),
                    "res" : "no result"
                },
                source=owner
        )
        self.assertEqual(res, result.storage["yes"])
    
    def test_pause_as_owner_F2T(self):
        owner = "tz1Yzb54tZxbDDEePxKPPCCV4H2TiN667row"
        res = True
        result = self.test.pausevote("True").result(
                storage={
                    "status":False,
                    "yes":0,
                    "no":0,
                    "voters":set(),
                    "res" : "no result"
                },
                source=owner
        )
        self.assertEqual(res, result.storage["status"])

    def test_pause_as_user(self):
        alice = "tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN"
        with self.assertRaises(MichelsonRuntimeError):
            self.test.pausevote("True").result(
                    storage={
                        "status":False,
                        "yes":2,
                        "no":1,
                        "voters":set(),
                        "res" : "no result"
                    },
                    source=alice
            )
