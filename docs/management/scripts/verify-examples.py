"""Check the actual examples used in the documents against the frozen implementation.

Run with the project's Python environment, after extracting snapshot/source.zip
to build/baseline-498dea0. No model server is called and no archived file is changed.
"""
from __future__ import annotations

import argparse
import importlib.metadata
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--baseline', type=Path, default=ROOT / 'build' / 'baseline-498dea0')
parser.add_argument('--manifest', type=Path,
                    default=ROOT / 'snapshot' / '2026-11-24-498dea0' / 'manifest.json')
args = parser.parse_args()
baseline = args.baseline.resolve()
if not (baseline / 'speccheck' / 'formalize.py').is_file():
    raise SystemExit('Extract the current source snapshot into build/baseline-498dea0 first.')
sys.path.insert(0, str(baseline))

from speccheck.logic import Vocabulary
from speccheck.formalize import _judge, judge_second
from speccheck.checks import analyze, find_scenarios
from speccheck.change import Merged, after_model, about_change, changed_rules, merge

checks = []

def record(name, condition, detail):
    if not condition:
        raise AssertionError(name + ': ' + detail)
    checks.append({'name': name, 'passed': True, 'detail': detail})

def sym(name, sort='Bool', event=False):
    return {'name': name, 'sort': sort, 'values': [], 'description': name, 'event': event}

vocab = Vocabulary([sym(x, event=x in ('s', 'c')) for x in ('s','v','f','b','c','q','u')])
defs = [('R1','(and s v)','f'), ('R2','(and s (not v))','b'),
        ('R3','true','(not b)'), ('R4','c','u'), ('R5','q','(not f)')]
rules = [vocab.rule({'id': i, 'antecedent': a, 'consequent': c}) for i,a,c in defs]
phi = [r.formula for r in rules]
trigger = vocab.parse('(and s (not v))')
record('Order global satisfiability', vocab.model(phi) is not None,
       'All implications can hold when nothing triggers; global SAT alone misses R2/R3.')
record('Order feasible trigger', vocab.model([trigger]) is not None, 'Submitted, no stock is feasible.')
record('Order R2/R3 contradiction', vocab.impossible([trigger, rules[1].formula, rules[2].formula]),
       'The feasible trigger forces b and not b.')
record('Order R1/R5 contradiction', vocab.impossible([vocab.parse('(and s v q)'), rules[0].formula, rules[4].formula]),
       'Submission, stock and canceled/refunded force f and not f.')
assumption=vocab.parse('(not (and f q))')
other_trigger=vocab.parse('(and s v q)')
record('Assumption does not exclude the trigger', vocab.model([other_trigger,assumption]) is not None,
       'The assumed exclusion of fulfillment and refunded state leaves the triggering context feasible.')
record('Assumption can make R1 alone impossible', vocab.impossible([other_trigger,assumption,rules[0].formula]),
       'A facts-only pass can reject the case through single-rule exclusion; rules-only checking preserves R1/R5.')
record('Order allowed scenario', vocab.model(phi+[vocab.parse('(and (not s) (not c) (not q) (not b) f)')]) is not None,
       'Fulfillment without submission is permitted by the encoded requirements.')
record('Order quiet uncovered state', vocab.model([vocab.parse('(and (not s) (not c) (not q))')]+
       [vocab.parse('(not '+a+')') for i,a,c in defs if i != 'R3']) is not None,
       'No conditional antecedent applies; R3 is an unconditional prohibition.')

# A generalized gap describes a region, not one fully specified valuation.
# The baseline sensitivity mark only needs the alternative to cover some of it.
sensitivity = {
    'symbols': [sym(name, event=name == 's') for name in ('s', 'x', 'y', 'f')],
    'rules': [{
        'id': 'R1', 'trigger': 's', 'status': 'ambiguous',
        'text': 'Illustrative rule with two possible conditions',
        'reading': 'Respond to s when x holds',
        'antecedent': '(and s x)', 'consequent': 'f',
        'alternative': {'reading': 'Respond to s when y holds',
                        'antecedent': '(and s y)', 'consequent': 'f'},
    }],
}
sensitivity_findings = analyze(sensitivity)
event_gap = next(finding for finding in sensitivity_findings
                 if finding['type'] == 'gap' and finding.get('event') == 's')
