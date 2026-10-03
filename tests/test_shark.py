import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "skills", "shark"))
import shark  # noqa: E402


class SharkTest(unittest.TestCase):
    def setUp(self):
        self.old = os.getcwd()
        self.tmp = tempfile.mkdtemp()
        os.chdir(self.tmp)
        os.makedirs(".shark")
        with open(".shark/pitch.md", "w") as f:
            f.write("A subscription box of local hot sauces\n\n$35 a month, 12 customers so far.\n")

    def tearDown(self):
        os.chdir(self.old)
        shutil.rmtree(self.tmp)

    def open_session(self, *extra):
        shark.main(["init", "--pitch-file", ".shark/pitch.md"] + list(extra))
        return shark.load_state()

    def write_all(self, state, phase, text):
        for j in shark.jobs(state, phase):
            with open(j["output"], "w") as f:
                f.write(text)

    def test_default_panel_is_the_core_five(self):
        state = self.open_session()
        self.assertEqual([i["name"] for i in state["panel"]],
                         [i["name"] for i in shark.load_investors()[:5]])

    def test_seeded_panel_is_distinct(self):
        state = self.open_session("--investors", "7", "--seed", "3")
        self.assertEqual(len({i["name"] for i in state["panel"]}), 7)

    def test_decide_brief_points_at_own_questions_and_answers(self):
        state = self.open_session()
        shark.main(["prompts", "decide"])
        j = shark.jobs(state, "decide")[1]
        text = open(j["brief"]).read()
        self.assertIn(os.path.abspath(os.path.join(state["dir"], "grill", "investor-2.md")), text)
        self.assertIn("answers/founder.md", text)
        self.assertIn("DECISION: IN or OUT", text)
        self.assertIn("For that reason, I'm out", text)
        self.assertIn(state["panel"][1]["signature"], text)

    def test_parse_decision(self):
        d = shark.parse_decision("DECISION: IN\nOFFER: $50,000 for 10%\nREASON: real buyers.\n"
                                 "WHAT WOULD CHANGE MY MIND: nothing")
        self.assertEqual((d["decision"], d["offer"]), ("IN", "$50,000 for 10%"))
        self.assertEqual(shark.parse_decision("**DECISION:** out\nOFFER: $1")["offer"], "none")
        self.assertIsNone(shark.parse_decision("NO DECISION"))

    def test_full_session_render(self):
        state = self.open_session()
        self.write_all(state, "grill", "BIGGEST WORRY: x\nQUESTIONS:\n1. a\n2. b\n3. c")
        self.write_all(state, "answers", "1. yes\nNOT ANSWERED: the founder needs to find out the shipping cost\n")
        decisions = ["IN", "OUT", "OUT", "IN", "NO DECISION"]
        for j, d in zip(shark.jobs(state, "decide"), decisions):
            with open(j["output"], "w") as f:
                f.write("NO DECISION" if d == "NO DECISION" else
                        "DECISION: %s\nOFFER: $20,000 for 15%%\nREASON: r\nWHAT WOULD CHANGE MY MIND: m\n" % d)
        t = shark.tally(state)
        self.assertEqual((t["in"], t["out"], t["panel"]), (2, 2, 5))
        text = shark.render(state)
        self.assertIn("# 2 of 5 sharks are in", text)
        self.assertIn("A subscription box of local hot sauces", text)
        self.assertIn("The founder needs to find out the shipping cost", text)
        second = state["panel"][1]["name"]
        self.assertIn("| %s | OUT | none |" % second, text)

    def test_no_deal_headline(self):
        state = self.open_session("--investors", "2", "--seed", "1")
        self.write_all(state, "decide", "DECISION: OUT\n")
        self.assertEqual(shark.headline(shark.tally(state)), "No deal: all 2 sharks are out")


if __name__ == "__main__":
    unittest.main()
