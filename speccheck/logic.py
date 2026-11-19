"""logic.py: the bridge between formal.json and the Z3 solver.

Everything Z3-specific that the other modules need lives here:

    Vocabulary   turns the "symbols" list of formal.json into Z3 variables,
                 parses SMT-LIB text into Z3 formulas, and asks Z3 questions
                 (is this possible? does this follow? do these two mean the same?).
    Rule         one compiled requirement: antecedent => consequent.

Nothing in this file knows about any particular spec. The symbols and the
formulas all come from data.
"""

import re
from dataclasses import dataclass

import z3

# A symbol name must be a plain identifier. This keeps LLM-invented names from
# clashing with SMT-LIB syntax or with the internal names used in checks.py.
_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

# Z3 gives up on a single question after this many milliseconds. Specs produce
# tiny problems, so a timeout only happens if the LLM wrote something exotic.
SOLVER_TIMEOUT_MS = 5000


def describe(witness: dict, descriptions: dict) -> str:
    """A witness (symbol -> value) as text, one fact per line.

    Used wherever a situation is shown to the LLM or to the reader. Yes/no
    facts are written as TRUE/FALSE in front of the fact. Writing
    "x = false (the order was canceled)" instead made the model read the
    description and overlook the "false".
    """
    if not witness:
        return "- any situation"
    lines = []
    for name, value in witness.items():
        meaning = descriptions.get(name, "")
        if isinstance(value, bool):
            lines.append(f"- {'TRUE' if value else 'FALSE'}: {name} ({meaning})")
        else:
            lines.append(f"- {name} = {value} ({meaning})")
    return "\n".join(lines)


@dataclass
class Rule:
    """One requirement, compiled to Z3."""

    id: str                 # the rule's label in the spec, e.g. "R2"
    antecedent: z3.BoolRef  # WHEN / WHILE / IF part: the situations the rule applies to
    consequent: z3.BoolRef  # SHALL part: what must be true in those situations
    # The name of the event the rule reacts to, as the read step named it
    # ("trigger"); "" when it reacts to no event; None when the formal model
    # was made before the read step named triggers. Used only to see whether a
    # conflict needs two events at once.
    trigger: str | None = None

    @property
    def formula(self) -> z3.BoolRef:
        """The whole rule as one logical statement: antecedent => consequent."""
        return z3.Implies(self.antecedent, self.consequent)