ambiguity = next(finding for finding in sensitivity_findings if finding['type'] == 'ambiguity')
record('Generalized event gap', event_gap['when'] == {'s': True, 'x': False},
       'The original s-and-x rule leaves s true and x false uncovered; y is unspecified.')
record('Partial-coverage sensitivity annotation',
       'R1' in event_gap.get('depends_on_reading', {})
       and ambiguity['other_reading']['covers_gaps'] == 1,
       'The alternative s-and-y rule marks the original generalized gap as reading-dependent.')
variant = {**sensitivity, 'rules': [{**sensitivity['rules'][0],
                                   'status': 'accepted', 'antecedent': '(and s y)'}]}
sensitivity_vocab = Vocabulary(sensitivity['symbols'])
uncovered_completion = sensitivity_vocab.parse('(and s (not x) (not y))')
no_alternative_response = sensitivity_vocab.parse('(not (and s y))')
record('Alternative leaves uncovered completion',
       sensitivity_vocab.model([uncovered_completion, no_alternative_response]) is not None
       and any(finding['type'] == 'gap' and finding.get('event') == 's'
               for finding in analyze(variant)),
       's true, x false, y false remains uncovered after substitution; the mark is not full coverage.')

auth = Vocabulary([sym('n','Int'),sym('locked')])
def translation(a, c='locked'):
    return {'reading': 'Illustrative threshold reading', 'antecedent': a, 'consequent': c}
a=translation('(= n 5)')
b=translation('(>= n 5)')
d=translation('(> n 5)')
ar=auth.rule({'id':'A',**a}); br=auth.rule({'id':'B',**b})
witness=auth.parse('(and (= n 6) (not locked))')
record('Authentication distinct readings', not auth.same_meaning(ar,br), 'Exactly five and at least five differ.')
record('Authentication explicit witness', auth.model([witness,ar.formula]) is not None and auth.impossible([witness,br.formula]),
       'n=6, unlocked obeys the exact-five implication and violates at-least-five.')
for sizes, expected in [([8], 'accepted'),([7,1],'accepted'),([6,2],'ambiguous'),([5,3],'ambiguous'),([4,2,2],'rejected')]:
    answers=[t for t,count in zip([a,b,d],sizes) for _ in range(count)]
    result=_judge(auth,answers)
    record('Cluster '+str(sizes), result['status']==expected,
           f"Entropy {result['entropy']}; initial status {expected}; constructed samples, not a model experiment.")
second=judge_second(auth,{'id':'A',**a},[a]*3+[b]*5,8)
record('Second-reader illustration', second['support']=='3/8' and not second['confirms'] and 'antecedent' in second,
       'Three matching answers out of eight do not confirm; a usable alternative exists.')

# The authentication walkthrough uses the exact saved merged-model readings.
# R1-R4 describe the baseline scenarios; R5 is the actual administrator addition.
# The gap and allowed snapshot below are constructed illustrations, not saved runs.
auth_saved = json.loads((baseline/'specs/auth_change/formal.json').read_text(encoding='utf-8'))
auth_saved_vocab = Vocabulary(auth_saved['symbols'])
auth_rule_data = {rule['id']: rule for rule in auth_saved['rules']}
auth_rules = {name: auth_saved_vocab.rule(rule) for name, rule in auth_rule_data.items()}
record('Saved authentication formula and event vocabulary',
       auth_saved_vocab.events == {'password_submitted'}
       and auth_rule_data['R3']['trigger'] == 'password_submitted'
       and auth_rule_data['R3']['antecedent'] == '(= failed_attempts_count 5)',
       'Only password_submitted is an event. R3 names it in trigger metadata but its saved antecedent is n=5, without an event guard.')

auth_change = merge(baseline/'specs/auth_change/openspec/changes/admin-never-locked')
auth_changed = changed_rules(auth_saved, auth_change)
auth_active = after_model(auth_saved, auth_change)
auth_findings = analyze(auth_active)
admin_conflict = next(finding for finding in auth_findings
                      if finding['type'] == 'conflict' and set(finding['rules']) == {'R3', 'R5'})
saved_auth_findings = json.loads((baseline/'specs/auth_change/findings.json').read_text(encoding='utf-8'))
saved_admin_conflict = next(finding for finding in saved_auth_findings
                           if finding['type'] == 'conflict' and set(finding['rules']) == {'R3', 'R5'})
