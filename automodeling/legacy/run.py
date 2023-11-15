from src.legacy.simplify_toc import simplify_table_of_contents
from src.legacy.convert_page_to_snippet import convert_page_to_snippets
from src.legacy.snippet_to_ontology import extract_ontology_from_next_snippet
from src.legacy.inject_ontology_to_snippet import inject_ontology_into_snippet
from src.legacy.convert_snippet_to_lap import convert_snippet_to_lap_simple
from src.legacy.harmnize_lap import harmonize_declarations
from src.legacy.apply_ontology import apply_ontology_to_lap
from src.legacy.convert_lap_to_json import convert_lap_to_json
from src.legacy.get_graph import get_graph
from src.legacy.assemble_clauses import assemble_clauses
from src.legacy.clean_md import clean_page
from src.legacy.llm import LLM

# PDF 2 MD
# MD to sections
# MD to ONTOLOGY
# MD + ontology -> computable contract
# test MD -> situation

p1 = """CONTENTS
Motor Breakdown Insurance Policy & Summary
A – Policy wording 3
Breakdown Causes 8
SECTION A – AXA LOCAL 9
SECTION B – AXA NATIONWIDE 10
SECTION C – AXA NATIONWIDE & HOMESTART 11
SECTION A, B, C – MISFUELLING 12
SECTION D – AXA EUROPEAN 13
SECTION E – GENERAL EXCLUSIONS THAT APPLY TO ALL PARTS 17 OF THIS POLICY
SECTION F – GENERAL CONDITIONS APPLYING TO ALL PARTS 20 OF THIS POLICY
B – Policy summary 26 AXA BREAKDOWN COVER POLICY SUMMARY 26"""

p2 = """A – Policy wording STATUS
This policy is provided on behalf of AXA Insurance by AXA Assistance (UK) Ltd. AXA Assistance (UK) Limited is authorised and regulated by
the Financial Conduct Authority. AXA Assistance (UK) Limited’s firm register number is 439069. You can check this on the Financial Services Register by visiting
the website www.fca.org.uk/ register. Its registered office is at The Quadrangle, 106-118 Station Road, Redhill, Surrey, RH1 1PR. It is registered in England under company number 02638890.
This policy is underwritten by Inter Partner Assistance SA UK Branch
(IPA) which is fully owned by the
AXA Assistance Group. Inter Partner Assistance is a Belgian firm authorised by the National Bank of Belgium and subject to limited regulation by the Financial Conduct Authority. Details about the extent of its regulation by the Financial Conduct Authority are available from us on request. Inter Partner Assistance SA’s register number is 202664. You can check this on the Financial Services Register by visiting the website www.fca.org.uk/register.
AXA Assistance (UK) Limited operates the 24-hour motoring assistance helpline.
This insurance is governed by the laws of England and Wales.
IMPORTANT INFORMATION
This document sets out the terms and conditions of your cover and it is important that you read it carefully. There are different levels of cover available. The cover you hold will be set out in the accompanying policy schedule. If changes are made, these will be confirmed to you separately in writing.
Each section of cover explains what
is and is not covered. There are also general exclusions (things that are not included) that apply to all sections
of the cover, and there are general conditions that you must follow so you are entitled to the cover.
CANCELLATION
If you find that the cover provided under this policy does not meet your needs, please contact us on 0800 169 0206 within 14 days of receiving this document and we will cancel this policy.
You will receive a full refund of your premium as long as you have not made any claims.
If you cancel the policy outside the 14-day period, as long as you have not made any claims, you will receive a refund of your premium for the
Motor Breakdown Insurance Policy & Summary
 3
Policy wording continued
amount of time left to run on the policy, less an administrative charge of £15.
We may cancel this policy by giving you at least 14 days’ written notice at your last-known address if:
 you fail to pay the premiums after we have sent you a reminder to
do so. If we have been unable to collect a premium payment, we will contact you in writing requesting payment to be made by a specific date. If we do not receive payment by this date we will cancel your policy by immediate effect and notify you in writing that such cancellation has taken place;
 you refuse to allow us reasonable access to your vehicle to provide the services you have asked for under this policy or if you fail to co- operate with our representatives;
 you otherwise stop keeping to the terms and conditions of this policy in any significant way; or
 the cost of providing this policy becomes prohibitive.
We may cancel this policy without giving you notice if, by law or other reason, we are prevented from providing it.
If we cancel the policy under this section, we will refund the
premium paid for the remaining period of insurance, unless you have made any claims. We can refuse to renew any individual policy.
We may cancel this policy without giving you notice and without refunding your premium if you:
 make or try to make a fraudulent claim under your policy;
 are abusive or threatening towards our staff; or
 repeatedly or seriously break the terms of this policy.
If you make a valid claim before the policy is cancelled, we will pay the claim before we cancel the policy.
MEANING OF WORDS
Wherever the following words
and phrases appear in bold in this document, they will always have the following meanings.
1. We, us, our
Inter Partner Assistance SA and AXA Assistance (UK Branch) Ltd both of The Quadrangle, 106-118 Station Road, Redhill, Surrey, RH1 1PR, UK.
2. Vehicle policy
This policy covers breakdown assistance for the specific vehicle
(or vehicles) shown on your policy schedule. These are the only vehicles that this cover applies to.
"""


def run():
    md = [p1, p2]
    toc = simplify_table_of_contents(md[0], LLM)
    toc = toc.message.content
    graphs = []
    global_ontologies = []  # TODO need to merge ontologies

    for page in md[1:]:
        snippets = convert_page_to_snippets(page, LLM)
        for snippet in snippets:
            ontologies = extract_ontology_from_next_snippet(snippet)
            lap = convert_snippet_to_lap_simple(snippet, global_ontologies)

            # TODO handle when ontology empty in other tasks
            # get only relevant ontology
            # not used
            # if global_ontologies:
            # snippet = inject_ontology_into_snippet(snippet, global_ontologies)

            lap = harmonize_declarations(lap, None, LLM)  # no harmonized ontology
            lap = apply_ontology_to_lap(global_ontologies, lap, LLM)
            lap_json = convert_lap_to_json(lap, LLM)
            # TODO copy graph function, not sure needed
            # graph = get_graph(lap_json, snippet)
            graphs.append(lap_json)
            global_ontologies.extend(ontologies)

    general_conditions, coverages, general_exclusions = assemble_clauses(toc, graphs)


if __name__ == "__main__":
    run()