class Vocabulary:
    """The Z3 view of the "symbols" list of a formal.json.

    Each symbol is a dict:

        name         identifier used inside the formulas
        sort         "Bool", "Int", "Real" or "Enum"
        values       the member names when sort is "Enum", otherwise unused
        description  what the symbol means in the spec (for humans and the LLM)
        event        true for something that happens at one moment (optional)
    """

    def __init__(self, symbols: list[dict]):
        # A private Z3 context, so that two specs loaded in the same process
        # (tests, batch runs) can never mix up their symbols.
        self.ctx = z3.Context()
        # name -> Z3 variable. These are the things that get values in a witness.
        self.variables: dict[str, z3.ExprRef] = {}
        # Every name the SMT-LIB parser may meet: the variables plus enum members.
        self._names: dict[str, z3.ExprRef] = {}
        # Names of the yes/no symbols marked as events: things that happen at
        # one moment, like a request or a click (see checks._simultaneous_events).
        self.events = {s["name"] for s in symbols if s.get("event") and s["sort"] == "Bool"}

        for symbol in symbols:
            name, sort = symbol["name"], symbol["sort"]
            if sort == "Bool":
                variable = z3.Bool(name, self.ctx)
            elif sort == "Int":
                variable = z3.Int(name, self.ctx)
            elif sort == "Real":
                variable = z3.Real(name, self.ctx)
            elif sort == "Enum":
                # An enum is a finite set of named values. Z3 knows the members
                # are distinct, which gives "an order has exactly one state"
                # for free, without any extra background fact.
                # With a single member the symbol could never be anything else,
                # so every condition on it would be silently always true.
                if len(symbol.get("values", [])) < 2:
                    raise ValueError(f"enum symbol '{name}' needs at least two values")
                enum_sort, members = z3.EnumSort(f"{name}__sort", symbol["values"], self.ctx)
                for member_name, member in zip(symbol["values"], members):
                    self._declare(member_name, member)
                variable = z3.Const(name, enum_sort)
            else:
                raise ValueError(f"symbol '{name}' has unknown sort '{sort}'")
            self._declare(name, variable)
            self.variables[name] = variable

    def _declare(self, name: str, expr: z3.ExprRef) -> None:
        """Register a name for the parser, refusing bad or duplicate names."""
        if not _IDENTIFIER.match(name):
            raise ValueError(f"'{name}' is not a valid symbol name")
        if name in self._names:
            raise ValueError(f"the name '{name}' is declared twice")
        self._names[name] = expr

    # ------------------------------------------------------------------ parsing

    def parse(self, text: str) -> z3.BoolRef:
        """Turn one SMT-LIB boolean expression into a Z3 formula.

        Example: "(and order_submitted (not inventory_available))".

        Z3's own parser does the work, so no Python `eval` is involved and any
        unknown symbol, type error or syntax error raises ValueError.
        """
        try:
            parsed = z3.parse_smt2_string(f"(assert {text})", decls=self._names, ctx=self.ctx)
        except z3.Z3Exception as error:
            raise ValueError(f"cannot parse '{text}': {error}") from error
        # Exactly one assertion must come back. More than one means the text
        # tried to smuggle in extra SMT-LIB commands.
        if len(parsed) != 1:
            raise ValueError(f"'{text}' is not a single expression")
        return parsed[0]

    def rule(self, data: dict) -> Rule:
        """Compile one rule dict of formal.json (id, antecedent, consequent, trigger).

        A trigger that is not an event symbol counts as no trigger ("").
        """
        trigger = data.get("trigger")
        if trigger is not None and trigger not in self.events:
            trigger = ""
        return Rule(data["id"], self.parse(data["antecedent"]), self.parse(data["consequent"]), trigger)

    # ---------------------------------------------------------------- questions
    # Z3 answers sat, unsat or unknown. The two methods below each commit to one
    # definite answer, so "unknown" can never be reported as a finding.

    def solver(self, formulas) -> z3.Solver:
        """A Z3 solver that holds the given formulas. Every question goes through one."""
        solver = z3.Solver(ctx=self.ctx)
        solver.set("timeout", SOLVER_TIMEOUT_MS)
        solver.add(*formulas)
        return solver

    def model(self, formulas) -> z3.ModelRef | None:
        """Return a situation in which all formulas hold, or None if Z3 found none."""
        solver = self.solver(formulas)
        return solver.model() if solver.check() == z3.sat else None

    def impossible(self, formulas) -> bool:
        """True only when Z3 proved that the formulas can never hold together."""
        return self.solver(formulas).check() == z3.unsat

    def implies(self, premises, conclusion) -> bool:
        """True only when Z3 proved that the conclusion follows from the premises.

        "Follows" means: no situation makes all premises true and the conclusion false.
        """
        return self.impossible(list(premises) + [z3.Not(conclusion)])

    # Two rules (translations of a requirement, for instance) are compared as
    # whole formulas, antecedent => consequent. So two that only split the
    # condition and the demand differently still count as the same.

    def same_meaning(self, a: Rule, b: Rule, given=()) -> bool:
        """True only when Z3 proved that no situation tells the two rules apart.

        "Tells apart" means: one rule allows the situation and the other
        forbids it. `given` is what every situation looked at must satisfy.
        """
        return self.impossible([z3.Xor(a.formula, b.formula), *given])

    def difference(self, a: Rule, b: Rule, given=()) -> dict:
        """A situation that one rule allows and the other forbids, as a witness.

        Returns {} when there is none (the two mean the same where `given` holds).
        """
        model = self.model([z3.Xor(a.formula, b.formula), *given])
        relevant = self.symbols_in(a.formula) | self.symbols_in(b.formula)
        return self.witness(model, relevant) if model is not None else {}

    # ---------------------------------------------------------------- witnesses
    # A witness is a concrete situation shown to the user, stored in JSON as
    # {symbol name: value}, e.g. {"order_submitted": true, "inventory_available": false}.

    def symbols_in(self, formula: z3.ExprRef) -> set[str]:
        """Names of the spec symbols that occur in a formula."""
        found, seen, todo = set(), set(), [formula]
        while todo:
            node = todo.pop()
            if node.get_id() in seen:
                continue
            seen.add(node.get_id())
            # A variable is a leaf whose name we declared ourselves. Enum members
            # and numbers are leaves too, but they are not in self.variables.
            if z3.is_const(node) and node.decl().name() in self.variables:
                found.add(node.decl().name())
            todo.extend(node.children())
        return found

    def witness(self, model: z3.ModelRef, names) -> dict:
        """Read the values of the given symbols out of a Z3 model, as JSON values."""
        result = {}
        for name in sorted(names):
            # model_completion: Z3 picks a value even for symbols it did not need.
            value = model.eval(self.variables[name], model_completion=True)
            if z3.is_true(value):
                result[name] = True
            elif z3.is_false(value):
                result[name] = False
            elif z3.is_int_value(value):
                result[name] = value.as_long()
            else:
                result[name] = str(value)  # an enum member, or a fraction like "1/2"
        return result

    def assignment(self, witness: dict) -> list[z3.BoolRef]:
        """The inverse of `witness`: one "symbol == value" formula per entry."""
        formulas = []
        for name, value in witness.items():
            variable = self.variables[name]
            if isinstance(value, bool):
                formulas.append(variable if value else z3.Not(variable))
            elif isinstance(value, int):
                formulas.append(variable == value)
            elif value in self._names:              # an enum member
                formulas.append(variable == self._names[value])
            else:                                   # a fraction written as text
                formulas.append(variable == z3.RealVal(value, self.ctx))
        return formulas