record('Saved administrator conflict replay',
       auth_changed == {'R5'} and admin_conflict['when'] == saved_admin_conflict['when']
       == {'failed_attempts_count': 5, 'is_administrator': True}
       and about_change(admin_conflict, [auth_active], [auth_changed]),
       'The actual saved R3/R5 conflict is reproduced at five failed attempts on an administrator account and belongs to the change.')
admin_context = auth_saved_vocab.assignment(saved_admin_conflict['when'])
record('Administrator conflict witness',
       auth_saved_vocab.model(admin_context) is not None
       and all(auth_saved_vocab.model(admin_context + [auth_rules[name].formula]) is not None
               for name in ('R3', 'R5'))
       and auth_saved_vocab.impossible(admin_context + [auth_rules['R3'].formula, auth_rules['R5'].formula]),
       'The case is feasible and neither rule alone forbids it; together R3 and R5 require locked and not locked, without assumed facts.')

auth_alternative = auth_saved_vocab.rule({'id': 'R3-alternative', **auth_rule_data['R3']['probes'][0]})
threshold_witness = auth_saved_vocab.assignment({'failed_attempts_count': 6, 'account_locked': False})
record('Authentication threshold witness from saved readings',
       auth_saved_vocab.model(threshold_witness + [auth_rules['R3'].formula]) is not None
       and auth_saved_vocab.impossible(threshold_witness + [auth_alternative.formula]),
       'The saved exact-five reading permits six attempts while unlocked; the saved at-least-five alternative forbids it. This proves formula difference, not English ambiguity.')
auth_ambiguity = next(finding for finding in auth_findings
                      if finding['type'] == 'ambiguity' and finding['rule'] == 'R3')
record('Saved authentication ambiguity replay',
       auth_ambiguity['found_by'] == 'questions'
       and auth_ambiguity['differs_when'] == {'account_locked': False, 'failed_attempts_count': 6}
       and auth_ambiguity['answers'] == {'translation': 2, 'other': 6, 'either': 0},
       'The archived interpretation probe flags R3; the saved vote is 2 for the translation, 6 for the alternative, 0 either.')

auth_baseline = {**auth_saved, 'rules': [rule for rule in auth_saved['rules'] if rule['id'] != 'R5']}
auth_removed_raw = {**auth_baseline,
                    'rules': [{**rule, 'id': 'X1' if rule['id'] == 'R2' else rule['id']}
                              for rule in auth_baseline['rules']]}
auth_removal = Merged('illustrative-remove-invalid-credentials', '',
                     {rule['id']: {'status': 'removed' if rule['id'] == 'X1' else 'existing'}
                      for rule in auth_removed_raw['rules']}, [], [])
auth_without_r2 = after_model(auth_removed_raw, auth_removal)
auth_gap_witness = {'password_submitted': True, 'password_correct': False,
                    'account_locked': False, 'failed_attempts_count': 0}
auth_gap_context = auth_saved_vocab.assignment(auth_gap_witness)
auth_no_response = [auth_saved_vocab.parse('(not ' + rule['antecedent'] + ')')
                    for rule in auth_without_r2['rules']]
record('Authentication gap witness after removing R2',
       auth_saved_vocab.model(auth_gap_context + auth_no_response) is not None
       and auth_saved_vocab.impossible(auth_gap_context + [auth_saved_vocab.parse(
           '(not ' + auth_rule_data['R2']['antecedent'] + ')')]),
       'Constructed baseline variation: an incorrect password is submitted to an unlocked account with n=0. R1, R3 and R4 do not apply; the removed R2 would apply.')
auth_opened_gap = next(finding for finding in analyze(auth_without_r2)
                       if finding.get('opened_by') == ['X1'])
record('Authentication removal produces attributed event gap',
       auth_opened_gap['event'] == 'password_submitted'
       and auth_opened_gap['when'].get('password_submitted') is True
       and auth_opened_gap['when'].get('password_correct') is False
       and auth_opened_gap['when'].get('account_locked') is False
       and about_change(auth_opened_gap, [auth_without_r2], [set()])
       and not any(finding.get('event') == 'password_submitted' and finding['type'] == 'gap'
                   for finding in analyze(auth_baseline)),
       'Removing R2 creates a password-submission gap attributed to X1; R1/R2 cover that event before the constructed removal. No saved OpenSpec delta is claimed for this variation.')

auth_allowed_witness = {'password_submitted': False, 'password_correct': False,
                        'access_granted': True, 'access_denied': False,
                        'failed_attempts_count': 0, 'account_locked': False,
                        'is_administrator': False}
auth_base_formulas = [auth_rules[name].formula for name in ('R1', 'R2', 'R3', 'R4')]
auth_facts = [auth_saved_vocab.parse(fact['formula']) for fact in auth_baseline['background']]
record('Authentication allowed scenario under baseline rules',
       auth_saved_vocab.model(auth_base_formulas + auth_facts
                              + auth_saved_vocab.assignment(auth_allowed_witness)) is not None
       and auth_saved_vocab.impossible(auth_saved_vocab.assignment(auth_allowed_witness)
                                        + [auth_rules['R1'].antecedent])
       and any(scenario['verdict'] == 'accepted' and scenario['rules'] == ['R1']
               for scenario in find_scenarios(auth_baseline)),
       'Constructed satisfying snapshot: grant access without a submitted password, at n=0 while unlocked; all baseline implications and saved facts hold. R1 says if, not only if.')
forbidden_context = auth_saved_vocab.assignment({'password_submitted': True,
                                                'account_locked': True, 'is_administrator': True})
record('Authentication ruled-out administrator scenario',
       auth_saved_vocab.model(forbidden_context) is not None
       and auth_saved_vocab.impossible(forbidden_context + [auth_rules['R5'].formula])
       and any(scenario['verdict'] == 'rejected' and scenario['rules'] == ['R5', 'R4']
               for scenario in find_scenarios(auth_saved)),
       'With the administrator addition, a locked administrator submitting a password is ruled out by R5 alone while R4 would apply. It is a generated ruled-out scenario, not a multi-rule conflict.')

delete=Vocabulary([sym('d'),sym('m'),sym('k')])
obligations=[delete.parse('(=> d m)'),delete.parse('k'),delete.parse('d')]
record('Deletion without assumed link', delete.model(obligations) is not None,
       'Separate removal and retention symbols can both hold.')
record('Deletion with assumed link', delete.impossible(obligations+[delete.parse('(=> (and d m) (not k))')]),
       'The explicit illustrative link exposes the D2/D4 clash; it remains an assumption.')

saved=json.loads((baseline/'specs/order/formal.json').read_text(encoding='utf-8'))
findings=analyze(saved)
conflicts={frozenset(x['rules']) for x in findings if x['type']=='conflict'}
record('Saved order model replay', {frozenset(['R2','R3']),frozenset(['R1','R5'])} <= conflicts,
       'Frozen specs/order/formal.json yields both named order conflicts under the archived implementation.')
record('Saved quiet gap', any(x['type']=='gap' and x.get('quiet') for x in findings),
       'The archived order model yields a quiet gap.')
without_backorder = {**saved, 'rules': [rule for rule in saved['rules'] if rule['id'] != 'R2']}
record('Missing no-stock response creates event gap',
       any(finding['type'] == 'gap' and finding.get('event') == 'order_submitted'
           and finding['when'].get('order_submitted') is True
           and finding['when'].get('inventory_available') is False
           for finding in analyze(without_backorder)),
       'Removing R2 leaves R1 reacting to submission and exposes a submitted, no-stock coverage gap.')

# The new removal illustration uses the short running-example vocabulary.
# X1 is the former R2; this is constructed input, not a sampled model result.
raw_order = {
    'symbols': [sym(x, event=x in ('s', 'c')) for x in ('s','v','f','b','c','q','u')],
    'background': [],
    'rules': [{'id': 'X1' if i == 'R2' else i, 'text': 'Illustrative ' + i,
               'status': 'accepted', 'antecedent': a, 'consequent': c,
               'trigger': 's' if i in ('R1','R2') else 'c' if i == 'R4' else ''}
              for i, a, c in defs],
}
removed_change = Merged('remove-no-stock-response', '',
                        {r['id']: {'status': 'removed' if r['id'] == 'X1' else 'existing'}
                         for r in raw_order['rules']}, [], [])
active_order = after_model(raw_order, removed_change)
changed_ids = changed_rules(raw_order, removed_change)
opened = next(f for f in analyze(active_order) if f.get('opened_by') == ['X1'])
record('Removed order rule is separated from active obligations',
       all(r['id'] != 'X1' for r in active_order['rules'])
       and [r['id'] for r in active_order['removed_rules']] == ['X1'],
       'Former R2 is kept only as a removal seed; R3 remains an active prohibition.')
record('Removal opens the illustrated no-stock situation',
       opened['event'] == 's' and opened['when'] == {'s': True, 'v': False, 'c': False, 'q': False},
       'Submission with no stock, no cancellation and no canceled/refunded state has no conditional response.')
record('Removal-only gap belongs in the change report',
       not changed_ids and about_change(opened, [active_order], [changed_ids]),
       'opened_by X1 attributes this gap even though no rule was added or modified.')
retired_change = removed_change._replace(
    scenarios={i: {'status': 'removed' if i in ('R1', 'X1') else 'existing'}
               for i in removed_change.scenarios})
record('Retiring the last submission response gives no submission gap',
       not any(f.get('event') == 's' for f in analyze(after_model(raw_order, retired_change))),
       'The event-gap search covers events still handled by surviving conditional rules.')

# Replay the genuine saved removal example through change preprocessing.
visitor_raw = json.loads((baseline/'experiments/examples/visitors_removed/formal.json').read_text(encoding='utf-8'))
visitor_change = Merged('visitors-removed', '',
                        {r['id']: {'status': 'removed' if r['id'] == 'X1' else 'existing'}
                         for r in visitor_raw['rules']}, [], [])
visitor_active = after_model(visitor_raw, visitor_change)
visitor_gap = next(f for f in analyze(visitor_active) if f.get('opened_by') == ['X1'])
record('Saved visitor removal replay',
       visitor_gap['event'] == 'visitor_checks_in'
       and visitor_gap['when'].get('visitor_checks_in') is True
       and visitor_gap['when'].get('visitor_on_list') is False
       and about_change(visitor_gap, [visitor_active], [set()]),
       'The saved encoding yields a change-related gap for an unlisted visitor after X1 is removed.')

# Confirm the documented input boundary without calling a model.
with TemporaryDirectory(prefix='speccheck-doc-example-') as temporary:
    project_root = Path(temporary) / 'openspec'
    spec_file = project_root / 'specs' / 'auth' / 'spec.md'
    delta_file = project_root / 'changes' / 'edit' / 'specs' / 'auth' / 'spec.md'
    spec_file.parent.mkdir(parents=True)
    delta_file.parent.mkdir(parents=True)
    scenario = ('#### Scenario: Lockout\n'
                '- **WHEN** failed attempts reach 5\n'
                '- **THEN** the account is locked\n')
    spec_file.write_text('### Requirement: Access\nThe system SHALL lock accounts.\n' + scenario,
                         encoding='utf-8')
    changed_sentence = 'The system SHALL lock non-administrator accounts.'
    delta_file.write_text('## MODIFIED Requirements\n### Requirement: Access\n'
                          + changed_sentence + '\n' + scenario, encoding='utf-8')
    incremental = merge(delta_file.parents[2], on_base=True)
    full = merge(delta_file.parents[2])
    record('Sentence-only edit is absent from incremental input',
           incremental.text == '' and bool(incremental.changed_text)
           and incremental.scenarios['R1']['status'] == 'existing'
           and changed_sentence in full.text,
           'The full input includes the changed SHALL sentence; scenario-only reuse emits no new text.')
    delta_file.write_text('## ADDED Requirements\n### Requirement: Audit\n'
                          'The system SHALL record lockouts.\n', encoding='utf-8')
    record('Scenario-free added requirement is absent from incremental input',
           merge(delta_file.parents[2], on_base=True).text == ''
           and 'record lockouts' in merge(delta_file.parents[2]).text,
           'A new requirement without scenarios also needs full formalization in this revision.')

manifest=json.loads(args.manifest.read_text(encoding='utf-8-sig'))
report={'snapshot_revision':manifest['commit'], 'baseline':str(baseline),
        'python':sys.version.split()[0], 'z3_solver':importlib.metadata.version('z3-solver'),
        'network_calls':0, 'checks':checks, 'passed':len(checks)}
out=ROOT/'evidence/example-checks.json'
out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'{len(checks)} example checks passed; {out}')
